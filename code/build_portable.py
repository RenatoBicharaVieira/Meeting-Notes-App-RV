"""Build a self-contained Windows folder/ZIP. Explicit asset allowlists exclude secrets."""
import argparse
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import sys
import urllib.request
import zipfile

ROOT = Path(__file__).resolve().parents[1]


def zip_release(destination):
    for name in ('huggingface', 'sessions', 'preferences.json', 'app.lock'):
        if (destination / 'data' / name).exists():
            raise RuntimeError(f'Release contains runtime user data: {name}. Use a fresh release folder.')
    output = ROOT / 'dist/Meeting-Notes-App-RV-windows-x64.zip'
    print('Compressing portable ZIP…', flush=True)
    with zipfile.ZipFile(output, 'w', zipfile.ZIP_DEFLATED, compresslevel=1) as archive:
        for path in destination.rglob('*'):
            if path.is_file() and '__pycache__' not in path.parts:
                archive.write(path, path.relative_to(destination.parent))
    print(f'ZIP: {output}; {output.stat().st_size / 1024**3:.2f} GiB', flush=True)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--zip', action='store_true')
    parser.add_argument('--zip-only', action='store_true')
    args = parser.parse_args()
    if args.zip_only:
        zip_release(ROOT / 'dist/Meeting-Notes-App-RV')
        return
    build = ROOT / 'build'
    build.mkdir(exist_ok=True)
    subprocess.run([sys.executable, '-m', 'PyInstaller', '--noconfirm', '--clean', '--onefile',
        '--windowed', '--name', 'Meeting-Notes-App-RV', '--distpath', str(build / 'launcher'),
        '--workpath', str(build / 'pyinstaller'), '--specpath', str(build), str(ROOT / 'code/launcher.py')], check=True)
    embedded = build / 'python-3.11.9-embed-amd64.zip'
    if not embedded.exists():
        urllib.request.urlretrieve('https://www.python.org/ftp/python/3.11.9/python-3.11.9-embed-amd64.zip', embedded)
    destination = ROOT / 'dist/Meeting-Notes-App-RV'
    destination.mkdir(parents=True, exist_ok=True)
    runtime = destination / 'runtime'
    runtime.mkdir(exist_ok=True)
    with zipfile.ZipFile(embedded) as archive:
        archive.extractall(runtime)
    (runtime / 'python311._pth').write_text('python311.zip\n.\nLib/site-packages\n../code\nimport site\n', encoding='utf-8')
    print('Copying the Python packages…', flush=True)
    shutil.copytree(Path(sys.prefix) / 'Lib/site-packages', runtime / 'Lib/site-packages', dirs_exist_ok=True,
        ignore=shutil.ignore_patterns('__pycache__', '*.pyc'))
    appcode = destination / 'code'
    appcode.mkdir(exist_ok=True)
    for name in ('app.py', 'recorder.py', 'meeting_data.py', 'transcribe_worker.py', 'local_runtime.py'):
        shutil.copy2(ROOT / 'code' / name, appcode / name)
    shutil.copy2(build / 'launcher/Meeting-Notes-App-RV.exe', destination / 'Meeting-Notes-App-RV.exe')
    for model in ('faster-whisper-large-v3', 'community-1'):
        shutil.copytree(ROOT / 'data/models' / model, destination / 'data/models' / model,
            dirs_exist_ok=True, ignore=shutil.ignore_patterns('.cache'))
    shutil.copytree(ROOT / 'data/runtime/ffmpeg', destination / 'data/runtime/ffmpeg', dirs_exist_ok=True)
    shutil.copy2(ROOT / 'docs/UserGuide.md', destination / 'README.txt')
    shutil.copy2(ROOT / 'docs/ThirdParty.md', destination / 'THIRD-PARTY-NOTICES.txt')
    manifest = {'python_embed_sha256': hashlib.sha256(embedded.read_bytes()).hexdigest(),
                'python_embed_url': 'https://www.python.org/ftp/python/3.11.9/python-3.11.9-embed-amd64.zip'}
    (destination / 'BUILD.json').write_text(json.dumps(manifest, indent=2), encoding='utf-8')
    # Never package user-generated files or authentication data from a previously launched build.
    forbidden = [destination / 'data/huggingface', destination / 'data/sessions', destination / 'data/preferences.json']
    if any(path.exists() for path in forbidden):
        raise RuntimeError('Existing release folder contains runtime user data. Use a fresh build destination before zipping.')
    total = sum(path.stat().st_size for path in destination.rglob('*') if path.is_file())
    print(f'Portable folder: {destination}; {total / 1024**3:.2f} GiB', flush=True)
    if args.zip:
        zip_release(destination)


if __name__ == '__main__':
    main()
