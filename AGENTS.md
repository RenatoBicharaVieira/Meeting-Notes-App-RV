# Development conventions

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
