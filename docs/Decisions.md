# Decision history

Last updated: 2026-09-10.

## Current state and milestone references

The portable preview is implemented, both models are installed, and GitHub is configured. Historical entries below describe what was known at each stage; their old blockers are not current blockers. [ProjectOverview](ProjectOverview.md) describes the accepted scope and [TODO](TODO.md) is the live work list.

| Commit | Recorded milestone |
| --- | --- |
| `47b92ac` | Requirements and repository foundation |
| `e1785e1` | Public GitHub source repository configured |
| `e774345` | Corrected Python discovery; reused existing installation |
| `832a5c4` | Pinned GPU environment and Whisper setup |
| `ccb556d` | Community-1 download and offline GPU check completed |
| `31cc2a0` | Minimal app, tests, and portable build tooling |
| `972b785` | Portable ZIP verification and measured sizes |

## 2026-09-10 — Documentation reconciliation

Reviewed all 12 tracked Markdown files against the implementation and recorded evidence. Replaced obsolete current-state claims about missing Python, pending model access, candidate dependencies, and missing GitHub configuration. Split completed implementation from pending real-device, real-speech, and clean-PC validation. Recorded the measured 5.91 GiB ZIP / approximately 8.38 GiB folder instead of early estimates. This documentation pass does not change application code, run new accuracy benchmarks, rebuild the existing ZIP, or select a source license.

## 2026-09-10 — First application implementation and portable preview

Implemented the agreed one-window workflow in four small modules: UI, recorder, processing worker, and meeting-data helpers. Use a separate process for model inference so closing can stop computation before session cleanup. Use full-meeting diarization for stable remote speaker labels, while transcription reads five-minute blocks. This is simpler than adding custom cross-chunk voice matching, but long-meeting memory and chunk-boundary quality need measurement.

Package a thin executable launcher with an embedded Python runtime and unmodified dependency folders instead of freezing all ML libraries into one executable. Include only explicitly selected model/runtime assets, never the developer token cache. Keep source licensing and public redistribution checks as explicit remaining release tasks. Known recordings (AMI for English meetings, CORAA for Brazilian Portuguese) remain planned evaluation material after the initial app build; no dataset downloads were performed in this milestone.

The final archive passed source parity, expected asset/data-exclusion checks, duplicate-entry checks, and CRC verification. A late recorder fix was refreshed in the ZIP before verification. Twelve focused tests and bundled GPU checks passed. Silent playback gaps are padded incrementally; actual capture behavior with devices, overlap, and long meetings is not yet validated. CPU execution is implemented but not benchmarked; there is no separate CPU ZIP yet.

## 2026-09-10 — Both local models available

The user accepted Community-1 conditions and entered a Read token through the local hidden-input helper. Downloaded revision `3533c8cf8e369892e6b79ff1bf80f7b0286a54ee`; offline GPU inference on synthetic silence passed. This resolves the earlier model-access blocker. Both Whisper and Community-1 are now installed and runnable locally. No credentials or weights are committed. Real Portuguese/English speech and multi-speaker accuracy tests remain necessary before application quality claims.

## 2026-09-10 — Initial dependency environment validated

Created Python 3.11.9 `.venv`; pinned matching torch/torchaudio 2.11.0 CUDA 12.8 wheels rather than accepting an unconstrained mismatch. PySide6 6.11.2, PyAudioWPatch 0.2.12.8, faster-whisper 1.2.1, CTranslate2 4.8.2, pyannote.audio 4.0.7, and TorchCodec 0.16.0 passed imports. Added local FFmpeg shared libraries because TorchCodec requires them. Reuse PyTorch's CUDA DLL directory for CTranslate2, avoiding a global toolkit installation. GPU computation, synthetic decoding, and offline Whisper inference passed on the development PC. This does not establish accuracy or compatibility on other PCs.

At this stage Community-1 was still waiting for local authentication despite website sign-in. That blocker was resolved in `ccb556d`, as recorded above. The continuing decisions are to keep model/authentication data outside Git and disable telemetry in runtime helpers. See [StackSetup](StackSetup.md) for the working setup.

## 2026-09-10 — Reuse existing Python installation

After the user corrected the initial finding, inspection under the user's Windows account confirmed Python 3.13.14 (64-bit) and a working Python 3.11.9 command. Reuse existing Python 3.11 for the isolated environment rather than downloading a new runtime. The initial restricted shell had a different command path; its discovery result did not establish that Python was absent from the PC.

## 2026-09-10 — Stack preflight

The initial restricted-shell inspection confirmed the RTX 4070 and adequate disk space, but did not discover Python. This did not establish its absence from the PC. Later inspection found Python 3.11.9 and 3.13.14, and dependency versions were resolved in the setup milestone above. The retained decision is an isolated project environment without changing unrelated Python installations.

