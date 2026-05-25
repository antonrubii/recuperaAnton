"""
Módulo de Gestión de Usuarios.

Maneja el comportamiento y eventos de la pestaña de administración de usuarios.
Se encarga de procesar las altas, modificaciones, bajas y cargas de registros personales.
"""
import globals
from PyQt6 import QtWidgets, QtCore
from conexion import Conexion


class Usuarios:
    """
        Clase encargada de coordinar las interacciones CRUD aplicadas al personal o clientes.
        """
    @staticmethod
    def limpiarCampos():
        """
                Limpia las cajas de entrada de texto del panel de usuarios a su estado original.
                """
        globals.ui.lineDni.setText("")
        globals.ui.lineNombre.setText("")
        globals.ui.lineDireccion.setText("")
        globals.ui.lineEmail.setText("")
        globals.ui.lineMovil.setText("")
        globals.ui.lineDni.setEnabled(True)
        globals.ui.lineDni.setStyleSheet("background-color: white;")

    @staticmethod
    def cargarTabla(tipo="Todos"):

        """
        Repopula la cuadrícula visual de usuarios ('tabUsuarios') solicitando el listado
        actualizado a la capa de datos.
        """
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
        """
                Recoge las variables personales del formulario de usuarios, realiza el alta en
                base de datos y actualiza los componentes visuales pertinentes.
                """
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
        """
                Se ejecuta al pinchar una fila en 'tabUsuarios'. Obtiene el DNI seleccionado,
                busca el registro completo y rellena los lineEdits del formulario de Usuarios.
                """
        try:
            # 1. Obtenemos la fila seleccionada en la tabla
            row = globals.ui.tabUsuarios.currentRow()
            if row < 0: return

            # 2. Extraemos el DNI de la Columna 1
            item_dni = globals.ui.tabUsuarios.item(row, 1)
            if item_dni is None: return
            dni = item_dni.text()

            # 3. Consultamos la BD para traer el registro completo
            registro = Conexion.cargarUnUsuario(dni)

            if registro:
                # --- RELLENAR PESTAÑA USUARIOS (Asegúrate de que no falte nada) ---
                # registro traído de la BD: [0:dni, 1:nombre, 2:dir, 3:email, 4:movil, 5:tipo]
                globals.ui.lineDni.setText(str(registro[0]))
                globals.ui.lineNombre.setText(str(registro[1]))
                globals.ui.lineDireccion.setText(str(registro[2]))
                globals.ui.lineEmail.setText(str(registro[3]))
                globals.ui.lineMovil.setText(str(registro[4]))
                globals.ui.cmbTipo.setCurrentText(str(registro[5]))

                # Bloqueo estético del DNI para que no se cambie al editar
                globals.ui.lineDni.setEnabled(False)
                globals.ui.lineDni.setStyleSheet("background-color: #f0f0f0;")

                # --- SINCRONIZAR CON PESTAÑA TAREAS ---
                tipo = str(registro[5])  # "Cliente" o "Empleado"
                nombre = str(registro[1])  # Nombre de la persona

                # Buscamos el ID numérico que le corresponde a este DNI en la base de datos
                id_num = Conexion.obtenerIdPorDni(dni)

                if tipo == "Cliente":
                    globals.ui.lineCliente.setText(nombre)  # Ponemos el nombre en el campo Cliente
                    globals.idCliValido = id_num  # Guardamos el ID en la variable global
                elif tipo == "Empleado":
                    globals.ui.lineEdmpleado.setText(nombre)  # Ponemos el nombre en el campo Empleado
                    globals.idEmpValido = id_num  # Guardamos el ID en la variable global

                # --- ASIGNAR ID DE TAREA (Sugerencia del siguiente número) ---
                proximo_id = Conexion.proximoIdTarea()
                globals.ui.lblid.setText(str(proximo_id))
                globals.ui.lblid.setStyleSheet("color: #007AFF; font-weight: bold; font-size: 14px;")

        except Exception as e:
            print("Error en cargarUsuario:", e)
    @staticmethod
    def delUsuario():
        """
                Elimina el usuario activo basándose en el DNI presente en el formulario de la ventana.
                """
        dni = globals.ui.lineDni.text()
        if not dni: return
        if Conexion.delUsuario(dni):
            QtWidgets.QMessageBox.information(None, "Aviso", "Usuario borrado")
            Usuarios.cargarTabla()
            Usuarios.limpiarCampos()

    @staticmethod
    def modifUsuario():
        """
                Envía los valores modificados del formulario a la base de datos basándose en el
                DNI y refresca el grid.
                """
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