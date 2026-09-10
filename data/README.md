# Local data

Last updated: 2026-09-10.

This directory is reserved for untracked runtime assets and development working data. Its contents are ignored except this document and `.gitkeep`.

Keep persistent models and preferences separate from temporary meeting sessions. Delete meeting data on normal application exit and provide safe recovery cleanup after interrupted sessions. Exported `.txt` files selected by the user are outside session cleanup and must be preserved.

Never distribute account tokens or personal meeting recordings with the portable app.

## Current layout and lifetime

| Location | Contents | Lifetime / packaging |
| --- | --- | --- |
| `models/faster-whisper-large-v3/` | Transcription weights and download manifest | Persistent; bundled |
| `models/community-1/` | Diarization weights and download manifest | Persistent; bundled |
| `runtime/ffmpeg/` | Shared audio-decoding libraries and notices | Persistent; bundled |
| `huggingface/` | Developer download/authentication cache by default | Never bundled or committed |
| `sessions/meeting-<id>/` | Marked session folder with microphone/system WAVs, recording metadata, and transcript JSON | Deleted on normal close; abandoned marked sessions cleaned on next launch |
| `preferences.json` | Last language selection | Retained locally; excluded from a fresh ZIP |
| `app.lock` | Single-instance coordination | Runtime only; excluded from ZIP |
| `test_audio/` | Three reference WAVs with text, one longer PT-BR podcast MP3, source annotations and provenance manifest | Local test assets; ignored, never bundled; retained separately from session cleanup |

Manual audio deletion removes the two WAV files while keeping any transcript available in the current window. Closing clears the remaining session data and in-memory speaker names. Exported `.txt` files must live outside the session tree; export rejects destinations inside it. Cleanup refuses linked/reparse-point session contents and reports failure rather than intentionally following those links.

Developer assets such as the UI preview image or downloaded FFmpeg archive are not meeting history and are not part of session cleanup. The portable builder copies explicitly chosen model/runtime directories, not this whole data directory. Actual crash, device-loss, and long-recording behavior still needs validation beyond the synthetic cleanup tests.
