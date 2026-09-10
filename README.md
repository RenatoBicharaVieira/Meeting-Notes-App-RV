# Meeting-Notes-App-RV

A planned free, local Windows application for recording online meetings, transcribing and distinguishing speakers after recording, renaming speakers, and exporting timestamped plain text.

Status: requirements and repository foundation. No application has been implemented yet.

- [Project overview](docs/ProjectOverview.md)
- [Decision history](docs/Decisions.md)
- [Development tasks](docs/TODO.md)
- [Future ideas](docs/FutureIdeas.md)

## Repository structure

- `code/`: application source and relevant tests.
- `docs/`: maintained requirements, rationale, progress, and deferred ideas.
- `data/`: ignored local runtime assets and working data; never commit meeting recordings, transcripts, model weights, or credentials.

The intended release is a portable ZIP containing an executable, dependencies, and models. Recipients should not need an installer, Python, an account, or extra downloads. GPU acceleration requires a compatible installed driver; CPU fallback is planned.

No remote repository has been created or published. A source license will be selected before public release, and bundled dependency/model licenses will be reviewed separately.
