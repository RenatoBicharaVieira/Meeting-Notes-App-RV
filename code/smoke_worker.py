"""Exercise worker process/result handoff with generated silence, without recording."""
import json
import subprocess
import sys
import tempfile
import wave
from pathlib import Path

with tempfile.TemporaryDirectory() as temporary:
    folder = Path(temporary)
    for name in ('microphone', 'system'):
        with wave.open(str(folder / f'{name}.wav'), 'wb') as output:
            output.setparams((1, 2, 16000, 0, 'NONE', 'not compressed'))
            output.writeframes(bytes(2 * 16000 * 2))
    worker = Path(__file__).resolve().parent / 'transcribe_worker.py'
    subprocess.run([sys.executable, str(worker), str(folder), 'pt'], check=True)
    result = json.loads((folder / 'transcript.json').read_text(encoding='utf-8'))
    assert result == [], 'Silent input should not produce transcript text.'
    print('Worker pipeline passed on generated silence; no live audio captured.')
