import globals
from PyQt6 import QtWidgets, QtCore
from conexion import Conexion


class Usuarios:
    @staticmethod
    def limpiarCampos():
        globals.ui.lineDni.setText("")
        globals.ui.lineNombre.setText("")
        globals.ui.lineDireccion.setText("")
        globals.ui.lineEmail.setText("")
        globals.ui.lineMovil.setText("")
        globals.ui.lineDni.setEnabled(True)
        globals.ui.lineDni.setStyleSheet("background-color: white;")

    @staticmethod
    def cargarTabla(tipo="Todos"):
        """Renderizado dinámico de la tabla"""
        try:
            listado = Conexion.listadoUsuarios(tipo)
            globals.ui.tabUsuarios.setRowCount(0)
            for index, registro in enumerate(listado):
                globals.ui.tabUsuarios.insertRow(index)
                for col, dato in enumerate(registro):
                    globals.ui.tabUsuarios.setItem(index, col, QtWidgets.QTableWidgetItem(str(dato)))
        except Exception as e:
            print("Error cargando tabla", e)

    @staticmethod
    def addUsuario():
        if not Usuarios.validarCampos(): return

        datos = [
            globals.ui.lineNombre.text(),
            globals.ui.lineDni.text(),
            globals.ui.lineDireccion.text(),
            globals.ui.lineEmail.text(),
            globals.ui.lineMovil.text(),
            globals.ui.cmbTipo.currentText()
        ]

        if Conexion.addUsuario(datos):
            QtWidgets.QMessageBox.information(None, "Aviso", "Usuario guardado")
            Usuarios.cargarTabla()
            Usuarios.limpiarCampos()
        else:
            QtWidgets.QMessageBox.warning(None, "Error", "DNI repetido o error en BD")

        # usuarios.py (al final de la clase Usuarios)

    @staticmethod
    def cargarUsuario():
            try:
                row = globals.ui.tabUsuarios.currentRow()
                if row < 0: return

                # El DNI está en la columna 1 (Asegúrate de que en la tabla el DNI sea la col 1)
                dni = globals.ui.tabUsuarios.item(row, 1).text()
                registro = Conexion.cargarUnUsuario(dni)

                if registro:
                    globals.ui.lineDni.setText(str(registro[0]))
                    globals.ui.lineNombre.setText(str(registro[1]))
                    globals.ui.lineDireccion.setText(str(registro[2]))
                    globals.ui.lineEmail.setText(str(registro[3]))
                    globals.ui.lineMovil.setText(str(registro[4]))
                    globals.ui.cmbTipo.setCurrentText(str(registro[5]))

                    # Bloqueo para evitar editar la clave primaria
                    globals.ui.lineDni.setEnabled(False)
                    globals.ui.lineDni.setStyleSheet("background-color: #e1e1e1;")
            except Exception as e:
                print("Error en cargarUsuario:", e)
    @staticmethod
    def delUsuario():
        dni = globals.ui.lineDni.text()
        if not dni: return
        if Conexion.delUsuario(dni):
            QtWidgets.QMessageBox.information(None, "Aviso", "Usuario borrado")
            Usuarios.cargarTabla()
            Usuarios.limpiarCampos()

    @staticmethod
    def modifUsuario():
        datos = [
            globals.ui.lineDni.text(),
            globals.ui.lineNombre.text(),
            globals.ui.lineDireccion.text(),
            globals.ui.lineEmail.text(),
            globals.ui.lineMovil.text(),
            globals.ui.cmbTipo.currentText()
        ]
        if Conexion.modifUsuario(datos):
            QtWidgets.QMessageBox.information(None, "Aviso", "Usuario modificado")
            Usuarios.cargarTabla()

    @staticmethod
    def validarCampos():
        nombre = globals.ui.lineNombre.text()
        email = globals.ui.lineEmail.text()
        tipo = globals.ui.cmbTipo.currentText()

        if not nombre or not email or not tipo:
            QtWidgets.QMessageBox.warning(None, "Validación", "Nombre, Email y Tipo son obligatorios")
            return False
        return True