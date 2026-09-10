# Meeting-Notes-App-RV

A planned free, local Windows application for recording online meetings, transcribing and distinguishing speakers after recording, renaming speakers, and exporting timestamped plain text.

Status: first application preview implemented and portable folder built. The minimal recording, transcription, speaker-renaming, plain-text export, and cleanup workflow is available. Twelve focused tests pass, and both models run offline in the bundled runtime. Real-meeting accuracy and other-PC validation remain pending.

- [Project overview](docs/ProjectOverview.md)
- [Decision history](docs/Decisions.md)
- [Development tasks](docs/TODO.md)
- [Future ideas](docs/FutureIdeas.md)
- [Stack setup and validation](docs/StackSetup.md)
- [User guide](docs/UserGuide.md)
- [Implementation and validation limits](docs/Implementation.md)

For the locally built preview, launch `dist/Meeting-Notes-App-RV/Meeting-Notes-App-RV.exe`. Release binaries and models are intentionally excluded from Git. The source development command is `.venv/Scripts/pythonw.exe code/app.py`.

## Repository structure

- `code/`: application source and relevant tests.
- `docs/`: maintained requirements, rationale, progress, and deferred ideas.
- `data/`: ignored local runtime assets and working data; never commit meeting recordings, transcripts, model weights, or credentials.

The intended release is a portable ZIP containing an executable, dependencies, and models. Recipients should not need an installer, Python, an account, or extra downloads. GPU acceleration requires a compatible installed driver; CPU fallback is planned.

Public repository: https://github.com/RenatoBicharaVieira/Meeting-Notes-App-RV (default branch: `main`). A source license will be selected before public release, and bundled dependency/model licenses will be reviewed separately.

