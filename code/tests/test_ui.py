import os
os.environ['QT_QPA_PLATFORM'] = 'offscreen'
import pytest
from PySide6.QtWidgets import QApplication
import app as ui
from meeting_data import new_session


@pytest.fixture
def window(tmp_path, monkeypatch):
    application = QApplication.instance() or QApplication([])
    monkeypatch.setattr(ui, 'ROOT', tmp_path)
    device = {'index': 1, 'name': 'Test device'}
    monkeypatch.setattr(ui, 'devices', lambda: ([device], [device], 1, 1))
    view = ui.Window()
    yield view
    view.phase = 'stopped'
    view.recorder = None
    monkeypatch.setattr(view, 'confirm', lambda _: True)
    view.close()


def test_idle_and_processing_controls(window):
    assert window.buttons['Record'].isEnabled()
    assert not window.buttons['Stop'].isEnabled()
    assert not window.buttons['Transcribe'].isEnabled()
    window.folder = new_session(window.storage)
    (window.folder / 'system.wav').write_bytes(b'audio')
    window.phase = 'transcribing'
    window.controls()
    assert not any(button.isEnabled() for button in window.buttons.values())
    assert not window.delete_button.isEnabled()


@pytest.mark.parametrize('phase', ['stopped', 'recording', 'transcribing'])
def test_cancel_close_preserves_unexported_meeting(window, monkeypatch, phase):
    window.folder = new_session(window.storage)
    path = window.folder
    window.phase = phase
    monkeypatch.setattr(window, 'confirm', lambda _: False)
    assert not window.close()
    assert path.exists()


def test_delete_audio_keeps_transcript_for_export(window):
    window.folder = new_session(window.storage)
    for filename in ('system.wav', 'microphone.wav'):
        (window.folder / filename).write_bytes(b'audio')
    window.segments = [{'speaker': 'me', 'start': 0, 'text': 'Hello'}]
    window.delete_audio()
    assert window.segments
    assert window.buttons['Export'].isEnabled()
    assert not window.buttons['Transcribe'].isEnabled()
