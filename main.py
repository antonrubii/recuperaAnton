import sys
import os
import globals
from PyQt6 import QtWidgets, QtGui
from window import Ui_MainWindow
from events import Events
from usuarios import Usuarios
from conexion import Conexion
from reports import Reports


class Main(QtWidgets.QMainWindow):
    def __init__(self):
        super(Main, self).__init__()
        # Inicializamos la interfaz en la variable global
        globals.ui = Ui_MainWindow()
        globals.ui.setupUi(self)

        # 1. Inicialización de la Base de Datos
        if not os.path.exists('data'):
            os.makedirs('data')
        Conexion.db_connect("data/recupera.db")

        # 2. Instanciar módulos auxiliares
        self.report = Reports()

        # 3. Conexión de Menús y Barra de Herramientas
        globals.ui.actionSalir.triggered.connect(Events.salir)

        # Conexión del Informe PDF (Entrega 3)
        # Asegúrate de haber compilado el .ui para que 'actionListado_empleados' exista
        if hasattr(globals.ui, 'actionListado_empleados'):
            globals.ui.actionListado_empleados.triggered.connect(self.report.reportUsuarios)

        # 4. Conexión de Botones CRUD (Pestaña Usuarios)
        globals.ui.btnAlta.clicked.connect(Usuarios.addUsuario)
        globals.ui.btnModif.clicked.connect(Usuarios.modifUsuario)
        globals.ui.btnBaja.clicked.connect(Usuarios.delUsuario)

        # 5. Eventos de Tabla y Validaciones
        globals.ui.tabUsuarios.clicked.connect(Usuarios.cargarUsuario)

        # Validaciones visuales (cambian el color al terminar de escribir)
        globals.ui.lineDni.editingFinished.connect(self.checkDni)
        globals.ui.lineMovil.editingFinished.connect(self.checkMovil)

        # 6. Carga inicial de datos en la tabla
        Usuarios.cargarTabla()

    # --- MÉTODOS DE VALIDACIÓN VISUAL ---
    def checkDni(self):
        """Llamada a la lógica de validación de DNI en events.py"""
        dni = globals.ui.lineDni.text()
        if Events.validarDNI(dni):
            globals.ui.lineDni.setStyleSheet("background-color: #C8E6C9;")  # Verde éxito
        else:
            globals.ui.lineDni.setStyleSheet("background-color: #FFCDD2;")  # Rojo error
            globals.ui.lineDni.setText("")
            globals.ui.lineDni.setPlaceholderText("DNI INVÁLIDO")

    def checkMovil(self):
        """Llamada a la lógica de validación de Móvil en events.py"""
        movil = globals.ui.lineMovil.text()
        if Events.validarMovil(movil):
            globals.ui.lineMovil.setStyleSheet("background-color: #C8E6C9;")
        else:
            globals.ui.lineMovil.setStyleSheet("background-color: #FFCDD2;")
            globals.ui.lineMovil.setText("")
            globals.ui.lineMovil.setPlaceholderText("Móvil erróneo")


# --- BLOQUE DE EJECUCIÓN PRINCIPAL ---
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)

    # Cargar estilos QSS (opcional, si tienes el archivo styles.qss)
    try:
        ruta_estilo = os.path.join(os.path.dirname(__file__), "styles.qss")
        if os.path.exists(ruta_estilo):
            with open(ruta_estilo, "r", encoding="utf-8") as f:
                app.setStyleSheet(f.read())
    except Exception as e:
        print("Error cargando estilos:", e)

    window = Main()
    window.show()
    sys.exit(app.exec())