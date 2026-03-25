"""
Desktop Graphics Application Recorder & Player
===============================================

A tool that records all mouse and keyboard interactions with any desktop
graphics application and plays them back with pixel-perfect timing.

Usage (CLI)
-----------
  python src/desktop_recorder.py record --output my_session.json
  python src/desktop_recorder.py play   --input  my_session.json
  python src/desktop_recorder.py list   --input  my_session.json

Compile to a standalone executable
------------------------------------
  python build.py
  # produces  dist/desktop_recorder  (Linux/macOS)
  #           dist/desktop_recorder.exe  (Windows)
"""

from __future__ import annotations

import argparse
import json
import sys
import time
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any

# ---------------------------------------------------------------------------
# Optional GUI dependencies — imported lazily so the module can be imported
# (e.g. during tests) even on headless CI machines.
# ---------------------------------------------------------------------------
try:
    import pyautogui  # type: ignore[import]
    import pynput.keyboard as _kb  # type: ignore[import]
    import pynput.mouse as _ms  # type: ignore[import]

    _GUI_AVAILABLE = True
except Exception:  # noqa: BLE001
    pyautogui = None  # type: ignore[assignment]
    _kb = None  # type: ignore[assignment]
    _ms = None  # type: ignore[assignment]
    _GUI_AVAILABLE = False

try:
    from PIL import Image, ImageGrab  # type: ignore[import]

    _PIL_AVAILABLE = True
except Exception:  # noqa: BLE001
    _PIL_AVAILABLE = False


# ---------------------------------------------------------------------------
# Data model
# ---------------------------------------------------------------------------


@dataclass
class Event:
    """A single recorded interaction event."""

    timestamp: float  # seconds since session start
    kind: str  # "mouse_move" | "mouse_click" | "mouse_scroll" | "key_press" | "key_release"
    data: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_dict(cls, d: dict[str, Any]) -> "Event":
        return cls(
            timestamp=d["timestamp"],
            kind=d["kind"],
            data=d.get("data", {}),
        )


@dataclass
class Session:
    """A complete recording session (ordered list of events + metadata)."""

    name: str = ""
    recorded_at: str = ""
    events: list[Event] = field(default_factory=list)

    # ------------------------------------------------------------------
    # Serialisation
    # ------------------------------------------------------------------

    def save(self, path: Path | str) -> None:
        """Persist the session as a human-readable JSON file."""
        path = Path(path)
        payload = {
            "name": self.name,
            "recorded_at": self.recorded_at,
            "event_count": len(self.events),
            "events": [e.to_dict() for e in self.events],
        }
        path.write_text(json.dumps(payload, indent=2))

    @classmethod
    def load(cls, path: Path | str) -> "Session":
        """Load a previously recorded session from disk."""
        path = Path(path)
        raw = json.loads(path.read_text())
        return cls(
            name=raw.get("name", ""),
            recorded_at=raw.get("recorded_at", ""),
            events=[Event.from_dict(e) for e in raw.get("events", [])],
        )

    # ------------------------------------------------------------------
    # Summaries
    # ------------------------------------------------------------------

    def summary(self) -> str:
        """Return a multi-line human-readable summary."""
        if not self.events:
            return "  (no events)"
        duration = self.events[-1].timestamp - self.events[0].timestamp
        counts: dict[str, int] = {}
        for e in self.events:
            counts[e.kind] = counts.get(e.kind, 0) + 1
        lines = [
            f"  Name        : {self.name or '(unnamed)'}",
            f"  Recorded at : {self.recorded_at or 'n/a'}",
            f"  Duration    : {duration:.2f}s",
            f"  Total events: {len(self.events)}",
        ]
        for kind, n in sorted(counts.items()):
            lines.append(f"    {kind:<20}: {n}")
        return "\n".join(lines)


# ---------------------------------------------------------------------------
# Recorder
# ---------------------------------------------------------------------------


