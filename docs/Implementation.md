# First application preview

## Design

One PySide6 window manages one temporary meeting. Record and Stop only capture audio; Transcribe launches a separate Python process. The separate process releases model memory on completion and can be terminated safely before closing and deleting session files. No database, web service, history, transcript editor, or account UI is introduced.

Controls are enabled by state:

| State | Available actions |
| --- | --- |
| Ready | Choose devices/language, Record |
| Recording | Stop, microphone mute; minimize normally |
| Stopped with audio | Record another meeting, Transcribe, Delete audio |
| Transcribing | Wait or close with discard confirmation |
| Transcript ready | Rename speakers, Export, Delete audio, Record another meeting |

Repeated recording asks before discarding the current session. Retranscribing regenerates the transcript and name fields. Closing while processing or without an exported current transcript asks before permanent deletion. Changes to speaker names mark the export as out of date. Failed exports do not mark the meeting exported.

## Audio and timestamps

WASAPI microphone and loopback streams are captured separately. Callbacks enqueue input into bounded queues; writer threads downmix to mono, resample to 16 kHz PCM, and write incremental WAV files. The microphone mute zeros samples while preserving timeline duration. Stream timestamps map to a shared monotonic start; significant gaps are padded and overlaps trimmed. Overflow, a stopped stream, and clock jumps are reported rather than silently ignored. Real-device drift and reconnect scenarios still require validation.

Recording is capped at four hours. Stored mono PCM uses approximately 230 MB/hour for both tracks combined. Transcription reads five-minute chunks; no full native-rate multi-channel recording is held in RAM. Full-meeting diarization uses the normalized system waveform (approximately 922 MB float32 at four hours, plus model/intermediate memory). Total peak memory is not yet measured on long meetings. This preserves consistent speaker clustering across chunks rather than introducing custom speaker-embedding matching.

Whisper transcribes each track with explicit language, word timestamps, and speech detection. Word timestamps are matched to Community-1 exclusive speaker turns by overlap. Unmatched words are labelled speaker_unknown; microphone words are labelled me. The output is sorted chronologically. Five-minute transcription boundaries currently have no overlapping context; boundary accuracy must be assessed with real recordings.

## Local data and cleanup

Only marked session folders directly under data/sessions are eligible for cleanup. Reparse points are refused. A single-instance lock prevents two copies in the same folder from cleaning each other's sessions. After a crash, the next launch cleans abandoned sessions. Exports into the session tree are rejected. Exports are written through a temporary file and atomically replaced; original exports survive failed writes and session deletion.

Models and preferences persist. The application does not upload audio. Worker model loading uses local paths and offline mode. Developer account tokens are excluded from portable assembly.

## Packaging

A small executable launches a bundled, official Python 3.11.9 embedded runtime with unmodified package directories. This avoids fragile freezing of the entire ML stack. The portable folder contains runtime/, code/, and allowlisted data/models and data/runtime/ffmpeg. PyTorch's GPU libraries are reused by CTranslate2. Model processing falls back to CPU if CUDA is unavailable; it currently uses the same large model, so CPU performance needs measurement.

The development preview is for local evaluation. Source-license choice, complete third-party redistribution audit, Windows 10/CPU-only validation, and real meeting accuracy remain release work.

## Verification

- Twelve automated tests passed: UTF-8 export/timestamps, export survival after cleanup, preservation of existing exports after a failed replacement, protected folders, original chunk time offsets, speaker-turn assignment, UI control states, cancellation of close in recording/processing/unexported states, audio-only deletion, stereo resampling/muting, and padding a three-minute silent break.
- The dark window was rendered and visually inspected at 650 x 475 pixels using an offscreen preview.
- No private microphone/system audio or online dataset was recorded during these tests.
- The full worker process completed on two generated silent tracks and produced an empty transcript, with no invented text.
- The bundled embedded runtime passed imports, GPU computation, audio-device enumeration, synthetic WAV decoding, and offline Whisper/Community-1 GPU smoke tests. Its offscreen window also rendered successfully.
- Portable folder measured 8.38 GiB before subsequent Python bytecode caches. Final ZIP measurements are recorded in TODO.md when completed.
