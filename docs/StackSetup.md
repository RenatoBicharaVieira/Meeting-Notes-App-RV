# Stack setup

Last updated: 2026-09-10. Developer setup is complete; remaining work is application evaluation and release validation, not initial dependency installation.

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
- The same checks subsequently passed with the bundled embedded Python runtime, including offline GPU inference for both models. The portable window rendered successfully, and the final ZIP passed source-parity, required-file, exclusion, duplicate-entry, and CRC checks.
- Twelve focused application tests and a generated-silence worker run passed. No actual meeting/microphone capture, Portuguese/English accuracy benchmark, real-speech speaker separation test, long-duration trial, or clean other-PC validation has run. Silence smoke tests validate loading/execution, not accuracy or speaker clustering quality.

### Installed application baseline

| Component | Installed version / artifact |
| --- | --- |
| Python development and embedded runtime | 3.11.9 x64 |
| PySide6 | 6.11.2 |
| PyAudioWPatch | 0.2.12.8 |
| faster-whisper / CTranslate2 | 1.2.1 / 4.8.2 |
| pyannote.audio | 4.0.7 |
| torch / torchaudio | 2.11.0+cu128 / 2.11.0+cu128 |
| TorchCodec | 0.16.0 |
| FFmpeg | BtbN 8.1 LGPL shared build, digest recorded above |
| pytest / PyInstaller | 9.1.1 / 6.22.2 |

The full dependency snapshot is [requirements-win-gpu.lock.txt](../code/requirements-win-gpu.lock.txt). The recorder uses Python 3.11's `audioop`; it is deprecated and removed in Python 3.13, so the application cannot simply be moved to the separately installed 3.13 runtime without a recording-code change.

### Using the environment

Run these from the repository root in PowerShell. Activation is optional; using the explicit interpreter avoids PATH and execution-policy issues.

```powershell
.venv/Scripts/python.exe -m pip check
.venv/Scripts/python.exe code/check_stack.py
.venv/Scripts/python.exe code/check_models.py transcription
.venv/Scripts/python.exe code/check_models.py diarization
.venv/Scripts/python.exe -m pytest code/tests -q
.venv/Scripts/python.exe code/smoke_worker.py
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

This does not provision FFmpeg or models. FFmpeg was obtained from the BtbN provider linked by https://ffmpeg.org/download.html, asset `ffmpeg-n8.1-latest-win64-lgpl-shared-8.1.zip`. Its moving release URL may change; verify the recorded digest or explicitly review and record a newer artifact. Model downloads resolve the current upstream revision and record it in local manifests; the exact existing revisions are recorded above, but the downloader does not yet enforce those revisions on a fresh download. External-asset reproducibility and required notices/source offers remain release work.

For a new developer checkout after authentication and FFmpeg provisioning:

```powershell
.venv/Scripts/python.exe code/download_models.py transcription
.venv/Scripts/python.exe code/download_models.py diarization
```

### Launching and packaging the implemented app

```powershell
.venv/Scripts/pythonw.exe code/app.py
.venv/Scripts/python.exe code/build_portable.py --zip
.venv/Scripts/python.exe code/check_release.py
```

The builder creates a small PyInstaller launcher, downloads/caches the official Python 3.11.9 embedded ZIP, copies the installed package directories and selected application modules, and bundles only the selected models and FFmpeg directory from data. It does not copy the developer Hugging Face cache. The embedded archive's SHA256 is recorded in `BUILD.json`; the script currently calculates it rather than checking it against a preselected trusted expected digest.

Use a fresh release destination. The builder merges files into an existing folder and does not remove stale files. It refuses recognized runtime user data when zipping. `--zip-only` is available for a clean, already assembled folder; it does not copy changed source files first, so `check_release.py` must pass afterward.

Delivered local preview: `dist/Meeting-Notes-App-RV/Meeting-Notes-App-RV.exe` and `dist/Meeting-Notes-App-RV-windows-x64.zip` (5.91 GiB compressed; approximately 8.38 GiB extracted). No public binary release is published. The current documentation refresh does not rebuild those artifacts; their bundled `.txt` guide/notices remain the original build snapshots.

### References

- https://github.com/SYSTRAN/faster-whisper
- https://github.com/pyannote/pyannote-audio
- https://github.com/pytorch/torchcodec (torch/torchcodec compatibility and FFmpeg shared-library requirement)
- https://download.pytorch.org/whl/cu128
- https://ffmpeg.org/download.html

## Historical preflight notes

### Correction — existing Python installations confirmed

The initial inspection ran under a restricted account with a different command path. A follow-up in the user's Windows account confirmed:

- Python 3.13.14, 64-bit: `C:/Users/renat/AppData/Local/Programs/Python/Python313/python.exe`.
- Existing `C:/Users/renat/AppData/Local/Microsoft/WindowsApps/python3.11.exe` successfully reports Python 3.11.9.

The existing Python 3.11 installation was then used successfully to create `.venv`. No new development Python installation was needed. A separate embedded runtime was later downloaded for the portable package. The earlier command-discovery results describe the restricted session only, not the user's installed software.

### 2026-09-10 — Initial machine inspection

Read-only inspection completed before installing dependencies.

- NVIDIA GPU detected: GeForce RTX 4070, 12,282 MiB reported VRAM.
- NVIDIA driver: 616.92; nvidia-smi reports CUDA UMD 13.4. This is driver capability information, not proof that CUDA runtime libraries or the CUDA toolkit are installed.
- Free space at inspection: approximately 267 GiB on C: and 336 GiB on D:.
- `python`, `py`, `pip`, `uv`, and `nvcc` were not found in the current shell command path.
- No Python installation was found in the checked standard locations (`AppData/Local/Programs/Python` and `Program Files/Python311`). This is not an exhaustive search of the PC.
- Windows system-management queries were denied in the restricted session; CPU and RAM remain user-reported (Ryzen 7800X3D, 32 GB). No need to broaden privileges solely to verify these.
- Git repository was clean and synchronized before the inspection.

### Original proposal — subsequently implemented

The original proposal was Python 3.11, PySide6, PyAudioWPatch, faster-whisper/CTranslate2, pyannote.audio/PyTorch, and pytest in an isolated environment. Dependency resolution and installation are complete. Packaging evolved into a thin launcher plus embedded Python rather than freezing the entire AI stack. The current-state sections above supersede this proposal.

### Original setup sequence — completed

1. Reused existing Python 3.11 to create the project environment.
2. Resolved and pinned compatible Windows wheels and GPU runtimes.
3. Checked imports, UI initialization, device enumeration, and GPU execution.
4. Acquired both models into ignored data; completed Community-1 authentication locally.
5. Verified local model execution with synthetic audio. Real-speech performance and compatibility on other PCs remain in [TODO](TODO.md).

At the initial inspection, no packages or models had been installed and no inference had been tested. See the current-state section above for subsequent setup results.
