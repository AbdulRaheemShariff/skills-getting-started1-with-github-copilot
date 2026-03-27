# -*- mode: python ; coding: utf-8 -*-
"""
PyInstaller spec file for the Desktop Recorder tool.

Build with:
    pyinstaller desktop_recorder.spec
or simply:
    python build.py
"""

from PyInstaller.utils.hooks import collect_all

# Collect all data files, binaries, and hidden imports for packages that
# use dynamic or platform-specific backends that static analysis misses.
# This is the most reliable way to ensure pynput and pyautogui are fully
# bundled on every platform without manually tracking every sub-module.
_pynput_datas, _pynput_bins, _pynput_hidden = collect_all('pynput')
_pyautogui_datas, _pyautogui_bins, _pyautogui_hidden = collect_all('pyautogui')

block_cipher = None

a = Analysis(
    ['src/desktop_recorder.py'],
    pathex=['.'],
    binaries=[] + _pynput_bins + _pyautogui_bins,
    datas=[] + _pynput_datas + _pyautogui_datas,
    hiddenimports=[
        # pynput platform backends (one is picked at runtime based on OS)
        'pynput.keyboard._xorg',
        'pynput.mouse._xorg',
        'pynput.keyboard._win32',
        'pynput.mouse._win32',
        'pynput.keyboard._darwin',
        'pynput.mouse._darwin',
        'pynput._util',
        # PIL / Pillow
        'PIL._imaging',
        'PIL.Image',
        'PIL.ImageGrab',
        'PIL.BmpImagePlugin',
        'PIL.PngImagePlugin',
        'PIL.JpegImagePlugin',
        'PIL.GifImagePlugin',
        'PIL.IcoImagePlugin',
        # pyautogui platform backends (dynamically imported, missed by analysis)
        'pyautogui._pyautogui_win',
        'pyautogui._pyautogui_osx',
        'pyautogui._pyautogui_x11',
        # pyautogui runtime dependencies
        'pyscreeze',
        'mouseinfo',
        'pygetwindow',
        'pymsgbox',
        'pyperclip',
        'pytweening',
    ] + _pynput_hidden + _pyautogui_hidden,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='desktop_recorder',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    # UPX is disabled: it recompresses bundled DLLs in a way that Windows
    # loader cannot always verify, causing "missing prerequisites" crashes
    # on machines where the VC++ runtime or other DLLs aren't pre-installed.
    upx=False,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,   # CLI tool — keep the console window
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
