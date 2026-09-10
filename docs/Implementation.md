# First application preview

Last updated: 2026-09-10. Implementation milestone `31cc2a0`; archive verification milestone `972b785`. This document describes existing code, with limits called out separately.

## Design

One PySide6 window manages one temporary meeting. Record and Stop only capture audio; Transcribe launches a separate Python process. The separate process releases model memory on completion and can be terminated safely before closing and deleting session files. No database, web service, history, transcript editor, or account UI is introduced.

Controls are enabled by state:

| State | Available actions |
| --- | --- |
| Ready | Choose devices/language, Record |
| Recording | Stop, microphone mute; minimize normally |
| Stopped with audio | Record another meeting, Transcribe, Delete audio |
| Transcribing | Wait or close with discard confirmation |
| Transcript ready | Rename speakers, Export, Record another meeting; retranscribe/delete audio while audio still exists |

Device and language selectors are locked while audio exists or work is active. Only language is persisted; device choices start with the detected system defaults on launch. Starting another recording discards the old session after confirmation. There is no file-import control in this preview.

Repeated recording asks before discarding the current session. Retranscribing regenerates the transcript and name fields. Closing while processing or without an exported current transcript asks before permanent deletion. Changes to speaker names mark the export as out of date. Failed exports do not mark the meeting exported.

## Audio and timestamps

WASAPI microphone and loopback streams are captured separately. Callbacks enqueue input into bounded queues; writer threads downmix to mono, resample to 16 kHz PCM, and write incremental WAV files. The microphone mute zeros samples while preserving timeline duration. Stream timestamps map to a shared monotonic start; significant gaps are padded and overlaps trimmed. Overflow, a stopped stream, and clock jumps are reported rather than silently ignored. Real-device drift and reconnect scenarios still require validation.

Recording is capped at four hours. Stored mono PCM uses approximately 230 MB/hour for both tracks combined. Transcription reads five-minute chunks; no full native-rate multi-channel recording is held in RAM. Full-meeting diarization uses the normalized system waveform (approximately 922 MB float32 at four hours, plus model/intermediate memory). Total peak memory is not yet measured on long meetings. This preserves consistent speaker clustering across chunks rather than introducing custom speaker-embedding matching.

Three-minute callback gaps are covered by a synthetic test; padding is written in small pieces. This does not prove every WASAPI device's clock or silence behavior. The diarization call currently permits up to six remote speakers plus the separately known microphone voice; the product's expected use remains approximately six people total, not a guaranteed maximum-speaker accuracy result.

Whisper transcribes each track with explicit language, word timestamps, and speech detection. Word timestamps are matched to Community-1 exclusive speaker turns by overlap. Unmatched words are labelled speaker_unknown; microphone words are labelled me. The output is sorted chronologically. Five-minute transcription boundaries currently have no overlapping context; boundary accuracy must be assessed with real recordings.

## Local data and cleanup

Only marked session folders directly under data/sessions are eligible for cleanup. Reparse points are refused. A single-instance lock prevents two copies in the same folder from cleaning each other's sessions. After a crash, the next launch cleans abandoned sessions. Exports into the session tree are rejected. Exports are written through a temporary file and atomically replaced; original exports survive failed writes and session deletion.

Models and preferences persist. The application does not upload audio. Worker model loading uses local paths and offline mode. Developer account tokens are excluded from portable assembly.

Export writes a title, language, and `[HH:MM:SS] Name: text` lines in UTF-8. Timestamps are recording-relative segment starts, not wall-clock time or start/end ranges. Empty speaker-name fields retain generic labels; examples are shown as field tooltips. Editing a name invalidates the prior export state. Reprocessing regenerates names and text; no edit history is retained.

## Packaging

A small executable launches a bundled, official Python 3.11.9 embedded runtime with unmodified package directories. This avoids fragile freezing of the entire ML stack. The portable folder contains runtime/, code/, and allowlisted data/models and data/runtime/ffmpeg. PyTorch's GPU libraries are reused by CTranslate2. Model processing falls back to CPU if CUDA is unavailable; it currently uses the same large model, so CPU performance needs measurement.

CPU mode uses INT8 transcription. CUDA mode uses float16 transcription. GPU exhaustion or an inference error does not trigger an automatic CPU retry; the UI reports failure and retains the audio. Separate CPU packaging and smaller models are not implemented. Dependency directories currently include development packages as well; package-size pruning is not a completed optimization.

The development preview is for local evaluation. Source-license choice, complete third-party redistribution audit, Windows 10/CPU-only validation, and real meeting accuracy remain release work.

## Verification

- Twelve automated tests passed: UTF-8 export/timestamps, export survival after cleanup, preservation of existing exports after a failed replacement, protected folders, original chunk time offsets, speaker-turn assignment, UI control states, cancellation of close in recording/processing/unexported states, audio-only deletion, stereo resampling/muting, and padding a three-minute silent break.
- The dark window was rendered and visually inspected at 650 x 475 pixels using an offscreen preview.
- No private microphone/system audio or online dataset was recorded during these tests.
- The full worker process completed on two generated silent tracks and produced an empty transcript, with no invented text.
- The bundled embedded runtime passed imports, GPU computation, audio-device enumeration, synthetic WAV decoding, and offline Whisper/Community-1 GPU smoke tests. Its offscreen window also rendered successfully.
- Portable folder measured 8.38 GiB before subsequent Python bytecode caches; ZIP measured 5.91 GiB. `code/check_release.py` verifies packaged source parity, required runtime/model files, exclusion of account/session data, unique entries, and ZIP CRCs.

## Remaining evidence gaps

Real playback/microphone recording, speaker accuracy, Portuguese/English word accuracy, chunk-boundary effects, long-meeting resource use, device reconnects, hardware-level shutdown failures, and a clean recipient PC remain untested. CPU-only and target Windows-version compatibility are not established by running embedded Python on the development PC. [TODO](TODO.md) tracks these separately from completed implementation. No tests were rerun during this Markdown-only refresh.
