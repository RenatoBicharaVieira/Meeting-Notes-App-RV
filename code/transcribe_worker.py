"""Offline worker process. Streams status to the UI; writes session-only results."""
import gc
import json
import os
import sys
import wave
from pathlib import Path
from local_runtime import ROOT, configure

configure()
os.environ['HF_HUB_OFFLINE'] = '1'
os.environ['HF_HUB_DISABLE_IMPLICIT_TOKEN'] = '1'


def report(message):
    print(json.dumps({'status': message}), flush=True)


def read_chunks(path, seconds=300):
    import numpy as np
    with wave.open(str(path), 'rb') as source:
        offset = 0
        while data := source.readframes(16000 * seconds):
            yield offset, np.frombuffer(data, dtype='<i2').astype(np.float32) / 32768
            offset += len(data) / 2 / 16000


def assign_words(words, turns):
    """Use word/turn overlap; leave unsupported words explicitly unknown."""
    result = []
    cursor = 0
    for word in words:
        start, end = word['start'], word['end']
        while cursor < len(turns) and turns[cursor][1] <= start:
            cursor += 1
        best, speaker = 0, 'speaker_unknown'
        for index in range(cursor, len(turns)):
            left, right, label = turns[index]
            if left >= end:
                break
            overlap = max(0, min(end, right) - max(start, left))
            if overlap > best:
                best, speaker = overlap, label
        if result and result[-1]['speaker'] == speaker and start - result[-1]['end'] < 1.5:
            result[-1]['text'] += word['text']
            result[-1]['end'] = end
        else:
            result.append({'start': start, 'end': end, 'speaker': speaker, 'text': word['text']})
    return result


def run(folder, language):
    import numpy as np
    import torch
    from faster_whisper import WhisperModel
    from meeting_data import save_json
    device = 'cuda' if torch.cuda.is_available() else 'cpu'
    report(f'Loading transcription model ({"GPU" if device == "cuda" else "CPU"})…')
    model = WhisperModel(str(ROOT / 'data/models/faster-whisper-large-v3'),
        device=device, compute_type='float16' if device == 'cuda' else 'int8', local_files_only=True)
    mic, remote = [], []
    for name, target in [('microphone', mic), ('system', remote)]:
        for offset, samples in read_chunks(folder / f'{name}.wav'):
            report(f'Transcribing {name}: {int(offset // 60)} minutes processed…')
            segments, _ = model.transcribe(samples, language=language, task='transcribe',
                word_timestamps=True, vad_filter=True, condition_on_previous_text=False)
            for segment in segments:
                for word in segment.words or []:
                    target.append({'start': offset + word.start, 'end': offset + word.end, 'text': word.word})
    del model
    gc.collect()
    if device == 'cuda':
        torch.cuda.empty_cache()
    result = assign_words(mic, [(0, float('inf'), 'me')])
    if remote:
        report('Identifying speakers across the meeting…')
        from pyannote.audio import Pipeline
        pipeline = Pipeline.from_pretrained(str(ROOT / 'data/models/community-1'))
        pipeline.to(torch.device(device))
        # Full timeline clustering preserves speaker identities across chunk boundaries.
        # Audio memory is bounded by the supported four-hour limit (~922 MB float32).
        with wave.open(str(folder / 'system.wav'), 'rb') as source:
            if source.getnframes() > 16000 * 4 * 3600 + 16000:
                raise ValueError('This version supports recordings up to four hours.')
            samples = np.frombuffer(source.readframes(source.getnframes()), dtype='<i2').astype(np.float32) / 32768
        output = pipeline({'waveform': torch.from_numpy(samples).unsqueeze(0), 'sample_rate': 16000}, max_speakers=6)
        annotation = output.exclusive_speaker_diarization
        mapping, turns = {}, []
        for turn, _, label in annotation.itertracks(yield_label=True):
            if label not in mapping:
                mapping[label] = f'speaker_{len(mapping) + 1}'
            turns.append((turn.start, turn.end, mapping[label]))
        result.extend(assign_words(remote, turns))
    result.sort(key=lambda item: item['start'])
    save_json(folder / 'transcript.json', result)
    report('Finished')


if __name__ == '__main__':
    try:
        run(Path(sys.argv[1]), sys.argv[2])
    except Exception as exc:
        print(json.dumps({'error': str(exc)}), flush=True)
        sys.exit(1)