class Recorder:
    """
    Captures mouse and keyboard events in real-time and stores them in a
    Session object.

    Example::

        rec = Recorder()
        rec.start()
        # … user interacts with the desktop …
        rec.stop()
        rec.session.save("my_recording.json")
    """

    def __init__(self, capture_screenshots: bool = False) -> None:
        if not _GUI_AVAILABLE:
            raise RuntimeError(
                "pynput / pyautogui not available; "
                "install them with: pip install pynput pyautogui"
            )
        self._capture_screenshots = capture_screenshots
        self.session = Session()
        self._start_time: float = 0.0
        self._mouse_listener: Any = None
        self._kb_listener: Any = None

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def start(self) -> None:
        """Begin recording. Non-blocking — listeners run in background threads."""
        import datetime

        self._start_time = time.time()
        self.session = Session(
            name="",
            recorded_at=datetime.datetime.now().isoformat(timespec="seconds"),
        )

        self._mouse_listener = _ms.Listener(
            on_move=self._on_move,
            on_click=self._on_click,
            on_scroll=self._on_scroll,
        )
        self._kb_listener = _kb.Listener(
            on_press=self._on_key_press,
            on_release=self._on_key_release,
        )
        self._mouse_listener.start()
        self._kb_listener.start()

    def stop(self) -> None:
        """Stop recording and join listener threads."""
        if self._mouse_listener:
            self._mouse_listener.stop()
        if self._kb_listener:
            self._kb_listener.stop()

    # ------------------------------------------------------------------
    # Internal callbacks
    # ------------------------------------------------------------------

    def _ts(self) -> float:
        return time.time() - self._start_time

    def _on_move(self, x: int, y: int) -> None:
        self.session.events.append(
            Event(timestamp=self._ts(), kind="mouse_move", data={"x": x, "y": y})
        )

    def _on_click(self, x: int, y: int, button: Any, pressed: bool) -> None:
        self.session.events.append(
            Event(
                timestamp=self._ts(),
                kind="mouse_click",
                data={
                    "x": x,
                    "y": y,
                    "button": str(button),
                    "pressed": pressed,
                },
            )
        )
        if self._capture_screenshots and _PIL_AVAILABLE and pressed:
            self._screenshot(x, y)

    def _on_scroll(self, x: int, y: int, dx: int, dy: int) -> None:
        self.session.events.append(
            Event(
                timestamp=self._ts(),
                kind="mouse_scroll",
                data={"x": x, "y": y, "dx": dx, "dy": dy},
            )
        )

    def _on_key_press(self, key: Any) -> None:
        self.session.events.append(
            Event(
                timestamp=self._ts(),
                kind="key_press",
                data={"key": _key_name(key)},
            )
        )

    def _on_key_release(self, key: Any) -> None:
        self.session.events.append(
            Event(
                timestamp=self._ts(),
                kind="key_release",
                data={"key": _key_name(key)},
            )
        )

    def _screenshot(self, x: int, y: int) -> None:
        """Capture a screenshot centred around (x, y) and attach to last event."""
        region = (max(0, x - 50), max(0, y - 50), x + 50, y + 50)
        try:
            img = ImageGrab.grab(bbox=region)
            # Store as a tiny thumbnail to keep the JSON lean
            img = img.resize((50, 50), Image.LANCZOS)
            import base64
            import io

            buf = io.BytesIO()
            img.save(buf, format="PNG")
            b64 = base64.b64encode(buf.getvalue()).decode()
            if self.session.events:
                self.session.events[-1].data["screenshot_b64"] = b64
        except Exception:  # noqa: BLE001
            pass


# ---------------------------------------------------------------------------
# Player
# ---------------------------------------------------------------------------


class Player:
    """
    Replays a previously recorded Session, reproducing every mouse and
    keyboard event with the original timing.

    Example::

        session = Session.load("my_recording.json")
        player  = Player(session)
        player.play()
    """

    def __init__(self, session: Session, speed: float = 1.0) -> None:
        """
        :param session: The Session to play back.
        :param speed:   Playback speed multiplier.  1.0 = real time,
                        2.0 = double speed, 0.5 = half speed.
        """
        if not _GUI_AVAILABLE:
            raise RuntimeError(
                "pynput / pyautogui not available; "
                "install them with: pip install pynput pyautogui"
            )
        if speed <= 0:
            raise ValueError("speed must be positive")
        self.session = session
        self.speed = speed
        self._kb_ctrl = _kb.Controller()
        self._ms_ctrl = _ms.Controller()

    def play(self, on_event: Any = None) -> None:
        """
        Replay all events.

        :param on_event: Optional callable(event) called before each event
                         is replayed — useful for progress logging.
        """
        if pyautogui is not None:
            pyautogui.FAILSAFE = True  # move mouse to corner to abort
            pyautogui.PAUSE = 0  # we handle timing ourselves

        events = self.session.events
        if not events:
            return

        wall_start = time.time()
        rec_start = events[0].timestamp

        for event in events:
            # Sleep until this event should fire
            target = wall_start + (event.timestamp - rec_start) / self.speed
            now = time.time()
            if target > now:
                time.sleep(target - now)

            if on_event:
                on_event(event)

            self._dispatch(event)

    # ------------------------------------------------------------------
    # Internal dispatcher
    # ------------------------------------------------------------------

    def _dispatch(self, event: Event) -> None:
        d = event.data
        if event.kind == "mouse_move":
            self._ms_ctrl.position = (d["x"], d["y"])

        elif event.kind == "mouse_click":
            btn = _parse_button(d["button"])
            if d["pressed"]:
                self._ms_ctrl.press(btn)
            else:
                self._ms_ctrl.release(btn)

        elif event.kind == "mouse_scroll":
            self._ms_ctrl.scroll(d["dx"], d["dy"])

        elif event.kind == "key_press":
            self._kb_ctrl.press(_parse_key(d["key"]))

        elif event.kind == "key_release":
            self._kb_ctrl.release(_parse_key(d["key"]))


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _key_name(key: Any) -> str:
    """Normalise a pynput key to a plain string."""
    try:
        return key.char  # type: ignore[union-attr]
    except AttributeError:
        return str(key)


