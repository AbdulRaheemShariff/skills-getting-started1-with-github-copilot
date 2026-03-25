"""
Tests for the desktop recording / playback data model and serialisation.

These tests cover the pure-Python parts of the tool (Event, Session) and the
Player/Recorder interface, without requiring an actual display or device drivers.
"""

import json
import time
from pathlib import Path

import pytest

from src.desktop_recorder import Event, Session, _key_name, _parse_key, build_parser


# ──────────────────────────────────────────────────────────────────────────────
# Event
# ──────────────────────────────────────────────────────────────────────────────


def test_event_to_dict_round_trip():
    e = Event(timestamp=1.5, kind="mouse_click", data={"x": 100, "y": 200, "pressed": True})
    d = e.to_dict()
    restored = Event.from_dict(d)
    assert restored.timestamp == e.timestamp
    assert restored.kind == e.kind
    assert restored.data == e.data


def test_event_from_dict_defaults_empty_data():
    d = {"timestamp": 0.0, "kind": "mouse_move"}
    e = Event.from_dict(d)
    assert e.data == {}


def test_event_kinds_preserved():
    for kind in ("mouse_move", "mouse_click", "mouse_scroll", "key_press", "key_release"):
        e = Event(timestamp=0.0, kind=kind)
        assert Event.from_dict(e.to_dict()).kind == kind


# ──────────────────────────────────────────────────────────────────────────────
# Session serialisation
# ──────────────────────────────────────────────────────────────────────────────


def _make_session() -> Session:
    s = Session(name="pytest_session", recorded_at="2025-01-01T00:00:00")
    s.events = [
        Event(0.0,  "mouse_move",  {"x": 10, "y": 20}),
        Event(0.5,  "mouse_click", {"x": 10, "y": 20, "button": "Button.left", "pressed": True}),
        Event(0.6,  "mouse_click", {"x": 10, "y": 20, "button": "Button.left", "pressed": False}),
        Event(1.0,  "key_press",   {"key": "a"}),
        Event(1.1,  "key_release", {"key": "a"}),
        Event(2.0,  "mouse_scroll", {"x": 50, "y": 50, "dx": 0, "dy": -3}),
    ]
    return s


def test_session_save_and_load(tmp_path: Path):
    original = _make_session()
    path = tmp_path / "session.json"
    original.save(path)

    loaded = Session.load(path)
    assert loaded.name == original.name
    assert loaded.recorded_at == original.recorded_at
    assert len(loaded.events) == len(original.events)
    for orig, rest in zip(original.events, loaded.events):
        assert rest.timestamp == orig.timestamp
        assert rest.kind == orig.kind
        assert rest.data == orig.data


def test_session_save_creates_valid_json(tmp_path: Path):
    path = tmp_path / "out.json"
    _make_session().save(path)
    payload = json.loads(path.read_text())
    assert "events" in payload
    assert payload["event_count"] == 6


def test_session_load_missing_file_raises(tmp_path: Path):
    with pytest.raises(FileNotFoundError):
        Session.load(tmp_path / "nope.json")


def test_session_summary_contains_name():
    s = _make_session()
    summary = s.summary()
    assert "pytest_session" in summary
    assert "mouse_click" in summary
    assert "key_press" in summary


def test_session_summary_empty():
    s = Session()
    assert "(no events)" in s.summary()


def test_session_duration_in_summary():
    s = _make_session()
    summary = s.summary()
    # Duration should be ~2.0 s (last event at t=2.0, first at t=0.0)
    assert "2.00s" in summary


# ──────────────────────────────────────────────────────────────────────────────
# Playback timing logic (mocked — no display required)
# ──────────────────────────────────────────────────────────────────────────────


