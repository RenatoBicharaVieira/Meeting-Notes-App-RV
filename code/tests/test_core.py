import json
import wave
from pathlib import Path

import pytest

from meeting_data import clean_stale, delete_session, export_text, new_session
from transcribe_worker import assign_words, read_chunks


def test_export_survives_session_cleanup_and_preserves_portuguese(tmp_path):
    storage = tmp_path / 'sessions'
    session = new_session(storage)
    (session / 'system.wav').write_bytes(b'audio')
    destination = tmp_path / 'meeting.txt'
    export_text(destination, [{'start': 3661, 'text': 'Olá, reunião amanhã.', 'speaker': 's1'}],
                {'s1': 'João'}, 'Portuguese (Brazil)', storage)
    delete_session(storage, session)
    assert '[01:01:01] João: Olá, reunião amanhã.' in destination.read_text(encoding='utf-8')
    assert not session.exists()


def test_cleanup_refuses_unowned_folder_and_export_to_session(tmp_path):
    storage = tmp_path / 'sessions'
    session = new_session(storage)
    with pytest.raises(ValueError):
        export_text(session / 'export.txt', [], {}, 'English', storage)
    with pytest.raises(ValueError):
        delete_session(storage, tmp_path)
    unrelated = storage / 'keep'
    unrelated.mkdir()
    clean_stale(storage)
    assert unrelated.exists()
    assert not session.exists()


def test_word_assignment_splits_at_speaker_change_and_marks_unknown():
    words = [{'start': 0, 'end': .4, 'text': 'Hello'}, {'start': .5, 'end': .9, 'text': ' there'},
             {'start': 1, 'end': 1.4, 'text': ' Yes'}, {'start': 3, 'end': 3.4, 'text': ' Unknown'}]
    result = assign_words(words, [(0, 1, 'speaker_1'), (1, 2, 'speaker_2')])
    assert [item['speaker'] for item in result] == ['speaker_1', 'speaker_2', 'speaker_unknown']
    assert result[0]['text'] == 'Hello there'


def test_streamed_wav_chunks_keep_original_time(tmp_path):
    path = tmp_path / 'audio.wav'
    with wave.open(str(path), 'wb') as out:
        out.setparams((1, 2, 16000, 0, 'NONE', 'not compressed'))
        out.writeframes(b'\0\0' * 40000)
    chunks = list(read_chunks(path, seconds=1))
    assert [offset for offset, _ in chunks] == [0, 1, 2]
    assert [len(data) for _, data in chunks] == [16000, 16000, 8000]


def test_failed_export_preserves_existing_file(tmp_path, monkeypatch):
    import meeting_data
    destination = tmp_path / 'existing.txt'
    destination.write_text('Keep this export', encoding='utf-8')
    def fail(*args):
        raise PermissionError('File locked')
    monkeypatch.setattr(meeting_data.os, 'replace', fail)
    with pytest.raises(PermissionError):
        export_text(destination, [], {}, 'English', tmp_path / 'sessions')
    assert destination.read_text() == 'Keep this export'
    assert list(tmp_path.glob('.meeting-export-*')) == []
