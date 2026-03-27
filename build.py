"""
Build script — compiles desktop_recorder.py into a single standalone executable.

Usage
-----
    python build.py

Output
------
    dist/desktop_recorder        (Linux / macOS)
    dist/desktop_recorder.exe    (Windows)

Requirements
------------
    pip install pyinstaller pynput pyautogui Pillow
    # or simply:
    pip install -r requirements.txt
"""

import subprocess
import sys
from pathlib import Path


def main() -> None:
    repo_root = Path(__file__).parent

    print("=" * 60)
    print("Desktop Recorder - PyInstaller build")
    print("=" * 60)

    # Ensure PyInstaller is available
    try:
        import PyInstaller  # noqa: F401
    except ImportError:
        print("PyInstaller not found - installing ...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pyinstaller"])

    spec_file = repo_root / "desktop_recorder.spec"
    if not spec_file.exists():
        print(f"Error: spec file not found at {spec_file}", file=sys.stderr)
        sys.exit(1)

    cmd = [
        sys.executable,
        "-m",
        "PyInstaller",
        "--clean",
        str(spec_file),
    ]

    print(f"\nRunning: {' '.join(cmd)}\n")
    result = subprocess.run(cmd, cwd=str(repo_root))

    if result.returncode != 0:
        print("\nBuild FAILED.", file=sys.stderr)
        sys.exit(result.returncode)

    exe_path = repo_root / "dist" / "desktop_recorder"
    if sys.platform == "win32":
        exe_path = exe_path.with_suffix(".exe")

    print("\n" + "=" * 60)
    if exe_path.exists():
        size_mb = exe_path.stat().st_size / (1024 * 1024)
        print(f"Build SUCCEEDED -> {exe_path}  ({size_mb:.1f} MB)")
    else:
        print(f"Build completed. Look for the executable in: {repo_root / 'dist'}")
    print("=" * 60)

    print(
        "\nQuick-start:\n"
        "  Record a session : ./dist/desktop_recorder record -o my_session.json\n"
        "  Play it back     : ./dist/desktop_recorder play   -i my_session.json\n"
        "  Inspect it       : ./dist/desktop_recorder list   -i my_session.json\n"
    )


if __name__ == "__main__":
    main()
