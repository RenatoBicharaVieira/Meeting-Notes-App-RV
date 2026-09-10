# Project overview

Last updated: 2026-09-10

## Objective

Meeting-Notes-App-RV is a free, locally processed, portable Windows application that turns online meeting recordings into timestamped, speaker-labelled `.txt` transcripts. The user manually uploads exports to ChatGPT for contextual conversations, notes, decisions, and action items. ChatGPT integration is outside the application.

## Supported scope

- Windows 10 and 11, 64-bit.
- Online Zoom/Teams meetings; no in-person/shared-microphone meetings.
- Typically up to six speakers and 30-minute to four-hour meetings.
- Brazilian Portuguese or English; language switching within a meeting is rare.
- Development hardware: Ryzen 7800X3D, 32 GB RAM, RTX 4070.
- Support less capable PCs through CPU fallback and evaluated model profiles. Minimum specifications and processing speeds are not yet measured.
- No paid API, live transcription, or network processing of meeting audio.

## Workflow and interface

A small English-only, dark window contains Record, Stop, Transcribe, Export, and Delete meeting audio buttons, a microphone-mute control, status/progress, and editable speaker-name fields beneath the controls.

1. Record captures the selected microphone and all audio from the selected playback device into separate synchronized tracks.
2. Recording continues when the normal window is minimized. No system tray or Pause control.
3. Stop finishes recording. Silent breaks may remain in recordings.
4. Transcribe explicitly starts local transcription and diarization. This supersedes earlier automatic processing after Stop.
5. Display anonymous stable speaker labels and editable names. A short example quote can help identify each speaker. No transcript editor.
6. Export saves a timestamped `.txt` file with the chosen names. No Markdown export.
7. Delete meeting audio explicitly removes recordings when requested. Do not silently delete recordings immediately after export.
8. Normal exit removes all meeting-specific recordings, temporary files, transcript data, and speaker mappings. Preserve user-exported files, reusable models, and app preferences.

Before closing with an unexported meeting, during recording, or during transcription, warn that closing permanently discards the meeting and allow cancellation. Closing during work must safely stop workers and release files before cleanup. Unexpected termination cannot guarantee immediate deletion; startup cleanup needs explicit implementation and validation.

## Language behavior

Prefer automatic detection only if it has no time, compute, or accuracy cost. That guarantee is unavailable, so a remembered Portuguese/English selector is the proposed initial choice.

## Accuracy and capture constraints

Microphone capture is independent of Zoom/Teams mute; the app has its own mute control. Assume only the local user speaks into the microphone. Remote participants arrive as mixed system audio; notifications and other application sounds are accepted. Overlapping remote voices and speaker grouping can be imperfect. Speaker names are supplied by the user, not inferred from meeting-platform metadata.

Write recordings incrementally to disk; do not buffer a four-hour meeting entirely in RAM. Preserve original timing through resampling and speech filtering. Never run heavy inference in audio capture callbacks or the UI thread.

## Distribution

Portable folder distributed as a ZIP, containing executable, dependencies, and models. No recipient installation, account, or additional downloads. The developer accepts creating a Hugging Face account for model acquisition; tokens must not be shipped. Verify redistribution terms for exact artifacts before bundling. CPU and NVIDIA editions are proposed to avoid unnecessary GPU library downloads.

Earlier package estimates (not measured): CPU ZIP 1–2.5 GB / extracted 2–4 GB; GPU large-v3 ZIP 4–7 GB / extracted 7–12 GB. Replace with measured sizes after packaging.

## Candidate architecture

Python + PySide6 UI; PyAudioWPatch/WASAPI capture; faster-whisper transcription; pyannote.audio Community-1 diarization. Evaluate large-v3 on the development PC and smaller/quantized configurations on weaker machines. Run heavy models sequentially to reduce peak memory. Alignment is optional, subject to demonstrated need. All choices require compatibility and offline packaging validation.

## Documentation and version control

Keep code and documentation current together, with local commits made by the development agent. Record why decisions were made and what was tested. The user is comfortable with public source code; no hosting account, remote destination, or source license has yet been selected.
