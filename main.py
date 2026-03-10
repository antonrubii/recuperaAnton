import sys

from PyQt6 import uic
from PyQt6.QtWidgets import QApplication

app = QApplication(sys.argv)

window = uic.loadUi("window.ui")
window.show()

sys.exit(app.exec())