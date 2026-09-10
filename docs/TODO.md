# Development progress

Last updated: 2026-09-10

Current milestone: portable preview implemented in `31cc2a0`, archive verified in `972b785`. This list separates completed development from validation still needed; source publication is complete, public binary publication is not.

## Completed

- [x] Create Python 3.11 `.venv`, install and freeze GPU dependencies, and validate imports, GPU computation, device enumeration, and synthetic WAV decoding.
- [x] Download Whisper large-v3 and verify offline GPU inference using synthetic silence.
- [x] Inspect available Python commands, NVIDIA GPU/driver, and free disk space; record limitations in `StackSetup.md`.
- [x] Capture requirements, revised decisions, and exclusions.
- [x] Create repository structure and development conventions.
- [x] Exclude runtime data, models, credentials, and generated packages from version control.
- [x] Configure the public GitHub source repository and milestone commits.
- [x] Pin dependency versions and verify offline loading of both models on the development GPU.
- [x] Document user instructions, architecture, setup commands, and current limitations.
- [x] Measure the preview ZIP (5.91 GiB) and extracted folder (approximately 8.38 GiB).
- [x] Verify the finished archive's required assets, source parity, unique entries, data exclusions, and file CRCs.

## Implemented foundations

- [x] Finish Community-1 authenticated download and offline GPU smoke test (completed with synthetic silence; real-speech validation remains pending).
- [x] Specify and implement application states and enabled controls, including cancellation, repeated meetings, and deletion before export.
- [x] Implement guarded normal-exit cleanup, stale-session cleanup, and export preservation; real crash/hardware scenarios remain to be exercised.

## Implementation milestones

- [x] Recording service implemented with incremental files and timestamps; live device/shutdown stress validation pending.
- [x] Local transcription, diarization, and timestamp reconciliation worker implemented.
- [x] Minimal dark UI, microphone control, language selection, progress, and speaker renaming.
- [x] UTF-8 `.txt` export, export-error handling, and manual audio deletion.
- [x] Exit warnings and cleanup of meeting data without touching exports or models.
- [x] Local portable preview assembled with embedded Python, dependencies, models, and initial third-party notices; tokens excluded. Public redistribution audit remains pending.

## Next: evaluate the existing app

No additional interface features are scheduled. Use known recordings now that the first app exists.

- [ ] Select small licensed reference samples: AMI for English meetings; CORAA for Brazilian Portuguese transcription. Record sample IDs, source, reference annotations, and permitted usage before acquisition. Keep audio outside Git.
- [ ] Compare transcript words, speaker labels, and timestamps against reference material; report transcription errors and speaker-attribution errors separately.
- [ ] Test playback capture plus microphone using headphones, including minimization, app mute, silent breaks, overlap, and device disconnection.
- [ ] Check transcription quality at five-minute chunk boundaries and unmatched `speaker_unknown` passages.
- [ ] Run a three-to-four-hour capture/processing test, measuring clock drift, gaps, disk usage, processing time, RAM, and VRAM.
- [ ] Exercise actual worker termination, recording close, export failure, crash/relaunch cleanup, and user cancellation. Synthetic tests cover only part of these paths.
- [ ] Validate supported Windows versions and a clean CPU-only PC without development Python, accounts, or downloads. The existing bundled-runtime checks occurred on the development PC.
- [ ] Establish measured minimum hardware requirements. Consider smaller models or a CPU package only if results justify them; do not silently reduce the current accuracy baseline.

## Before distributing a public binary

- [ ] Select the project source license; the code is already public but has no project license file.
- [ ] Complete exact dependency/model license, notice, attribution, and corresponding-source review; see [ThirdParty](ThirdParty.md).
- [ ] Improve reproducible provisioning of external build assets: verify embedded Python against a trusted expected digest, pin FFmpeg acquisition, and require fixed model revisions rather than resolving current upstream heads on each new download.
- [ ] Rebuild from a fresh release directory, include current user guide/notices, and rerun archive checks after the last application change.
- [ ] Publish a binary only after validation and distribution decisions. The current ZIP remains local and ignored by Git.

## Validation log

- Portable preview: extracted folder approximately 8.38 GiB; ZIP 5.91 GiB. Bundled source parity and exclusion of account/session data checked. No public binary release uploaded; archive remains in local ignored dist/.
- Documentation reconciliation: all 12 tracked Markdown documents reviewed against code and milestone history. No new runtime tests or binary rebuild were performed in this documentation-only pass.
- First preview: 12 focused tests passed; compile check passed; synthetic-silence worker produced an empty transcript. Bundled Python independently passed GPU and model smoke checks, audio decoding, and UI rendering. Folder size: 8.38 GiB. No actual microphone/system audio or public dataset was recorded during these checks.
- 2026-09-10: Workspace inspection found an empty directory and no existing Git repository. Application tests are not applicable to the documentation-only foundation.

- 2026-09-10: Created the public GitHub repository under RenatoBicharaVieira and successfully pushed the initial documentation commit to main.

