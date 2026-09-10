# Meeting-Notes-App-RV — preview

Extract the complete portable ZIP into a writable folder, then double-click Meeting-Notes-App-RV.exe. Keep the runtime, code, and data/models folders next to the executable. No Python installation or Hugging Face account is needed to run the packaged app. NVIDIA acceleration requires a compatible installed driver; CPU processing is available but slower.

1. Choose English or Portuguese (Brazil), your microphone, and the system playback device used by Zoom/Teams.
2. Press Record. Minimize the window if desired; recording continues.
3. Use the app's microphone mute checkbox when needed. Zoom/Teams mute does not control this recorder.
4. Press Stop, then Transcribe. Processing is local and can take time, especially on CPU.
5. Enter speaker names in the fields. Hover over a field for an example quote. Leave a field blank to keep its generic speaker label.
6. Press Export to save a timestamped UTF-8 .txt file outside the app's temporary session folder.
7. Delete meeting audio if desired, or close the app to remove all temporary meeting data. Exported files are preserved.

Closing during recording/processing or before export prompts before discarding data. Starting another recording also asks before discarding the previous meeting. If processing or export fails, audio remains until you delete it or close the app. After an unexpected exit, the next launch cleans up abandoned sessions. Reusable models and language preference are retained.

Use headphones to prevent playback from leaking into your microphone. All sound from the selected output device is captured, including other apps. Select the correct devices before each meeting; device changes during capture are not automatically followed. Reopen the app after connecting a new device if it is not listed.

## Preview limitations

- Supports a maximum recording length of four hours; recording stops at that limit.
- Speaker labels describe voices, not Zoom/Teams participant identities. The microphone is labelled Me. Remote overlap, short utterances, and uncertain boundaries may be assigned incorrectly or labelled speaker_unknown.
- No transcript editor, history, automatic notes, live transcription, or cloud processing.
- Windows 10, CPU-only hardware, four-hour stress tests, and real Portuguese/English meeting accuracy still require validation. This is a development preview, not a production-certified release.
- Available disk space and RAM affect long meetings. Raw stored audio is approximately 230 MB per hour for both 16 kHz mono tracks; processing additionally uses model and waveform memory.
- Current large-v3 model is used on GPU or CPU. Smaller model profiles are deferred pending measurements.

For now use exported transcripts as reviewable drafts. The developer checks use synthetic fixtures and do not establish meeting transcription accuracy.