def _parse_key(name: str) -> Any:
    """Convert a stored key name back to a pynput Key or character."""
    if _GUI_AVAILABLE:
        # Try special keys first
        try:
            return _kb.Key[name.removeprefix("Key.")]
        except KeyError:
            pass
        # Single character
        if len(name) == 1:
            return name
        # Fallback
        try:
            return _kb.KeyCode.from_char(name)
        except Exception:  # noqa: BLE001
            return name
    return name


def _parse_button(name: str) -> Any:
    """Convert a stored button name back to a pynput Button."""
    if _GUI_AVAILABLE:
        try:
            return _ms.Button[name.removeprefix("Button.")]
        except KeyError:
            return _ms.Button.left
    return name


# ---------------------------------------------------------------------------
# Command-line interface
# ---------------------------------------------------------------------------


def _cmd_record(args: argparse.Namespace) -> None:
    """Interactive recording loop."""
    print("Desktop Recorder — press Ctrl+C to stop recording.\n")
    rec = Recorder(capture_screenshots=args.screenshots)
    rec.session.name = args.name or Path(args.output).stem
    try:
        rec.start()
        print("Recording … (interact with any application)")
        while True:
            time.sleep(0.1)
    except KeyboardInterrupt:
        print("\nStopping recorder …")
    finally:
        rec.stop()
        output = Path(args.output)
        rec.session.save(output)
        print(f"Session saved to '{output}'")
        print(rec.session.summary())


def _cmd_play(args: argparse.Namespace) -> None:
    """Load and replay a session."""
    path = Path(args.input)
    if not path.exists():
        print(f"Error: '{path}' not found.", file=sys.stderr)
        sys.exit(1)

    session = Session.load(path)
    print(f"Playing back '{path}'\n{session.summary()}\n")

    player = Player(session, speed=args.speed)

    def _log(event: Event) -> None:
        print(f"  t={event.timestamp:7.3f}s  {event.kind:<18}  {event.data}")

    player.play(on_event=_log if args.verbose else None)
    print("Playback complete.")


def _cmd_list(args: argparse.Namespace) -> None:
    """Print a summary of a saved session."""
    path = Path(args.input)
    if not path.exists():
        print(f"Error: '{path}' not found.", file=sys.stderr)
        sys.exit(1)

    session = Session.load(path)
    print(f"Session file : {path}")
    print(session.summary())
    if args.events:
        print("\nEvents:")
        for i, e in enumerate(session.events):
            print(f"  {i:4d}  t={e.timestamp:8.3f}s  {e.kind:<18}  {e.data}")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="desktop_recorder",
        description=(
            "Record and play back desktop graphics application interactions. "
            "Compile to a standalone exe with:  python build.py"
        ),
    )
    sub = parser.add_subparsers(dest="command", required=True)

    # record
    r = sub.add_parser("record", help="Record mouse and keyboard events")
    r.add_argument("-o", "--output", default="session.json", help="Output JSON file")
    r.add_argument("-n", "--name", default="", help="Human-readable session name")
    r.add_argument(
        "--screenshots",
        action="store_true",
        help="Capture a small screenshot region on each mouse click",
    )

    # play
    p = sub.add_parser("play", help="Replay a recorded session")
    p.add_argument("-i", "--input", default="session.json", help="Session JSON file")
    p.add_argument(
        "-s",
        "--speed",
        type=float,
        default=1.0,
        help="Playback speed multiplier (default 1.0)",
    )
    p.add_argument(
        "-v", "--verbose", action="store_true", help="Print each event as it fires"
    )

    # list
    ls = sub.add_parser("list", help="Show a summary of a recorded session")
    ls.add_argument("-i", "--input", default="session.json", help="Session JSON file")
    ls.add_argument(
        "--events", action="store_true", help="Print every event in the session"
    )

    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()

    if args.command == "record":
        _cmd_record(args)
    elif args.command == "play":
        _cmd_play(args)
    elif args.command == "list":
        _cmd_list(args)


if __name__ == "__main__":
    main()
