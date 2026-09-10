# Meeting-Notes-App-RV — preview

Last updated: 2026-09-10. This guide describes the implemented first preview. The local ZIP is 5.91 GiB and extracts to approximately 8.38 GiB before runtime caches or recordings.

Extract the complete portable ZIP into a writable folder, then double-click Meeting-Notes-App-RV.exe. Keep the complete runtime, code, and data folders next to the executable. The package includes Python and both models; there is no recipient account or model-download step. NVIDIA acceleration requires a compatible installed driver. A CPU path is implemented, but its speed and operation on CPU-only PCs have not yet been validated. The portable checks so far ran on the development PC.

1. Choose English or Portuguese (Brazil), your microphone, and the system playback device used by Zoom/Teams.
2. Press Record. Minimize the window if desired; recording continues.
3. Use the app's microphone mute checkbox when needed. Zoom/Teams mute does not control this recorder.
4. Press Stop, then Transcribe. Processing is local and can take time, especially on CPU.
5. Enter speaker names in the fields. Hover over a field for an example quote. Leave a field blank to keep its generic speaker label.
6. Press Export to save a timestamped UTF-8 .txt file outside the app's temporary session folder.
7. Delete meeting audio if desired, or close the app to remove all temporary meeting data. Exported files are preserved.

Closing during recording/processing or before export prompts before discarding data. Starting another recording also asks before discarding the previous meeting. If processing or export fails, audio remains until you delete it or close the app. After an unexpected exit, the next launch cleans up abandoned sessions. Reusable models and language preference are retained.

Speaker renaming is the only transcript editing provided. Re-running Transcribe regenerates the transcript and resets speaker-name fields. Changing names after export means you need to export again to save those changes. Manual audio deletion keeps an already generated transcript available until close, but prevents retranscription. If no transcript exists yet, audio deletion asks for confirmation.

Timestamps in the exported file count from the start of recording, for example `[00:03:12] Speaker 1: ...`. The app does not infer participants' real names or generate meeting notes. Upload the exported file to ChatGPT yourself for that last step.

Use headphones to prevent playback from leaking into your microphone. All sound from the selected output device is captured, including other apps. Select the correct devices before each meeting; device changes during capture are not automatically followed. Reopen the app after connecting a new device if it is not listed.

## If a control is unavailable

- Stop is available only while recording.
- Transcribe requires saved audio and is disabled while another operation is active.
- Export becomes available after speech has been transcribed. A silent recording can produce no transcript.
- Device/language selection is locked while the current audio exists. The language choice is remembered on exit; audio-device choices start from system defaults when the app opens.
- Processing errors keep the recording available for retry. The app does not automatically switch from a failed GPU job to CPU mode.

Keep exports outside the temporary session folder; the app rejects export destinations inside it. Exported files are your responsibility to keep or edit and are not part of the app's cleanup.

## Preview limitations

- Supports a maximum recording length of four hours; recording stops at that limit.
- Speaker labels describe voices, not Zoom/Teams participant identities. The microphone is labelled Me. Remote overlap, short utterances, and uncertain boundaries may be assigned incorrectly or labelled speaker_unknown.
- No transcript editor, history, automatic notes, live transcription, or cloud processing.
- Windows 10, CPU-only hardware, four-hour stress tests, and real Portuguese/English meeting accuracy still require validation. This is a development preview, not a production-certified release.
- Available disk space and RAM affect long meetings. Raw stored audio is approximately 230 MB per hour for both 16 kHz mono tracks; processing additionally uses model and waveform memory.
- Current large-v3 model is used on GPU or CPU. Smaller model profiles are deferred pending measurements.

For now use exported transcripts as reviewable drafts. The developer checks use synthetic fixtures and do not establish meeting transcription accuracy.

The repository guide is the current source of instructions. The README.txt inside an already built ZIP is a snapshot and will be refreshed during the next build.
