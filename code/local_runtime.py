"""Configure project-local libraries without changing the system environment."""
import os
import sys
from pathlib import Path

ROOT = Path(os.environ.get('MEETING_NOTES_ROOT', Path(__file__).resolve().parents[1]))
_dll_handles = []


def configure():
    os.environ['PYANNOTE_METRICS_ENABLED'] = '0'
    os.environ['HF_HUB_DISABLE_TELEMETRY'] = '1'
    os.environ.setdefault('HF_HOME', str(ROOT / 'data' / 'huggingface'))
    paths = [Path(sys.prefix) / 'Lib' / 'site-packages' / 'torch' / 'lib']
    paths.extend((ROOT / 'data' / 'runtime' / 'ffmpeg').glob('*/bin'))
    for path in paths:
        if path.is_dir():
            os.environ['PATH'] = str(path) + os.pathsep + os.environ.get('PATH', '')
            if os.name == 'nt':
                _dll_handles.append(os.add_dll_directory(str(path)))
