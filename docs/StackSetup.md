# Stack setup

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

No packages or models have been installed, no audio has been recorded, and no inference has been tested during this inspection.
