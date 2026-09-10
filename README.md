# Meeting-Notes-App-RV

A planned free, local Windows application for recording online meetings, transcribing and distinguishing speakers after recording, renaming speakers, and exporting timestamped plain text.

Status: development environment and both models installed; Whisper and Community-1 offline GPU inference verified with synthetic silence. Real-speech accuracy and the end-user application remain to be developed and validated.

- [Project overview](docs/ProjectOverview.md)
- [Decision history](docs/Decisions.md)
- [Development tasks](docs/TODO.md)
- [Future ideas](docs/FutureIdeas.md)
- [Stack setup and validation](docs/StackSetup.md)

## Repository structure

- `code/`: application source and relevant tests.
- `docs/`: maintained requirements, rationale, progress, and deferred ideas.
- `data/`: ignored local runtime assets and working data; never commit meeting recordings, transcripts, model weights, or credentials.

The intended release is a portable ZIP containing an executable, dependencies, and models. Recipients should not need an installer, Python, an account, or extra downloads. GPU acceleration requires a compatible installed driver; CPU fallback is planned.

Public repository: https://github.com/RenatoBicharaVieira/Meeting-Notes-App-RV (default branch: `main`). A source license will be selected before public release, and bundled dependency/model licenses will be reviewed separately.

