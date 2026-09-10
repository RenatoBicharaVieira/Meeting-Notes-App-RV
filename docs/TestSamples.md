# Reference audio for testing

Prepared and decoded successfully on 2026-09-10. These are test inputs, not application accuracy results. Files live in ignored `data/test_audio/` and are excluded from the portable app and GitHub.

| Audio filename | Language / duration | Reference and purpose |
| --- | --- | --- |
| `english_ami_ES2002a.wav` | English, 21m 12.64s | AMI meeting ES2002a, mixed headsets; four annotated speakers A–D. Timestamped text and JSON contain 236 speech segments. Checks transcription and speaker separation. |
| `ptbr_coraa_sp2010.wav` | PT-BR, 8.31s | CORAA SP2010 `test/sp/45227_sp_.wav`, São Paulo accent; fast spontaneous/read speech category. Validated text for a short transcription check. |
| `ptbr_coraa_coral.wav` | PT-BR, 39.42s | CORAA C-ORAL-BRASIL I `test/CORAL/13711_CO_bfammn22.wav`, Minas Gerais accent; spontaneous speech with hesitations and filled pauses. Validated text for a more demanding transcription check. |

Each of the original three WAVs has a matching `.reference.txt`. `manifest.json` records source URLs, original archive paths, metadata, SHA-256 hashes, sizes, durations and codecs. Total audio size is approximately 41.75 MiB. All three files were fully decoded using PyAV; all are mono at 16 kHz. AMI is 16-bit PCM; the original CORAA clips are floating-point PCM. Audio has not been trimmed, concatenated or re-encoded.

## Additional long PT-BR conversation

Added on 2026-09-10 after the user requested at least ten minutes and three speakers. `data/test_audio/ptbr_hipsters_291.mp3` is the complete **Hipsters Ponto Tech #291: Processamento de Linguagem Natural** episode (2022-02-08), **52m 54.95s**, 37.48 MiB, stereo MP3 at 44.1 kHz. The [publisher page](https://www.hipsters.tech/processamento-de-linguagem-natural-hipsters-ponto-tech-291/) lists four participants: Paulo Silveira, Ana Mioto, João Granzotti and Sthefanie Monica, and provides the [audio download](https://media.blubrry.com/hipsterstech/content.blubrry.com/hipsterstech/hipsters_291_nlp.mp3).

The entire file decoded successfully with PyAV; source, duration and SHA-256 are recorded in the local manifest. Participant count is supported by the publisher listing, not an independently annotated speaker timeline. No reference transcript was found on the publisher page. Use it for longer PT-BR playback/capture and manual speaker-consistency checks; do not treat app-generated text as ground truth. Podcast introductions, music and editing differ from an online meeting. This supplements rather than replaces the short reference-text clips.

The publisher offers a download, but no open redistribution license was established. Keep this file local, outside Git and app distributions. The reference-text comparison step below applies to the original three samples; this fourth sample requires manual listening.

## Provenance and reproduction

- AMI Consortium, [official download and license information](https://groups.inf.ed.ac.uk/ami/download/), CC BY 4.0. [Meeting audio](https://groups.inf.ed.ac.uk/ami/AMICorpusMirror/amicorpus/ES2002a/audio/ES2002a.Mix-Headset.wav), [manual annotations v1.6.2](https://groups.inf.ed.ac.uk/ami/AMICorpusAnnotations/ami_public_manual_1.6.2.zip). The local reference is a reformatted derivative: segment child ranges were resolved against word XML, spoken words joined, then segments sorted by start time. Non-word events are omitted; original timing and speaker letters are preserved. Raw XML and the annotation ZIP remain under `sources/`.
- CORAA ASR v1.1, Candido Junior et al.; [official project and attribution](https://github.com/nilc-nlp/CORAA), [CC BY-NC-ND 4.0 license](https://github.com/nilc-nlp/CORAA/blob/main/LICENSE). The official project links this [test archive](https://huggingface.co/datasets/gabrielrstan/CORAA-v1.1/resolve/main/test.zip) and [metadata CSV](https://huggingface.co/datasets/gabrielrstan/CORAA-v1.1/resolve/main/metadata_test_final.csv). Only the two entries above were extracted using HTTP byte ranges, avoiding the complete 2.42 GB download. Reference text is copied unchanged from matching metadata rows explicitly marked `pt_br`. Both were selected by highest reference word count within their respective source datasets. The metadata CSV and license are retained locally.

The CORAA material is retained for local noncommercial evaluation, not bundled for redistribution. These dataset licenses are separate from the still-unselected application source license.

## Test procedure

1. Open the app and select the playback device that the audio player uses. Choose the sample language and mute the microphone in the app.
2. Press Record, then play one WAV through that device. Keep other system audio quiet. The English file has roughly 50 seconds before its first annotated speech, so initial silence is expected.
3. After playback finishes, Stop, Transcribe, assign speaker names where applicable, and Export outside the session folder.
4. Compare the export with the matching reference text. For English, map arbitrary output speaker labels to A–D by their speech; labels need not have the same numbering. Account for the delay between pressing Record and starting playback when comparing timestamps.
5. Record processing time, missing/repeated words, speaker confusion, timestamp drift and any capture errors. Close the app and verify session cleanup while preserving the exported file.

The app has no audio-import feature. Playback tests exercise system capture as well as processing; they do not exercise the separate microphone track. A later developer-level direct-file test can isolate model performance without adding an import UI.

## Limits

Portuguese references have no speaker identities or segment timestamps, so they cannot score diarization. English annotations can contain overlapping turns; the text rendering is not a complete diarization scoring format. The AMI recording is an in-person headset mix used as a reference input, not proof of Zoom/Teams capture quality. These three examples do not establish long-meeting reliability, broad language accuracy, CPU performance or independence from model training data. No transcription accuracy score has yet been measured.
