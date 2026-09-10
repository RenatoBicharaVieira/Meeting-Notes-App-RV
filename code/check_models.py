"""Offline model smoke tests with synthetic silence; not an accuracy benchmark."""
import argparse
import os
from local_runtime import ROOT, configure

configure()
os.environ['HF_HUB_OFFLINE'] = '1'


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('model', choices=['transcription', 'diarization'])
    args = parser.parse_args()
    if args.model == 'transcription':
        import numpy as np
        from faster_whisper import WhisperModel
        model = WhisperModel(
            str(ROOT / 'data/models/faster-whisper-large-v3'),
            device='cuda', compute_type='float16', local_files_only=True,
        )
        segments, _ = model.transcribe(
            np.zeros(16000, dtype=np.float32), language='en',
            beam_size=1, vad_filter=False,
        )
        list(segments)
        print('Whisper large-v3 offline GPU inference passed (synthetic silence).')
    else:
        import torch
        from pyannote.audio import Pipeline
        pipeline = Pipeline.from_pretrained(str(ROOT / 'data/models/community-1'))
        pipeline.to(torch.device('cuda'))
        pipeline({'waveform': torch.zeros(1, 160000), 'sample_rate': 16000})
        print('Community-1 offline GPU inference passed (synthetic silence).')


if __name__ == '__main__':
    main()
