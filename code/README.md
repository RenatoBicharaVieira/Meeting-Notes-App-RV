# Application source

Application implementation will live here. Environment setup helpers and pinned dependencies are now available; see `../docs/StackSetup.md` for usage and validation limits.

- `requirements.txt`: pinned direct dependencies.
- `requirements-win-gpu.lock.txt`: full installed GPU environment snapshot.
- `local_runtime.py`: project-local library paths and telemetry settings.
- `check_stack.py`: synthetic environment checks; does not record audio.
- `download_models.py`: model acquisition into ignored data.
- `login_huggingface.py`: developer-only hidden-token sign-in.
- `check_models.py`: offline synthetic GPU model checks, not accuracy benchmarks.