def test_player_calls_on_event_for_each_event():
    """Player.play() must invoke the on_event callback for every event."""
    import types
    import src.desktop_recorder as dr

    fake_kb = types.ModuleType("pynput.keyboard")
    fake_ms = types.ModuleType("pynput.mouse")

    class _FakeKBController:
        def press(self, key): pass
        def release(self, key): pass

    class _FakeMouseController:
        def __init__(self): self.position = (0, 0)
        def press(self, btn): pass
        def release(self, btn): pass
        def scroll(self, dx, dy): pass

    class _FakeKeyMeta(type):
        def __getitem__(cls, name): raise KeyError(name)

    class _FakeKey(metaclass=_FakeKeyMeta):
        """Minimal pynput.keyboard.Key stand-in."""
        enter = "enter"

    class _FakeKeyCode:
        @staticmethod
        def from_char(c): return c

    class _FakeButtonMeta(type):
        def __getitem__(cls, name): raise KeyError(name)

    class _FakeButton(metaclass=_FakeButtonMeta):
        left = "left"
        right = "right"
        middle = "middle"

    fake_kb.Controller = _FakeKBController
    fake_kb.Key = _FakeKey
    fake_kb.KeyCode = _FakeKeyCode
    fake_ms.Controller = _FakeMouseController
    fake_ms.Button = _FakeButton

    orig_gui = dr._GUI_AVAILABLE
    orig_kb = dr._kb
    orig_ms = dr._ms

    dr._GUI_AVAILABLE = True
    dr._kb = fake_kb
    dr._ms = fake_ms

    try:
        session = _make_session()
        player = dr.Player(session, speed=100.0)  # 100× speed → near-instant

        fired: list[Event] = []
        player.play(on_event=fired.append)

        assert len(fired) == len(session.events)
        assert [e.kind for e in fired] == [e.kind for e in session.events]
    finally:
        dr._GUI_AVAILABLE = orig_gui
        dr._kb = orig_kb
        dr._ms = orig_ms


# ──────────────────────────────────────────────────────────────────────────────
# CLI argument parser
# ──────────────────────────────────────────────────────────────────────────────


def test_parser_record_defaults():
    parser = build_parser()
    args = parser.parse_args(["record"])
    assert args.command == "record"
    assert args.output == "session.json"
    assert args.screenshots is False


def test_parser_record_custom_output():
    args = build_parser().parse_args(["record", "-o", "custom.json", "-n", "demo"])
    assert args.output == "custom.json"
    assert args.name == "demo"


def test_parser_play_defaults():
    args = build_parser().parse_args(["play"])
    assert args.command == "play"
    assert args.input == "session.json"
    assert args.speed == pytest.approx(1.0)
    assert args.verbose is False


def test_parser_play_with_speed():
    args = build_parser().parse_args(["play", "-s", "2.5", "-v"])
    assert args.speed == pytest.approx(2.5)
    assert args.verbose is True


def test_parser_list_defaults():
    args = build_parser().parse_args(["list"])
    assert args.command == "list"
    assert args.events is False


def test_parser_list_with_events_flag():
    args = build_parser().parse_args(["list", "--events"])
    assert args.events is True


def test_parser_invalid_command_exits():
    with pytest.raises(SystemExit):
        build_parser().parse_args(["badcommand"])


# ──────────────────────────────────────────────────────────────────────────────
# Helper functions
# ──────────────────────────────────────────────────────────────────────────────


def test_key_name_returns_char_for_char_key():
    class _FakeCharKey:
        char = "q"

    assert _key_name(_FakeCharKey()) == "q"


def test_key_name_falls_back_to_str():
    class _FakeSpecialKey:
        @property
        def char(self):
            raise AttributeError

        def __str__(self):
            return "Key.enter"

    assert _key_name(_FakeSpecialKey()) == "Key.enter"


def test_player_speed_zero_raises():
    import types
    import src.desktop_recorder as dr

    fake_kb = types.ModuleType("pynput.keyboard")
    fake_ms = types.ModuleType("pynput.mouse")

    class _FakeKBController:
        pass

    class _FakeMouseController:
        def __init__(self): self.position = (0, 0)

    fake_kb.Controller = _FakeKBController
    fake_ms.Controller = _FakeMouseController

    orig_gui = dr._GUI_AVAILABLE
    orig_kb = dr._kb
    orig_ms = dr._ms
    dr._GUI_AVAILABLE = True
    dr._kb = fake_kb
    dr._ms = fake_ms

    try:
        with pytest.raises(ValueError, match="speed must be positive"):
            dr.Player(Session(), speed=0)
    finally:
        dr._GUI_AVAILABLE = orig_gui
        dr._kb = orig_kb
        dr._ms = orig_ms
