# Application source

Last updated: 2026-09-10.

This directory contains the first working application preview, setup helpers, build tools, and focused tests. See [Stack setup](../docs/StackSetup.md) for dependencies and [Implementation](../docs/Implementation.md) for behavior and validation limits.

## Application

- `app.py`: single-window UI and worker lifecycle.
- `recorder.py`: two audio capture streams, bounded queues, incremental mono WAV writing.
- `transcribe_worker.py`: offline transcription and full-meeting speaker clustering in a separate process.
- `meeting_data.py`: temporary sessions, safe cleanup, atomic plain-text export.
- `launcher.py`: executable launcher for bundled Python or the development environment.
- `build_portable.py`: portable runtime/model assembly and optional ZIP.
- `check_release.py`: verifies archive integrity, source parity, and data exclusions before delivery.
- `tests/`: focused synthetic tests; run `.venv/Scripts/python.exe -m pytest code/tests -q` from the repository root.

Development launch: `.venv/Scripts/pythonw.exe code/app.py`. Build: `.venv/Scripts/python.exe code/build_portable.py --zip`. The build downloads Python's embedded runtime and uses the locally installed dependencies/models. It excludes developer authentication caches.

Run commands from the repository root with the project interpreter. Use a fresh release destination: the builder copies into the existing folder rather than cleaning it, and refuses to ZIP recognized session/account data. For an already assembled clean folder, `code/build_portable.py --zip-only` compresses it without rebuilding. Run `code/check_release.py` afterward; it checks code parity and every ZIP file CRC. Build scripts are developer tools, not app controls.

## Environment and verification helpers

- `requirements.txt`: pinned direct dependencies.
- `requirements-win-gpu.lock.txt`: full installed GPU environment snapshot.
- `local_runtime.py`: project-local library paths and telemetry settings.
- `check_stack.py`: synthetic environment checks; does not record audio.
- `download_models.py`: model acquisition into ignored data.
- `login_huggingface.py`: developer-only hidden-token sign-in.
- `check_models.py`: offline synthetic GPU model checks, not accuracy benchmarks.
- `smoke_worker.py`: exercises the full worker/result handoff with temporary generated silence.
- `preview_ui.py`: renders the dark window using isolated temporary session storage; does not capture audio.

Twelve focused tests passed for the current preview. Model and portable checks also passed on the development GPU. No real-speech accuracy result, live capture result, or clean-PC certification is implied. Packaging includes only the five runtime application modules; developer login, build, and test helpers are not copied into the app's `code/` folder.
