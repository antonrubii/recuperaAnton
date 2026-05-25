"""
Módulo de Gestión de Tareas.

Controla el comportamiento visual de la pestaña Tareas, procesando la
recogida de datos desde el formulario de la interfaz y la sincronización con la tabla.
"""

import globals
from PyQt6 import QtWidgets, QtCore
from conexion import Conexion


class Tareas:
    """
        Clase contenedora de la lógica operativa (CRUD) de las Tareas de la aplicación.
        """

    @staticmethod
    def cargarTabla():

        """
                Limpia la tabla gráfica 'tabTareas' y añade las filas correspondientes
                con los datos vigentes extraídos desde la base de datos.
                """
        try:
            listado = Conexion.listadoTareas()
            globals.ui.tabTareas.setRowCount(0)

            for index, registro in enumerate(listado):

                globals.ui.tabTareas.insertRow(index)

                # COLUMNAS
                # 0 ID
                # 1 CLIENTE
                # 2 EMPLEADO
                # 3 SERVICIO
                # 4 HORAS
                # 5 PRECIO

                globals.ui.tabTareas.setItem(
                    index, 0,
                    QtWidgets.QTableWidgetItem(str(registro[0]))
                )

                globals.ui.tabTareas.setItem(
                    index, 1,
                    QtWidgets.QTableWidgetItem(str(registro[1]))
                )

                globals.ui.tabTareas.setItem(
                    index, 2,
                    QtWidgets.QTableWidgetItem(str(registro[2]))
                )

                globals.ui.tabTareas.setItem(
                    index, 3,
                    QtWidgets.QTableWidgetItem(str(registro[3]))
                )

                total = float(registro[4]) * float(registro[5])

                globals.ui.tabTareas.setItem(
                    index, 4,
                    QtWidgets.QTableWidgetItem(str(registro[4]))
                )

                globals.ui.tabTareas.setItem(
                    index, 5,
                    QtWidgets.QTableWidgetItem(f"{total:.2f} €")
                )

                # alineación
                globals.ui.tabTareas.item(
                    index, 0
                ).setTextAlignment(
                    QtCore.Qt.AlignmentFlag.AlignCenter
                )

                globals.ui.tabTareas.item(
                    index, 5
                ).setTextAlignment(
                    QtCore.Qt.AlignmentFlag.AlignRight |
                    QtCore.Qt.AlignmentFlag.AlignVCenter
                )

        except Exception as e:
            print("Error cargando tareas:", e)

    @staticmethod
    def addTarea():
        """
                Captura la información de los campos de texto e inserta la nueva tarea en la BD.
                Vuelve a refrescar la tabla al finalizar.
                """
        try:

            # DATOS FORMULARIO
            nombreCliente = globals.ui.lineCliente.text().strip()
            nombreEmpleado = globals.ui.lineEdmpleado.text().strip()

            cliente = Conexion.obtenerIdPorNombre(nombreCliente)
            empleado = Conexion.obtenerIdPorNombre(nombreEmpleado)
            print("CLIENTE TEXTO:", nombreCliente)
            print("CLIENTE ID:", cliente)

            print("EMPLEADO TEXTO:", nombreEmpleado)
            print("EMPLEADO ID:", empleado)
            servicio = globals.ui.lineServicio.text().strip()
            horas = globals.ui.lineHoras.text().strip()
            precio = globals.ui.linePrecio_Hora.text().strip()
            estado = globals.ui.cmbEstado.currentText()

            # VALIDACIONES
            if not cliente:
                QtWidgets.QMessageBox.warning(
                    None,
                    "Error",
                    "Cliente obligatorio"
                )
                return

            if not empleado:
                QtWidgets.QMessageBox.warning(
                    None,
                    "Error",
                    "Empleado obligatorio"
                )
                return

            if not servicio:
                QtWidgets.QMessageBox.warning(
                    None,
                    "Error",
                    "Servicio obligatorio"
                )
                return

            if estado == "":
                QtWidgets.QMessageBox.warning(
                    None,
                    "Error",
                    "Selecciona un estado"
                )
                return

            # VALIDAR HORAS
            try:
                horas_float = float(horas)

                if horas_float <= 0:
                    raise ValueError

            except:
                QtWidgets.QMessageBox.warning(
                    None,
                    "Error",
                    "Horas incorrectas"
                )
                return

            # VALIDAR PRECIO
            try:
                precio_float = float(precio)

                if precio_float < 0:
                    raise ValueError

            except:
                QtWidgets.QMessageBox.warning(
                    None,
                    "Error",
                    "Precio incorrecto"
                )
                return

            # DATOS A INSERTAR
            datos = [
                cliente,
                empleado,
                servicio,
                horas_float,
                precio_float,
                estado
            ]

            # INSERT BD
            if Conexion.addTarea(datos):

                QtWidgets.QMessageBox.information(
                    None,
                    "OK",
                    "Tarea guardada correctamente"
                )

                Tareas.cargarTabla()
                Tareas.limpiarFormulario()

            else:

                QtWidgets.QMessageBox.warning(
                    None,
                    "Error",
                    "No se pudo guardar la tarea"
                )

        except Exception as e:
            print("Error addTarea:", e)

    @staticmethod
    def selecTarea():
        """
                Evento disparado al hacer clic en una fila de la tabla de tareas.
                Extrae la información de las celdas de dicha fila y la proyecta en los inputs de arriba.
                """

        try:

            fila = globals.ui.tabTareas.currentRow()

            if fila < 0:
                return

            idTarea = globals.ui.tabTareas.item(fila, 0).text()

            registro = Conexion.cargarUnaTarea(idTarea)

            if registro:

                globals.ui.lblid.setText(str(registro[0]))

                globals.ui.lineCliente.setText(
                    str(registro[1])
                )

                globals.ui.lineEdmpleado.setText(
                    str(registro[2])
                )

                globals.ui.lineServicio.setText(
                    str(registro[3])
                )

                globals.ui.lineHoras.setText(
                    str(registro[4])
                )

                globals.ui.linePrecio_Hora.setText(
                    str(registro[5])
                )

        except Exception as e:
            print("Error seleccionando tarea:", e)

    @staticmethod
    def delTarea():
        """
                Elimina la tarea apuntada por el label identificador y limpia el formulario visual.
                """

        try:

            idTarea = globals.ui.lblid.text()

            if not idTarea:
                QtWidgets.QMessageBox.warning(
                    None,
                    "Error",
                    "Selecciona una tarea"
                )
                return

            respuesta = QtWidgets.QMessageBox.question(
                None,
                "Confirmar",
                "¿Eliminar tarea?"
            )

            if respuesta == QtWidgets.QMessageBox.StandardButton.Yes:

                if Conexion.delTarea(idTarea):

                    QtWidgets.QMessageBox.information(
                        None,
                        "OK",
                        "Tarea eliminada"
                    )

                    Tareas.cargarTabla()
                    Tareas.limpiarFormulario()

        except Exception as e:
            print("Error eliminando tarea:", e)

    @staticmethod
    def modifTarea():
        """
                Lee el ID activo del label y actualiza la tarea correspondiente en la BD
                con los nuevos valores introducidos en el formulario.
                """

        try:

            idTarea = globals.ui.lblid.text()

            if not idTarea:
                QtWidgets.QMessageBox.warning(
                    None,
                    "Error",
                    "Selecciona una tarea"
                )
                return

            cliente = globals.ui.lineCliente.text().strip()
            empleado = globals.ui.lineEdmpleado.text().strip()
            servicio = globals.ui.lineServicio.text().strip()
            horas = globals.ui.lineHoras.text().strip()
            precio = globals.ui.linePrecio_Hora.text().strip()

            datos = [
                idTarea,
                cliente,
                empleado,
                servicio,
                horas,
                precio
            ]

            if Conexion.modifTarea(datos):

                QtWidgets.QMessageBox.information(
                    None,
                    "OK",
                    "Tarea modificada"
                )

                Tareas.cargarTabla()

        except Exception as e:
            print("Error modificando tarea:", e)

    @staticmethod
    def limpiarFormulario():
        """
                Restablece todos los inputs y el combobox de la pestaña tareas dejándolos vacíos.
                """

        globals.ui.lblid.setText("")

        globals.ui.lineCliente.setText("")
        globals.ui.lineEdmpleado.setText("")
        globals.ui.lineServicio.setText("")
        globals.ui.lineHoras.setText("")
        globals.ui.linePrecio_Hora.setText("")

        globals.ui.cmbEstado.setCurrentIndex(0)

    @staticmethod
    def cargarCliente():
        """
                       Carga el Cliente seleccionado en la tabla
                       """

        fila = globals.ui.tabUsuarios.currentRow()

        if fila >= 0:
            nombre = globals.ui.tabUsuarios.item(fila, 0).text()

            globals.ui.lineCliente.setText(nombre)

    @staticmethod
    def cargarEmpleado():
        """
                      Carga el Empleado seleccionado en la tabla
                       """

        fila = globals.ui.tabUsuarios.currentRow()

        if fila >= 0:
            nombre = globals.ui.tabUsuarios.item(fila, 0).text()

            globals.ui.lineEdmpleado.setText(nombre)