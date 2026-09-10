# Third-party components — development preview

Last updated: 2026-09-10. Status: inventory maintained from the setup/build work; no new license determination or completed redistribution audit in this documentation pass.

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

## Current distribution state

The source repository is already public under RenatoBicharaVieira/Meeting-Notes-App-RV. It does not yet contain a project-level LICENSE file; public visibility alone is not a source-license selection. The 5.91 GiB ZIP is a local development preview and has not been uploaded as a public binary release.

The build copies complete installed package directories, including development tools and transitive dependencies. The list above summarizes major components rather than every bundled license. Preserve and audit their metadata/notices before distributing a public binary; confirm the exact Qt modules and FFmpeg/NVIDIA artifacts, not only top-level package names.

The current model snapshots are Whisper `edaa852ec7e145841d8ffdb056a99866b5f0a478` and Community-1 `3533c8cf8e369892e6b79ff1bf80f7b0286a54ee`. Artifact sources and FFmpeg digest are recorded in [StackSetup](StackSetup.md). Download access conditions and redistribution permissions are separate questions; the developer's completed account sign-in is not the final distribution review.

`docs/UserGuide.md` and this document are copied into a build as `README.txt` and `THIRD-PARTY-NOTICES.txt`. Updating repository Markdown does not update an existing ZIP; rebuild those snapshots during the next packaging milestone. Outstanding release work is tracked in [TODO](TODO.md).
