# Development conventions

Last reviewed: 2026-09-10, following portable preview build `972b785`.

Keep this repository as a durable record of the product requirements and the reasoning behind implementation decisions.

- Read `docs/ProjectOverview.md`, `docs/Decisions.md`, and `docs/TODO.md` before substantive work.
- Keep application code under `code/` and development documentation under `docs/`.
- Update relevant documentation in the same milestone as code changes. Record rationale, material tradeoffs, validation results, and unresolved limitations; distinguish proposed choices from verified behavior.
- Add dated decisions to `docs/Decisions.md`; preserve history and explicitly supersede decisions when requirements change.
- Maintain `docs/TODO.md` as the current progress record. Put optional scope in `docs/FutureIdeas.md`.
- Commit completed, coherent milestones with descriptive messages. Do not commit unrelated changes or claim validation that did not run.
- Never commit meeting data, model weights, credentials, generated packages, or personal identifiers from recordings.
- Preserve the minimal agreed interface. Do not implement deferred features without user direction.
- Public publishing and remote creation are separate from local commits; do not infer a remote destination.

## Current handoff

The first preview is implemented. The configured public source remote is `RenatoBicharaVieira/Meeting-Notes-App-RV`, branch `main`; continuing authorized development commits uses that existing remote. No public binary release has been uploaded. Source-license selection remains unresolved.

Read `docs/Implementation.md` and `docs/StackSetup.md` before changing the pipeline or packaging. Preserve the distinction between implemented behavior, synthetic verification, and real-device/real-speech validation. The current evidence is 12 focused tests, offline GPU model checks, and portable ZIP verification on the development PC; do not describe these as a completed meeting-quality or cross-PC evaluation.

Repository Markdown maintenance covers tracked project documents, not third-party Markdown inside ignored environments, model downloads, or built archives. Keep historical decisions recognizable as history and link current-state documents. A documentation-only pass does not rebuild the already delivered ZIP; its bundled README/notices are snapshots until the next packaging run.
