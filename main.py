import sys
import globals
from PyQt6 import QtWidgets
from window import Ui_MainWindow
from events import Events
from usuarios import Usuarios  # Importamos la lógica de usuarios
from conexion import Conexion # Importamos la conexión

class Main(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        globals.ui = Ui_MainWindow()
        globals.ui.setupUi(self)

        # 1. Inicializar la base de datos
        # Creamos la carpeta data si no existe y conectamos
        import os
        if not os.path.exists('data'):
            os.makedirs('data')
        Conexion.db_connect("data/recupera.db")

        # 2. Conectar menús
        globals.ui.actionSalir.triggered.connect(Events.salir)
        globals.ui.menuAcerca_de.aboutToShow.connect(Events.acerca_de)

        # 3. Conectar botones del CRUD (Usuarios)
        globals.ui.btnAlta.clicked.connect(Usuarios.addUsuario)
        globals.ui.btnModif.clicked.connect(Usuarios.modifUsuario)
        globals.ui.btnBaja.clicked.connect(Usuarios.delUsuario)

        # 4. Eventos de la Tabla y Validaciones
        globals.ui.tabUsuarios.clicked.connect(Usuarios.selUsuario)
        globals.ui.lineDni.editingFinished.connect(self.checkDni)
        globals.ui.lineMovil.editingFinished.connect(self.checkMovil)
        globals.ui.tabUsuarios.clicked.connect(Usuarios.cargarUsuario)


        # 5. Cargar la tabla al iniciar
        Usuarios.cargarTabla()

        globals.ui.tabUsuarios.clicked.connect(Usuarios.cargarUsuario)

    def checkDni(self):
        dni = globals.ui.lineDni.text()
        if Events.validarDNI(dni):
            globals.ui.lineDni.setStyleSheet("background-color: #C8E6C9;")
        else:
            globals.ui.lineDni.setStyleSheet("background-color: #FFCDD2;")
            globals.ui.lineDni.setText("")
            globals.ui.lineDni.setPlaceholderText("DNI INVÁLIDO")

    def checkMovil(self):
        movil = globals.ui.lineMovil.text()
        if Events.validarMovil(movil):
            globals.ui.lineMovil.setStyleSheet("background-color: #C8E6C9;")
        else:
            globals.ui.lineMovil.setStyleSheet("background-color: #FFCDD2;")
            globals.ui.lineMovil.setText("")
            globals.ui.lineMovil.setPlaceholderText("Móvil erróneo")

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = Main()
    window.show()
    sys.exit(app.exec())