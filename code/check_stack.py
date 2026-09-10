"""Non-recording environment check using synthetic audio only."""
import os
import tempfile
import wave
from pathlib import Path
from local_runtime import configure

configure()
os.environ['QT_QPA_PLATFORM'] = 'offscreen'
import torch
import torchaudio
import ctranslate2
import faster_whisper
import pyannote.audio
import pyaudiowpatch as pyaudio
from PySide6.QtWidgets import QApplication, QWidget
from torchcodec.decoders import AudioDecoder

print('Torch:', torch.__version__, 'Torchaudio:', torchaudio.__version__)
print('CUDA available:', torch.cuda.is_available())
if torch.cuda.is_available():
    result = (torch.ones((32, 32), device='cuda') @ torch.ones((32, 32), device='cuda')).sum()
    assert result.item() == 32768
    print('GPU tensor computation passed:', torch.cuda.get_device_name(0))
print('CTranslate2 CUDA devices:', ctranslate2.get_cuda_device_count())
app = QApplication([])
window = QWidget()
print('Qt widget initialization passed')
window.close()
app.quit()
with pyaudio.PyAudio() as audio:
    print('Audio devices:', audio.get_device_count())
    print('Loopback devices:', len(list(audio.get_loopback_device_info_generator())))
with tempfile.TemporaryDirectory() as directory:
    path = Path(directory) / 'silence.wav'
    with wave.open(str(path), 'wb') as wav:
        wav.setnchannels(1)
        wav.setsampwidth(2)
        wav.setframerate(16000)
        wav.writeframes(b'\0\0' * 16000)
    decoded = AudioDecoder(str(path)).get_all_samples()
    assert decoded.data.shape[-1] == 16000
    print('TorchCodec synthetic WAV decoding passed')
print('Stack check passed; no microphone or system audio was recorded.')
