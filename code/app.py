"""Meeting-Notes-App-RV: one window, one temporary meeting."""
import json
import os
import sys
import time
from pathlib import Path
from local_runtime import ROOT, configure

configure()
from PySide6.QtCore import QLockFile, QProcess, QTimer
from PySide6.QtWidgets import (QApplication, QCheckBox, QComboBox, QFileDialog,
    QFormLayout, QHBoxLayout, QLabel, QLineEdit, QMainWindow, QMessageBox,
    QProgressBar, QPushButton, QScrollArea, QVBoxLayout, QWidget)
from meeting_data import clean_stale, delete_session, export_text, new_session, save_json, timestamp
from recorder import Recorder, devices


class Window(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Meeting-Notes-App-RV')
        self.resize(650, 475)
        self.storage = ROOT / 'data/sessions'
        self.folder = self.recorder = self.worker = None
        self.segments, self.names = [], {}
        self.exported = False
        self.phase = 'idle'
        self.recorded_language = 'en'
        self.pending_output = ''
        self.worker_error = ''
        self.prefs_path = ROOT / 'data/preferences.json'
        try:
            self.prefs = json.loads(self.prefs_path.read_text(encoding='utf-8'))
        except (OSError, ValueError):
            self.prefs = {}
        central = QWidget()
        self.setCentralWidget(central)
        layout = QVBoxLayout(central)
        layout.setContentsMargins(22, 20, 22, 20)
        title = QLabel('Meeting notes')
        title.setStyleSheet('font-size: 23px; font-weight: 600;')
        layout.addWidget(title)
        subtitle = QLabel('Record locally. Name speakers. Export plain text.')
        subtitle.setStyleSheet('color: #9ca7b8;')
        layout.addWidget(subtitle)
        form = QFormLayout()
        self.language = QComboBox()
        self.language.addItem('English', 'en')
        self.language.addItem('Português (Brasil)', 'pt')
        self.language.setCurrentIndex(1 if self.prefs.get('language') == 'pt' else 0)
        form.addRow('Meeting language', self.language)
        self.microphone, self.playback = QComboBox(), QComboBox()
        for combo in (self.microphone, self.playback):
            combo.setMinimumContentsLength(20)
            combo.setSizeAdjustPolicy(QComboBox.SizeAdjustPolicy.AdjustToMinimumContentsLengthWithIcon)
        form.addRow('Microphone', self.microphone)
        form.addRow('System audio', self.playback)
        layout.addLayout(form)
        self.mute = QCheckBox('Mute microphone in this app')
        self.mute.toggled.connect(lambda value: self.recorder.mute(value) if self.recorder else None)
        layout.addWidget(self.mute)
        row = QHBoxLayout()
        self.buttons = {}
        for name, action in [('Record', self.record), ('Stop', self.stop), ('Transcribe', self.transcribe), ('Export', self.export)]:
            button = QPushButton(name)
            button.clicked.connect(action)
            self.buttons[name] = button
            row.addWidget(button)
        layout.addLayout(row)
        self.delete_button = QPushButton('Delete meeting audio')
        self.delete_button.clicked.connect(self.delete_audio)
        layout.addWidget(self.delete_button)
        self.status = QLabel('Ready — select the devices used by your meeting.')
        self.status.setWordWrap(True)
        layout.addWidget(self.status)
        self.progress = QProgressBar()
        self.progress.setFixedHeight(5)
        self.progress.setTextVisible(False)
        self.progress.hide()
        layout.addWidget(self.progress)
        self.speaker_form = QFormLayout()
        panel = QWidget()
        panel.setLayout(self.speaker_form)
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setWidget(panel)
        layout.addWidget(scroll)
        self.timer = QTimer(self)
        self.timer.setInterval(500)
        self.timer.timeout.connect(self.tick)
        self.timer.start()
        try:
            clean_stale(self.storage)
            microphones, playbacks, default_mic, default_playback = devices()
            for combo, items, preferred in [(self.microphone, microphones, default_mic), (self.playback, playbacks, default_playback)]:
                for item in items:
                    combo.addItem(item['name'], item)
                    if item['index'] == preferred:
                        combo.setCurrentIndex(combo.count() - 1)
        except Exception as exc:
            self.status.setText(f'Setup needs attention: {exc}')
        self.controls()

    def controls(self):
        busy = self.phase in ('recording', 'transcribing')
        audio = bool(self.folder and (self.folder / 'system.wav').exists())
        self.buttons['Record'].setEnabled(not busy and self.microphone.count() > 0 and self.playback.count() > 0)
        self.buttons['Stop'].setEnabled(self.phase == 'recording')
        self.buttons['Transcribe'].setEnabled(audio and not busy)
        self.buttons['Export'].setEnabled(bool(self.segments) and not busy)
        self.delete_button.setEnabled(audio and not busy)
        for widget in (self.language, self.microphone, self.playback):
            widget.setEnabled(not busy and not audio)
        self.mute.setEnabled(self.phase != 'transcribing')
        for edit in self.names.values():
            edit.setEnabled(not busy)
        self.progress.setVisible(self.phase == 'transcribing')
        self.progress.setRange(0, 0)

    def confirm(self, text):
        return QMessageBox.question(self, 'Discard meeting?', text,
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No) == QMessageBox.StandardButton.Yes

    def error(self, message):
        QMessageBox.warning(self, 'Meeting notes', str(message))

    def clear_names(self):
        while self.speaker_form.rowCount():
            self.speaker_form.removeRow(0)
        self.names = {}

    def discard(self):
        if self.folder:
            delete_session(self.storage, self.folder)
        self.folder = None
        self.segments = []
        self.exported = False
        self.clear_names()

    def record(self):
        if self.folder and not self.confirm('Starting a new meeting permanently discards the current meeting data. Exported files are kept. Continue?'):
            return
        try:
            self.discard()
            self.folder = new_session(self.storage)
            self.recorder = Recorder(self.folder, self.microphone.currentData(), self.playback.currentData(), self.mute.isChecked())
            self.phase = 'recording'
            self.recorded_language = self.language.currentData()
        except Exception as exc:
            self.phase = 'stopped'
            self.error(exc)
        self.controls()

    def stop(self):
        if self.recorder:
            errors = self.recorder.stop()
            self.recorder = None
            self.phase = 'stopped'
            self.status.setText('Recording saved. Press Transcribe when ready.')
            if errors:
                self.error('\n'.join(errors))
        self.controls()

    def tick(self):
        if self.recorder:
            elapsed = time.perf_counter() - self.recorder.origin
            self.status.setText(f'Recording  {timestamp(elapsed)}' + ('  •  Microphone muted' if self.mute.isChecked() else ''))
            fault = self.recorder.error()
            if fault or elapsed >= 4 * 3600:
                self.stop()
                self.error(fault or 'The four-hour recording limit has been reached.')

    def transcribe(self):
        self.worker = QProcess(self)
        self.worker.setProgram(sys.executable.replace('pythonw.exe', 'python.exe'))
        self.worker.setArguments(['-u', str(ROOT / 'code/transcribe_worker.py'), str(self.folder), self.recorded_language])
        self.worker.setWorkingDirectory(str(ROOT))
        self.worker.setProcessChannelMode(QProcess.ProcessChannelMode.SeparateChannels)
        self.worker.readyReadStandardOutput.connect(self.read_progress)
        self.worker.readyReadStandardError.connect(self.read_errors)
        self.worker.finished.connect(self.finished)
        self.worker.errorOccurred.connect(self.process_error)
        self.worker_error, self.pending_output = '', ''
        self.phase = 'transcribing'
        self.status.setText('Starting local processing…')
        self.controls()
        self.worker.start()

    def read_progress(self):
        self.pending_output += bytes(self.worker.readAllStandardOutput()).decode('utf-8', errors='replace')
        while '\n' in self.pending_output:
            line, self.pending_output = self.pending_output.split('\n', 1)
            try:
                item = json.loads(line)
                if 'status' in item:
                    self.status.setText(item['status'])
                if 'error' in item:
                    self.worker_error = item['error']
            except ValueError:
                pass

    def read_errors(self):
        # Drain warnings to prevent pipe blockage. Meeting text is never logged.
        self.worker.readAllStandardError()

    def process_error(self, error):
        if error == QProcess.ProcessError.FailedToStart:
            self.phase = 'stopped'
            self.worker_error = 'Processing could not start. Check that the runtime is available.'
            self.status.setText(self.worker_error)
            self.worker.deleteLater()
            self.worker = None
            self.controls()

    def finished(self, code, exit_status):
        self.read_progress()
        self.phase = 'stopped'
        if code == 0 and exit_status == QProcess.ExitStatus.NormalExit:
            try:
                self.segments = json.loads((self.folder / 'transcript.json').read_text(encoding='utf-8'))
                self.exported = False
                self.clear_names()
                for segment in self.segments:
                    speaker = segment['speaker']
                    if speaker not in self.names:
                        edit = QLineEdit('Me' if speaker == 'me' else '')
                        edit.setPlaceholderText(speaker)
                        edit.textChanged.connect(self.mark_dirty)
                        edit.setToolTip(segment['text'][:250])
                        self.names[speaker] = edit
                        self.speaker_form.addRow(speaker.replace('_', ' ').capitalize(), edit)
                self.status.setText('Name the speakers, then export.' if self.segments else 'No speech detected. Check your devices and recording.')
            except Exception as exc:
                self.error(f'Could not read the transcript: {exc}')
        else:
            self.status.setText('Processing failed. Audio is kept so you can retry.')
            self.error(self.worker_error or 'Processing stopped unexpectedly. There may not be enough memory; close other applications and retry.')
        self.worker.deleteLater()
        self.worker = None
        self.controls()

    def mark_dirty(self):
        self.exported = False

    def export(self):
        destination, _ = QFileDialog.getSaveFileName(self, 'Export transcript', str(Path.home() / 'meeting-transcript.txt'), 'Text files (*.txt)')
        if not destination:
            return
        if not destination.lower().endswith('.txt'):
            destination += '.txt'
        try:
            export_text(destination, self.segments, {key: edit.text() for key, edit in self.names.items()},
                'Portuguese (Brazil)' if self.recorded_language == 'pt' else 'English', self.storage)
            self.exported = True
            self.status.setText('Transcript exported. You may delete the meeting audio or close the app.')
        except Exception as exc:
            self.error(f'Export failed; your meeting is still available. {exc}')

    def delete_audio(self):
        if not self.segments and not self.confirm('Deleting this audio before transcription permanently discards the recording. Continue?'):
            return
        try:
            for path in (self.folder / 'microphone.wav', self.folder / 'system.wav'):
                path.unlink(missing_ok=True)
            self.status.setText('Audio deleted. The transcript remains available until you close the app.' if self.segments else 'Audio deleted. Ready for a new meeting.')
        except OSError as exc:
            self.error(exc)
        self.controls()

    def closeEvent(self, event):
        if self.folder and (self.phase in ('recording', 'transcribing') or not self.exported):
            if not self.confirm('Closing stops any recording or transcription and permanently discards this meeting data. Exported files are kept. Close?'):
                event.ignore()
                return
        if self.worker and self.worker.state() != QProcess.ProcessState.NotRunning:
            self.worker.blockSignals(True)
            self.worker.kill()
            if not self.worker.waitForFinished(10000):
                self.error('Processing has not stopped. Please try closing again.')
                event.ignore()
                return
        try:
            self.stop()
            self.discard()
            save_json(self.prefs_path, {'language': self.language.currentData()})
        except Exception as exc:
            self.error(f'Could not finish cleanup: {exc}. Close again to retry.')
            event.ignore()
            return
        event.accept()


STYLE = '''
        QWidget { background: #171b22; color: #edf0f5; font-family: "Segoe UI"; font-size: 13px; }
        QPushButton { background: #2c3544; border: 1px solid #414d60; border-radius: 5px; padding: 9px 12px; }
        QPushButton:hover { background: #39465b; }
        QPushButton:disabled { color: #687384; background: #202630; border-color: #292f38; }
        QLineEdit, QComboBox { background: #222935; border: 1px solid #414d60; border-radius: 4px; padding: 6px; }
        QScrollArea { border: 1px solid #2c3544; border-radius: 5px; }
        QProgressBar::chunk { background: #7ca7ef; }
        QCheckBox::indicator { width: 14px; height: 14px; border: 1px solid #65738b; border-radius: 3px; background: #222935; }
        QCheckBox::indicator:checked { background: #7ca7ef; border-color: #aac8fa; }
    '''


def main():
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    app.setStyleSheet(STYLE)
    (ROOT / 'data').mkdir(parents=True, exist_ok=True)
    lock = QLockFile(str(ROOT / 'data/app.lock'))
    lock.setStaleLockTime(0)
    if not lock.tryLock(0):
        QMessageBox.information(None, 'Meeting notes', 'The app is already open in this folder.')
        return 1
    window = Window()
    window.show()
    result = app.exec()
    lock.unlock()
    return result


if __name__ == '__main__':
    sys.exit(main())
