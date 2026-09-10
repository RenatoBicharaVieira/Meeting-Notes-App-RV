# Meeting-Notes-App-RV

A free, local Windows application for recording online meetings, transcribing and distinguishing speakers after recording, renaming speakers, and exporting timestamped plain text.

Last updated: 2026-09-10. Current milestone: portable development preview, implemented in `31cc2a0` and verified in `972b785`.

Status: first application preview implemented and portable folder built. The minimal recording, transcription, speaker-renaming, plain-text export, and cleanup workflow is available. Twelve focused tests pass, and both models run offline in the bundled runtime. Real-meeting accuracy and other-PC validation remain pending.

- [Project overview](docs/ProjectOverview.md)
- [Decision history](docs/Decisions.md)
- [Development tasks](docs/TODO.md)
- [Future ideas](docs/FutureIdeas.md)
- [Stack setup and validation](docs/StackSetup.md)
- [User guide](docs/UserGuide.md)
- [Implementation and validation limits](docs/Implementation.md)
- [Third-party inventory and release work](docs/ThirdParty.md)

For the locally built preview, launch `dist/Meeting-Notes-App-RV/Meeting-Notes-App-RV.exe`. Release binaries and models are intentionally excluded from Git. The source development command is `.venv/Scripts/pythonw.exe code/app.py`.

## Repository structure

- `code/`: application source and relevant tests.
- `docs/`: maintained requirements, rationale, progress, and deferred ideas.
- `data/`: ignored local runtime assets and working data; never commit meeting recordings, transcripts, model weights, or credentials.

The local preview ZIP contains an executable launcher, embedded Python, dependencies, and both models: **5.91 GiB compressed**, approximately **8.38 GiB extracted** before runtime caches. It is designed to work without installation, accounts, or further model downloads. Bundled-runtime checks passed on the development PC; a clean recipient PC still needs testing. GPU acceleration requires a compatible installed driver. CPU fallback is implemented using the same large model, but CPU-only performance is not yet measured. There is one current package, not separate CPU/GPU editions.

Public source repository: [RenatoBicharaVieira/Meeting-Notes-App-RV](https://github.com/RenatoBicharaVieira/Meeting-Notes-App-RV), branch `main`. Source is already public; no project license has yet been selected and no binary release has been uploaded. The next work is known-recording evaluation, real capture/lifecycle checks, long-meeting and other-PC validation, and distribution review. Optional features remain outside scope.

