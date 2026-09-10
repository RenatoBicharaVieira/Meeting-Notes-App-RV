# Application source

Application implementation will live here. Environment setup helpers and pinned dependencies are now available; see `../docs/StackSetup.md` for usage and validation limits.

## Application

- `app.py`: single-window UI and worker lifecycle.
- `recorder.py`: two audio capture streams, bounded queues, incremental mono WAV writing.
- `transcribe_worker.py`: offline transcription and full-meeting speaker clustering in a separate process.
- `meeting_data.py`: temporary sessions, safe cleanup, atomic plain-text export.
- `launcher.py`: executable launcher for bundled Python or the development environment.
- `build_portable.py`: portable runtime/model assembly and optional ZIP.
- `tests/`: focused synthetic tests; run `.venv/Scripts/python.exe -m pytest code/tests -q` from the repository root.

Development launch: `.venv/Scripts/pythonw.exe code/app.py`. Build: `.venv/Scripts/python.exe code/build_portable.py --zip`. The build downloads Python's embedded runtime and uses the locally installed dependencies/models. It excludes developer authentication caches.

- `requirements.txt`: pinned direct dependencies.
- `requirements-win-gpu.lock.txt`: full installed GPU environment snapshot.
- `local_runtime.py`: project-local library paths and telemetry settings.
- `check_stack.py`: synthetic environment checks; does not record audio.
- `download_models.py`: model acquisition into ignored data.
- `login_huggingface.py`: developer-only hidden-token sign-in.
- `check_models.py`: offline synthetic GPU model checks, not accuracy benchmarks.
