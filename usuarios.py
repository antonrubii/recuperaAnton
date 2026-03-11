import globals
from PyQt6 import QtWidgets, QtCore
from conexion import Conexion


class Usuarios:
    @staticmethod
    def limpiarCampos():
        """Limpia los campos del formulario"""
        globals.ui.lineDni.setText("")
        globals.ui.lineNombre.setText("")
        globals.ui.lineDireccion.setText("")
        globals.ui.lineEmail.setText("")
        globals.ui.lineMovil.setText("")
        globals.ui.lineDni.setStyleSheet("background-color: white;")
        globals.ui.lineMovil.setStyleSheet("background-color: white;")

    @staticmethod
    def cargarTabla():
        """Refresca la tabla con los datos de la BD"""
        try:
            # Puedes filtrar según el combo si quieres (Opcional para nota)
            listado = Conexion.listadoUsuarios("Todos")
            globals.ui.tabUsuarios.setRowCount(0)
            for index, registro in enumerate(listado):
                globals.ui.tabUsuarios.insertRow(index)
                for col, dato in enumerate(registro):
                    globals.ui.tabUsuarios.setItem(index, col, QtWidgets.QTableWidgetItem(str(dato)))
        except Exception as e:
            print("Error cargando tabla", e)

    @staticmethod
    def addUsuario():
        """Guarda un nuevo usuario"""
        if not Usuarios.validarCampos(): return

        datos = [
            globals.ui.lineDni.text(),
            globals.ui.lineNombre.text(),
            globals.ui.lineDireccion.text(),
            globals.ui.lineEmail.text(),
            globals.ui.lineMovil.text(),
            globals.ui.cmbTipo.currentText()
        ]

        if Conexion.addUsuario(datos):
            QtWidgets.QMessageBox.information(None, "Éxito", "Usuario guardado correctamente")
            Usuarios.cargarTabla()
            Usuarios.limpiarCampos()
        else:
            QtWidgets.QMessageBox.warning(None, "Error", "No se pudo guardar. ¿DNI duplicado?")

    @staticmethod
    def selUsuario():
        """Carga los datos de la fila seleccionada en el formulario"""
        try:
            row = globals.ui.tabUsuarios.currentRow()
            dni = globals.ui.tabUsuarios.item(row, 1).text()  # Columna 1 es DNI según tu UI
            registro = Conexion.cargarUnUsuario(dni)
            if registro:
                globals.ui.lineDni.setText(str(registro[0]))
                globals.ui.lineNombre.setText(str(registro[1]))
                globals.ui.lineDireccion.setText(str(registro[2]))
                globals.ui.lineEmail.setText(str(registro[3]))
                globals.ui.lineMovil.setText(str(registro[4]))
                globals.ui.cmbTipo.setCurrentText(str(registro[5]))
        except Exception as e:
            print("Error seleccionando usuario", e)

    @staticmethod
    def delUsuario():
        """Borra el usuario del DNI actual"""
        dni = globals.ui.lineDni.text()
        if not dni: return

        mbox = QtWidgets.QMessageBox.question(None, "Confirmar", f"¿Borrar al usuario {dni}?",
                                              QtWidgets.QMessageBox.StandardButton.Yes |
                                              QtWidgets.QMessageBox.StandardButton.No)

        if mbox == QtWidgets.QMessageBox.StandardButton.Yes:
            if Conexion.delUsuario(dni):
                QtWidgets.QMessageBox.information(None, "Ok", "Usuario eliminado")
                Usuarios.cargarTabla()
                Usuarios.limpiarCampos()

    @staticmethod
    def modifUsuario():
        """Actualiza los datos del usuario"""
        dni = globals.ui.lineDni.text()
        datos = [
            dni,
            globals.ui.lineNombre.text(),
            globals.ui.lineDireccion.text(),
            globals.ui.lineEmail.text(),
            globals.ui.lineMovil.text(),
            globals.ui.cmbTipo.currentText()
        ]

        if Conexion.modifUsuario(datos):
            QtWidgets.QMessageBox.information(None, "Ok", "Datos actualizados")
            Usuarios.cargarTabla()

    @staticmethod
    def validarCampos():
        if not globals.ui.lineNombre.text() or not globals.ui.lineEmail.text() or not globals.ui.lineDni.text():
            QtWidgets.QMessageBox.warning(None, "Campos obligatorios", "Nombre, Email y DNI son necesarios")
            return False
        return True