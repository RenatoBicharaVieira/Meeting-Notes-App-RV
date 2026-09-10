# Stack setup

## Current state — 2026-09-10

- Created `.venv` using the existing Python 3.11.9 installation.
- Installed pinned direct dependencies from `code/requirements.txt`; full resolved versions are in `code/requirements-win-gpu.lock.txt`.
- PyTorch and torchaudio are both 2.11.0+cu128, installed from the official CUDA 12.8 wheel index. An unconstrained resolution selected different torch/torchaudio release numbers; pinning avoids that mismatch.
- Installed a project-local BtbN FFmpeg 8.1 LGPL shared build under ignored `data/runtime/ffmpeg`. ZIP SHA256: `79198851def8e61310eabd259225561472bb7ea6e5a7af488bf094a61f2ee615`, checked against the GitHub asset digest. This is a developer dependency, not a completed redistribution review.
- Downloaded `Systran/faster-whisper-large-v3`, revision `edaa852ec7e145841d8ffdb056a99866b5f0a478`, into `data/models/faster-whisper-large-v3`.
- Downloaded Community-1 revision `3533c8cf8e369892e6b79ff1bf80f7b0286a54ee` into `data/models/community-1` after the user accepted access conditions and authenticated locally. Earlier unauthenticated attempts received HTTP 401; access is now resolved.

### Validation performed

- `pip check`: no broken requirements.
- Imports: PySide6, PyAudioWPatch, faster-whisper, CTranslate2, pyannote.audio, torch, torchaudio, and TorchCodec.
- GPU tensor computation passed on RTX 4070; CTranslate2 detected one CUDA device.
- Qt widget initialization passed without displaying a window.
- Device enumeration found 22 audio devices, including 3 loopback devices; no capture streams were opened.
- TorchCodec decoded a generated one-second WAV correctly.
- Whisper large-v3 loaded locally and ran GPU inference on synthetic silence with Hugging Face offline mode enabled.
- Community-1 loaded from its local folder and completed GPU inference on ten seconds of synthetic silence with Hugging Face offline mode enabled. Non-fatal upstream warnings concerned unavailable Triton FLOP counting and TF32 being disabled for reproducibility; inference succeeded.
- No actual meeting/microphone recording, Portuguese/English accuracy benchmark, real-speech speaker separation test, Windows 10 validation, or portable-package test has run yet. Silence smoke tests validate loading/execution, not accuracy or speaker clustering quality.

### Using the environment

Run these from the repository root in PowerShell. Activation is optional; using the explicit interpreter avoids PATH and execution-policy issues.

```powershell
.venv/Scripts/python.exe -m pip check
.venv/Scripts/python.exe code/check_stack.py
.venv/Scripts/python.exe code/check_models.py transcription
```

For future developer setup, accept access conditions at https://huggingface.co/pyannote/speaker-diarization-community-1 and create a Read token at https://huggingface.co/settings/tokens. Enter it only in the hidden local prompt (already completed on the development PC):

```powershell
.venv/Scripts/python.exe code/login_huggingface.py
.venv/Scripts/python.exe code/download_models.py diarization
.venv/Scripts/python.exe code/check_models.py diarization
```

The developer token is stored in ignored `data/huggingface`, not Git or command-line arguments. Never distribute that folder. `code/local_runtime.py` disables Hugging Face and pyannote telemetry and registers project-local FFmpeg/PyTorch DLL directories for the current process only. Global PATH is unchanged.

### Recreating the Python dependency environment

```powershell
& "$env:LOCALAPPDATA/Microsoft/WindowsApps/python3.11.exe" -m venv .venv
.venv/Scripts/python.exe -m pip install --upgrade pip
.venv/Scripts/python.exe -m pip install torch==2.11.0 torchaudio==2.11.0 --index-url https://download.pytorch.org/whl/cu128
.venv/Scripts/python.exe -m pip install -r code/requirements-win-gpu.lock.txt --extra-index-url https://download.pytorch.org/whl/cu128
```

This does not provision FFmpeg or models. FFmpeg was obtained from the BtbN provider linked by https://ffmpeg.org/download.html, asset `ffmpeg-n8.1-latest-win64-lgpl-shared-8.1.zip`. Its moving release URL may change; verify the recorded digest or explicitly review and record a newer artifact. Model downloads record upstream revisions in local manifests. Release packaging must pin all external artifacts and include the required notices and source offers before distribution.

### References

- https://github.com/SYSTRAN/faster-whisper
- https://github.com/pyannote/pyannote-audio
- https://github.com/pytorch/torchcodec (torch/torchcodec compatibility and FFmpeg shared-library requirement)
- https://download.pytorch.org/whl/cu128
- https://ffmpeg.org/download.html

## Historical preflight notes

## Correction — existing Python installations confirmed

The initial inspection ran under a restricted account with a different command path. A follow-up in the user's Windows account confirmed:

- Python 3.13.14, 64-bit: `C:/Users/renat/AppData/Local/Programs/Python/Python313/python.exe`.
- Existing `C:/Users/renat/AppData/Local/Microsoft/WindowsApps/python3.11.exe` successfully reports Python 3.11.9.

Use the existing Python 3.11 installation to create the project environment, subject to environment creation and dependency validation. No new base Python download is needed. The earlier command-discovery results describe the restricted session only, not the user's installed software.

## 2026-09-10 — Initial machine inspection

Read-only inspection completed before installing dependencies.

- NVIDIA GPU detected: GeForce RTX 4070, 12,282 MiB reported VRAM.
- NVIDIA driver: 616.92; nvidia-smi reports CUDA UMD 13.4. This is driver capability information, not proof that CUDA runtime libraries or the CUDA toolkit are installed.
- Free space at inspection: approximately 267 GiB on C: and 336 GiB on D:.
- `python`, `py`, `pip`, `uv`, and `nvcc` were not found in the current shell command path.
- No Python installation was found in the checked standard locations (`AppData/Local/Programs/Python` and `Program Files/Python311`). This is not an exhaustive search of the PC.
- Windows system-management queries were denied in the restricted session; CPU and RAM remain user-reported (Ryzen 7800X3D, 32 GB). No need to broaden privileges solely to verify these.
- Git repository was clean and synchronized before the inspection.

## Proposed baseline, pending dependency resolution

Python 3.11 x64 in an isolated project environment; PySide6; PyAudioWPatch; faster-whisper/CTranslate2; pyannote.audio/PyTorch; pytest. Evaluate PyInstaller folder packaging later. Resolve exact compatible versions and GPU libraries before installation; do not interpret this proposal as a tested package set.

## Next setup steps

1. Use the confirmed existing Python 3.11 installation to create an isolated project environment without modifying system Python or global PATH.
2. Resolve and pin compatible Windows wheels, including AI runtimes and decoding dependencies.
3. Validate imports, UI initialization, audio device enumeration, and GPU execution before downloading large models.
4. Acquire model artifacts into ignored local data; obtain Community-1 access without putting tokens into source or logs.
5. Validate local model loading and short audio processing. Record performance and remaining compatibility gaps.

At the initial inspection, no packages or models had been installed and no inference had been tested. See the current-state section above for subsequent setup results.
