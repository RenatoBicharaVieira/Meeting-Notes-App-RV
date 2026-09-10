"""Small executable entry point for source and portable distributions."""
import ctypes
import os
from pathlib import Path
import subprocess
import sys


def main():
    root = Path(sys.executable).parent if getattr(sys, 'frozen', False) else Path(__file__).resolve().parents[1]
    python = root / 'runtime/pythonw.exe'
    if not python.exists():
        python = root / '.venv/Scripts/pythonw.exe'
    script = root / 'code/app.py'
    if not python.exists() or not script.exists():
        ctypes.windll.user32.MessageBoxW(None, 'Extract the entire app folder before launching. The Python runtime or app files are missing.', 'Meeting-Notes-App-RV', 0x10)
        return 1
    env = os.environ.copy()
    env['MEETING_NOTES_ROOT'] = str(root)
    env['PYTHONUTF8'] = '1'
    env.pop('PYTHONHOME', None)
    env.pop('PYTHONPATH', None)
    if getattr(sys, 'frozen', False):
        ctypes.windll.kernel32.SetDllDirectoryW(None)
    subprocess.Popen([str(python), str(script)], cwd=root, env=env, creationflags=subprocess.CREATE_NO_WINDOW)
    return 0


if __name__ == '__main__':
    sys.exit(main())
