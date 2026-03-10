import sys
from PyQt6 import QtWidgets
from window import Ui_MainWindow
from events import Events

class Main(QtWidgets.QMainWindow):

    def __init__(self):
        super().__init__()

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # conectar menú salir
        self.ui.actionSalir.triggered.connect(Events.salir)

        # validaciones
        self.ui.lineDni.editingFinished.connect(self.checkDni)
        self.ui.lineMovil.editingFinished.connect(self.checkMovil)

    def checkDni(self):
        dni = self.ui.lineDni.text()

        if Events.validarDNI(dni):
            self.ui.lineDni.setStyleSheet("background-color: lightgreen;")
        else:
            self.ui.lineDni.setStyleSheet("background-color: red;")

    def checkMovil(self):
        movil = self.ui.lineMovil.text()

        if Events.validarMovil(movil):
            self.ui.lineMovil.setStyleSheet("background-color: lightgreen;")
        else:
            self.ui.lineMovil.setStyleSheet("background-color: red;")


app = QtWidgets.QApplication(sys.argv)
window = Main()
window.show()

sys.exit(app.exec())