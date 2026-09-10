"""Download pinned snapshots into ignored local storage; never log credentials."""
import argparse
import json
from local_runtime import ROOT, configure

configure()
from huggingface_hub import HfApi, snapshot_download
from huggingface_hub.errors import GatedRepoError

MODELS = {
    'transcription': ('Systran/faster-whisper-large-v3', 'faster-whisper-large-v3'),
    'diarization': ('pyannote/speaker-diarization-community-1', 'community-1'),
}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('model', choices=MODELS)
    args = parser.parse_args()
    repo, folder = MODELS[args.model]
    destination = ROOT / 'data' / 'models' / folder
    revision = HfApi().model_info(repo).sha
    snapshot_download(repo, revision=revision, local_dir=destination)
    (destination / 'download-manifest.json').write_text(
        json.dumps({'repository': repo, 'revision': revision}, indent=2), encoding='utf-8'
    )
    print(f'Download complete: {folder}; revision {revision}')


if __name__ == '__main__':
    try:
        main()
    except GatedRepoError:
        print('Model access required: accept Community-1 conditions and run code/login_huggingface.py locally.')
        raise SystemExit(2)