## 2026-09-10 — Product requirements and repository foundation

### Free local processing

Use downloaded models locally, avoiding paid APIs. ChatGPT analysis is a manual downstream step using the user's subscription. Reason: zero recurring application service costs and local audio processing.

### Post-meeting analysis

Drop live transcription and live diarization. Reason: reduce complexity and prioritize final accuracy without needing inference to keep pace with a call.

### Separate capture tracks

Record microphone and playback separately. Reason: playback may omit the user's voice, and separate tracks help attribution during overlap. Accept all-output audio rather than adding application-specific capture.

### Minimal explicit controls

Use Record, Stop, Transcribe, Export, and Delete meeting audio. Transcribe is manual, superseding the earlier automatic-after-Stop proposal. Keep recording active when minimized. Omit Pause and system tray integration.

### Plain-text export only

Export `.txt` only, superseding the original `.md`/`.txt` choice. Users edit exported text themselves. Allow speaker renaming in the app but no transcript editing or passage reassignment.

### Session-only meeting data

Remove all meeting data on normal close and provide manual audio deletion. This supersedes the earlier retained meeting history and automatic deletion immediately after export proposals. Preserve exports, models, and preferences. Warn before closing an unexported meeting or during recording/transcription. Reason: avoid accumulating meeting data and feature bloat.

### Portable ZIP

Use a portable folder, rather than an installer or monolithic executable. Reason: practical packaging of large models and native libraries. Recipients must not need accounts or downloads. Verify exact redistribution terms; never bundle the developer's token.

### Platform and language

The agreed targets were Windows 10/11 x64, Portuguese (Brazil), English, roughly six speakers, and four-hour online meetings. Remembered language selection was proposed because cost-free automatic detection cannot be guaranteed; it is now implemented. Platform and long-meeting targets still need real-world validation.

### Stack status

At requirements time, Python, PySide6, PyAudioWPatch, faster-whisper, and Community-1 were candidates. These components, sequential model loading, and a CPU path are now implemented; installed versions and limited verification are recorded in [StackSetup](StackSetup.md). Large-v3 remains the baseline awaiting speech-quality evaluation.

### Repository

Name app and repository Meeting-Notes-App-RV. Store source in `code/`, maintained rationale and progress in `docs/`, ignored local data in `data/`. Commit coherent development milestones. The remote destination was initially unspecified and subsequently configured as recorded below. Project source-license selection remains open.

## Reference material reviewed during requirements discussions

- Capture: https://learn.microsoft.com/en-us/windows/win32/coreaudio/loopback-recording
- Capture library: https://github.com/s0d3s/PyAudioWPatch
- UI licensing: https://www.qt.io/development/open-source-lgpl-obligations
- Transcription: https://github.com/SYSTRAN/faster-whisper
- Large model files: https://huggingface.co/Systran/faster-whisper-large-v3/tree/main
- Smaller model files: https://huggingface.co/Systran/faster-whisper-small/tree/main
- Diarization code: https://github.com/pyannote/pyannote-audio
- Diarization model and access terms: https://huggingface.co/pyannote/speaker-diarization-community-1

Recheck exact versions, licenses, and redistribution requirements during implementation. Prior estimates are not benchmark results.

## 2026-09-10 — GitHub publication

Authenticated as RenatoBicharaVieira and created the public repository https://github.com/RenatoBicharaVieira/Meeting-Notes-App-RV. The default branch is main and origin points to that repository. Local commit identity is Renato Vieira <renatovieira@puc-rio.br>. This supersedes the earlier pending remote destination. Source license selection remains pending.


## 2026-09-10 - Acquire known reference recordings

Downloaded one complete AMI English meeting with four speaker annotations and two original CORAA PT-BR clips from different regional sources. Preserve reference text and provenance under ignored data/test_audio; publish only the testing guide. This gives us speaker-reference coverage in English and short Portuguese transcription checks without downloading the full CORAA corpus or expanding the app interface. All three audio files decode successfully; real transcription and capture evaluation remain pending. See [Test samples](TestSamples.md) for exact IDs, licenses, procedure and limits.

## 2026-09-10 - Supplement short Portuguese references with a full conversation

The user requested a PT-BR sample of at least ten minutes and three speakers because the original clips are too short for meeting-style speaker testing. Downloaded the publisher-provided Hipsters Ponto Tech #291 episode: 52m55s with four listed participants. It stays local and is not bundled. It adds duration and multiple participants but has no verified reference transcript, so retain the original clips for text comparison and distinguish manual listening checks from scored evaluation.
