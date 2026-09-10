# Third-party components — development preview

The portable folder includes unmodified Python package directories and their installed metadata/license files under runtime/Lib/site-packages. Python's license is included with its embedded distribution. This inventory is not a completed public redistribution compliance review; distribution of this preview to others remains pending the project source-license decision and final notices/source-offer audit.

- Python 3.11.9: Python Software Foundation license. https://www.python.org/downloads/release/python-3119/
- PySide6/Qt: LGPLv3/GPLv3 and component-specific terms. Use the LGPL-compatible components; retain notices and replacement/relinking rights. https://doc.qt.io/qtforpython-6/licenses.html
- PyAudioWPatch: MIT. https://github.com/s0d3s/PyAudioWPatch
- faster-whisper and CTranslate2: MIT. https://github.com/SYSTRAN/faster-whisper and https://github.com/OpenNMT/CTranslate2
- Systran faster-whisper-large-v3 model: upstream repository declares MIT. https://huggingface.co/Systran/faster-whisper-large-v3
- pyannote.audio: MIT. https://github.com/pyannote/pyannote-audio
- pyannote Community-1 weights: CC BY 4.0. Attribution: pyannote team, speaker-diarization-community-1. https://huggingface.co/pyannote/speaker-diarization-community-1 ; https://creativecommons.org/licenses/by/4.0/ . Weights are included without modification; local download metadata is added.
- PyTorch, torchaudio, TorchCodec and their bundled libraries: see installed license notices. https://pytorch.org/
- NVIDIA CUDA/cuDNN libraries bundled by PyTorch: NVIDIA license terms apply. No system NVIDIA driver is bundled. https://docs.nvidia.com/cuda/eula/index.html
- FFmpeg shared LGPL build from BtbN: retain bundled licenses and review corresponding-source obligations before public distribution. https://github.com/BtbN/FFmpeg-Builds ; https://ffmpeg.org/legal.html
- PyInstaller launcher: GPL with the bootloader distribution exception. https://pyinstaller.org/en/stable/license.html

Exact Python package versions: code/requirements-win-gpu.lock.txt in the source repository. No meeting recordings, credentials, Hugging Face token cache, or account information are intentionally bundled.
