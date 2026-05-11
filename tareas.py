import globals
from PyQt6 import QtWidgets, QtCore
from conexion import Conexion


class Tareas:

    @staticmethod
    def cargarTabla():
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

        try:

            # DATOS FORMULARIO
            nombreCliente = globals.ui.lineCliente.text().strip()
            nombreEmpleado = globals.ui.lineEdmpleado.text().strip()

            cliente = Conexion.obtenerIdPorNombre(nombreCliente)
            empleado = Conexion.obtenerIdPorNombre(nombreEmpleado)
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

        globals.ui.lblid.setText("")

        globals.ui.lineCliente.setText("")
        globals.ui.lineEdmpleado.setText("")
        globals.ui.lineServicio.setText("")
        globals.ui.lineHoras.setText("")
        globals.ui.linePrecio_Hora.setText("")

        globals.ui.cmbEstado.setCurrentIndex(0)

    @staticmethod
    def cargarCliente():

        fila = globals.ui.tabUsuarios.currentRow()

        if fila >= 0:
            nombre = globals.ui.tabUsuarios.item(fila, 0).text()

            globals.ui.lineCliente.setText(nombre)

    @staticmethod
    def cargarEmpleado():

        fila = globals.ui.tabUsuarios.currentRow()

        if fila >= 0:
            nombre = globals.ui.tabUsuarios.item(fila, 0).text()

            globals.ui.lineEdmpleado.setText(nombre)