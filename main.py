import sys
import os
from PyQt6 import QtWidgets
import globals
from window import Ui_MainWindow
from events import Events
from usuarios import Usuarios
from conexion import Conexion


class Main(QtWidgets.QMainWindow):
    def __init__(self):
        super(Main, self).__init__()
        globals.ui = Ui_MainWindow()
        globals.ui.setupUi(self)

        # --- CARGAR ESTILOS CSS ---
        self.load_stylesheet()

        # 1. Inicialización de la Base de Datos
        if not os.path.exists('data'):
            os.makedirs('data')
        # Conectamos a la base de datos
        Conexion.db_connect("data/recupera.db")

        # 2. Conexión de Menús
        globals.ui.actionSalir.triggered.connect(Events.salir)
        # Nota: Usamos aboutToShow para menús que no tienen sub-opciones
        globals.ui.menuAcerca_de.aboutToShow.connect(Events.acerca_de)

        # 3. Conexión de Botones CRUD (Usuarios)
        globals.ui.btnAlta.clicked.connect(Usuarios.addUsuario)
        globals.ui.btnModif.clicked.connect(Usuarios.modifUsuario)
        globals.ui.btnBaja.clicked.connect(Usuarios.delUsuario)

        # Opcional: Si tienes un botón para limpiar campos, conéctalo aquí
        # globals.ui.btnLimpiar.clicked.connect(Usuarios.limpiarCampos)

        # 4. Eventos de Tabla y Validaciones
        # IMPORTANTE: Aquí corregimos el error. Usamos Usuarios.cargarUsuario
        globals.ui.tabUsuarios.clicked.connect(Usuarios.cargarUsuario)

        globals.ui.lineDni.editingFinished.connect(self.checkDni)
        globals.ui.lineMovil.editingFinished.connect(self.checkMovil)

        # 5. Carga inicial de datos
        Usuarios.cargarTabla()

    # --- Métodos de validación visual ---
    def checkDni(self):
        dni = globals.ui.lineDni.text()
        if Events.validarDNI(dni):
            globals.ui.lineDni.setStyleSheet("background-color: #C8E6C9;")  # Verde
        else:
            globals.ui.lineDni.setStyleSheet("background-color: #FFCDD2;")  # Rojo
            globals.ui.lineDni.setText("")
            globals.ui.lineDni.setPlaceholderText("DNI INCORRECTO")

    def checkMovil(self):
        movil = globals.ui.lineMovil.text()
        if Events.validarMovil(movil):
            globals.ui.lineMovil.setStyleSheet("background-color: #C8E6C9;")
        else:
            globals.ui.lineMovil.setStyleSheet("background-color: #FFCDD2;")
            globals.ui.lineMovil.setText("")
            globals.ui.lineMovil.setPlaceholderText("Móvil erróneo")

    def load_stylesheet(self):
        try:
            with open("styles.qss", "r") as f:
                style = f.read()
                self.setStyleSheet(style)
        except Exception as e:
            print("No se pudo cargar el archivo de estilos:", e)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)

    # Intentamos cargar el archivo CSS
    try:
        # Forzamos la ruta para que encuentre el archivo styles.qss
        ruta_estilo = os.path.join(os.path.dirname(__file__), "styles.qss")
        if os.path.exists(ruta_estilo):
            with open(ruta_estilo, "r", encoding="utf-8") as f:
                app.setStyleSheet(f.read())
            print("Estilo cargado con éxito")
        else:
            print(f"Error: No se encuentra el archivo en {ruta_estilo}")
    except Exception as e:
        print("Error cargando estilos:", e)

    window = Main()
    window.show()
    sys.exit(app.exec())