# Decision history

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
Support Windows 10/11 x64, Portuguese (Brazil), and English. Up to roughly six speakers and four-hour online meetings. Remembered language selection is proposed because cost-free automatic detection cannot be guaranteed.

### Stack status
Python, PySide6, PyAudioWPatch, faster-whisper, and pyannote Community-1 are candidates, not a validated dependency set. Large-v3 is the accuracy baseline to test. Sequential model loading and CPU fallback are proposed for portability.

### Repository
Name app and repository Meeting-Notes-App-RV. Store source in `code/`, maintained rationale and progress in `docs/`, ignored local data in `data/`. Commit coherent development milestones. Public source is acceptable, but no remote has been requested by destination and no project license chosen.

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

