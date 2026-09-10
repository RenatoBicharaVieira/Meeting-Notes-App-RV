"""Small session store and plain-text export; no meeting history."""
import json
import os
import shutil
import stat
import tempfile
import uuid
from pathlib import Path


def new_session(root):
    root = Path(root)
    root.mkdir(parents=True, exist_ok=True)
    path = root / ('meeting-' + uuid.uuid4().hex)
    path.mkdir()
    (path / '.meeting-session').write_text('Meeting-Notes-App-RV', encoding='utf-8')
    return path


def delete_session(root, path):
    root, path = Path(root).resolve(), Path(path)
    if path.resolve().parent != root or not path.name.startswith('meeting-'):
        raise ValueError('Refusing to delete a folder outside meeting storage.')
    if not (path / '.meeting-session').is_file():
        raise ValueError('Unrecognized meeting folder.')
    for entry in [path, *path.rglob('*')]:
        if getattr(entry.lstat(), 'st_file_attributes', 0) & stat.FILE_ATTRIBUTE_REPARSE_POINT:
            raise ValueError('Refusing to follow a linked folder during cleanup.')
    shutil.rmtree(path)


def clean_stale(root):
    root = Path(root)
    if root.exists():
        for path in root.glob('meeting-*'):
            if path.is_dir() and (path / '.meeting-session').is_file():
                delete_session(root, path)


def timestamp(seconds):
    seconds = max(0, int(seconds))
    return f'{seconds // 3600:02}:{seconds // 60 % 60:02}:{seconds % 60:02}'


def export_text(destination, segments, names, language, session_root):
    destination = Path(destination).resolve()
    if destination.is_relative_to(Path(session_root).resolve()):
        raise ValueError('Choose an export location outside temporary meeting storage.')
    lines = ['Meeting-Notes-App-RV', f'Language: {language}', '']
    for item in segments:
        name = names.get(item['speaker'], '').strip() or item['speaker']
        name = ' '.join(name.splitlines())
        lines.append(f"[{timestamp(item['start'])}] {name}: {item['text'].strip()}")
    handle, temporary = tempfile.mkstemp(prefix='.meeting-export-', suffix='.tmp', dir=destination.parent)
    try:
        with os.fdopen(handle, 'w', encoding='utf-8', newline='\n') as stream:
            stream.write('\n'.join(lines) + '\n')
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(temporary, destination)
    finally:
        if os.path.exists(temporary):
            os.unlink(temporary)


def save_json(path, value):
    Path(path).write_text(json.dumps(value, ensure_ascii=False, indent=2), encoding='utf-8')
