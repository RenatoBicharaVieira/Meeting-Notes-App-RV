"""Verify archive integrity, source parity, and exclusion of developer/session data."""
from pathlib import Path
import zipfile

ROOT = Path(__file__).resolve().parents[1]
archive_path = ROOT / 'dist/Meeting-Notes-App-RV-windows-x64.zip'
prefix = 'Meeting-Notes-App-RV/'
with zipfile.ZipFile(archive_path) as archive:
    names = archive.namelist()
    assert len(names) == len(set(names)), 'Duplicate archive entries'
    for excluded in ('data/huggingface/', 'data/sessions/', 'data/preferences.json', 'data/app.lock'):
        assert not any(name.startswith(prefix + excluded) for name in names), excluded
    for source in ('app.py', 'recorder.py', 'meeting_data.py', 'transcribe_worker.py', 'local_runtime.py'):
        assert archive.read(prefix + 'code/' + source) == (ROOT / 'code' / source).read_bytes(), source
    for required in ('Meeting-Notes-App-RV.exe', 'runtime/python.exe', 'runtime/pythonw.exe',
                     'data/models/faster-whisper-large-v3/model.bin', 'data/models/community-1/config.yaml'):
        assert prefix + required in names, required
    print('Archive layout, code parity, and data exclusions passed. Checking all file CRCs…', flush=True)
    assert archive.testzip() is None, 'Archive checksum failure'
print(f'Portable ZIP verified: {archive_path.stat().st_size / 1024**3:.2f} GiB')
