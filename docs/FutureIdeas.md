# Future ideas

Last updated: 2026-09-10. The minimal app and portable preview already exist; the next priority is validating that implementation.

These are explicitly outside initial scope. Listing an idea does not authorize implementation.

- Live transcription or diarization.
- In-app transcript editing or passage-level speaker reassignment.
- Markdown export, generated notes, or direct ChatGPT/API integration.
- Meeting history, search, or persistent voice identity profiles.
- Pause/resume, system tray, automatic meeting detection.
- Application-specific capture rather than all-output capture.
- In-person meetings with a shared microphone.
- Additional operating systems, interface languages, or themes.
- Automatic language detection if its measured tradeoffs become acceptable.
- Additional model profiles after measured need.
- A separate CPU-only portable package if measurements justify its download-size benefit. The current single package already contains a CPU execution path.

Keep the first release focused on Record → Stop → Transcribe → Rename → Export, with deliberate audio deletion and session cleanup.

Known-recording evaluation, device reliability, cleanup correctness, long-meeting memory measurements, supported-PC verification, and release documentation are required follow-up work in [TODO](TODO.md), not optional product features. Do not postpone those checks in favor of adding the ideas above.
