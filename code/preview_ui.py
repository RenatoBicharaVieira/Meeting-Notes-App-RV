"""Developer visual check; no audio recording."""
import os
import tempfile
from pathlib import Path
os.environ['QT_QPA_PLATFORM'] = 'offscreen'
from PySide6.QtWidgets import QApplication
import app as ui
from PySide6.QtGui import QFontDatabase
from local_runtime import ROOT

application = QApplication([])
application.setStyle('Fusion')
QFontDatabase.addApplicationFont('C:/Windows/Fonts/segoeui.ttf')
application.setStyleSheet(ui.STYLE)
with tempfile.TemporaryDirectory() as temporary:
    ui.ROOT = Path(temporary)
    (ui.ROOT / 'data').mkdir()
    window = ui.Window()
    window.show()
    application.processEvents()
    window.grab().save(str(ROOT / 'data/ui-preview.png'))
    window.close()
