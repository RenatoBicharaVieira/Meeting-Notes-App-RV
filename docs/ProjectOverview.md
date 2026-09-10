# Project overview

Last updated: 2026-09-10

## Objective

Meeting-Notes-App-RV is a free, locally processed, portable Windows application that turns online meeting recordings into timestamped, speaker-labelled `.txt` transcripts. The user manually uploads exports to ChatGPT for contextual conversations, notes, decisions, and action items. ChatGPT integration is outside the application.

## Target scope and current preview

The first application and local portable ZIP are built. This is a development preview with synthetic verification, not a completed real-meeting evaluation. See [Implementation](Implementation.md) for details and [TODO](TODO.md) for remaining validation.

- Windows 10 and 11, 64-bit.
- Online Zoom/Teams meetings; no in-person/shared-microphone meetings.
- Typically up to six speakers and 30-minute to four-hour meetings.
- Brazilian Portuguese or English; language switching within a meeting is rare.
- Development hardware: Ryzen 7800X3D, 32 GB RAM, RTX 4070.
- CPU fallback is implemented with the same large-v3 model. Smaller profiles and minimum specifications are not yet established.
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

The preview warns before closing an unexported meeting or during recording/transcription and allows cancellation. It stops processing before cleanup. Marked stale-session cleanup is implemented for the next launch after an unexpected exit; immediate deletion during a crash cannot be guaranteed. Synthetic checks cover cancellation and cleanup helpers; real hardware/crash scenarios remain pending.

## Language behavior

The implemented Portuguese/English selector remembers the last choice on normal exit. Automatic detection is excluded because the requested guarantee of no time, compute, or accuracy cost cannot be made.

## Accuracy and capture constraints

Microphone capture is independent of Zoom/Teams mute; the app has its own mute control. Assume only the local user speaks into the microphone. Remote participants arrive as mixed system audio; notifications and other application sounds are accepted. Overlapping remote voices and speaker grouping can be imperfect. Speaker names are supplied by the user, not inferred from meeting-platform metadata.

Write recordings incrementally to disk; do not buffer a four-hour meeting entirely in RAM. Preserve original timing through resampling and speech filtering. Never run heavy inference in audio capture callbacks or the UI thread.

## Distribution

The built local ZIP contains an executable launcher, embedded Python, dependencies, and both models. Account-free offline use is the recipient requirement; bundled-runtime checks passed on the development PC, while a clean recipient PC still needs testing. Developer Hugging Face acquisition is complete and credentials are excluded. One GPU-capable package currently also has a CPU execution path; separate CPU and NVIDIA editions remain an optional later packaging decision.

Measured preview: ZIP **5.91 GiB**, extracted folder approximately **8.38 GiB** before runtime caches. These replace the early GPU package estimates. No smaller CPU package has been built. The ZIP is local under ignored `dist/`; no GitHub binary release has been published. Source-license choice and the complete redistribution review remain open.

## Implemented architecture

Python 3.11.9 + PySide6 UI; PyAudioWPatch/WASAPI capture; faster-whisper large-v3 transcription; pyannote.audio Community-1 diarization. Capture uses separate queues/writers; a separate process loads the models sequentially. Transcription reads five-minute blocks; diarization uses the whole normalized system track to group voices across the meeting. Word/turn overlap assigns speakers. Full-meeting processing peak memory and chunk-boundary accuracy are still unmeasured. WhisperX, a database, and a web server are not included.

Twelve focused tests, a generated-silence worker run, bundled offline GPU checks, UI rendering, and archive integrity/source-parity checks passed. These do not establish recognition accuracy, recording reliability over four hours, or Windows 10/CPU-only support. The development PC is the only machine checked so far.

## Documentation and version control

Code and documentation are committed together to [RenatoBicharaVieira/Meeting-Notes-App-RV](https://github.com/RenatoBicharaVieira/Meeting-Notes-App-RV), branch `main`. Source is public; project licensing is unresolved. The repository records reasoning, changes, verification evidence, and outstanding work. Downloaded models, tokens, meeting data, environments, and built archives stay outside Git.
