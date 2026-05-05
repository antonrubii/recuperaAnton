import globals
from PyQt6 import QtWidgets, QtCore
from conexion import Conexion


class Tareas:
    @staticmethod
    def cargarTabla():
        try:
            # Traemos los datos de la base de datos
            listado = Conexion.listadoTareas()
            globals.ui.tabTareas.setRowCount(0)

            for index, registro in enumerate(listado):
                globals.ui.tabTareas.insertRow(index)

                # registro[0]=id, [1]=cliente, [2]=empleado, [3]=servicio, [4]=horas, [5]=precio
                globals.ui.tabTareas.setItem(index, 0, QtWidgets.QTableWidgetItem(str(registro[0])))
                globals.ui.tabTareas.setItem(index, 1, QtWidgets.QTableWidgetItem(str(registro[1])))
                globals.ui.tabTareas.setItem(index, 2, QtWidgets.QTableWidgetItem(str(registro[2])))
                globals.ui.tabTareas.setItem(index, 3, QtWidgets.QTableWidgetItem(str(registro[3])))

                # Aquí podemos añadir el ESTADO si lo tienes en la BD,
                # si no, lo dejamos vacío o ponemos el dato que corresponda.
                # globals.ui.tabTareas.setItem(index, 4, QtWidgets.QTableWidgetItem("Pendiente"))

                # Cálculo del TOTAL para la columna 5
                total = float(registro[4]) * float(registro[5])
                globals.ui.tabTareas.setItem(index, 5, QtWidgets.QTableWidgetItem(f"{total:.2f} €"))

                # Alineación: ID y números al centro, textos a la izquierda
                globals.ui.tabTareas.item(index, 0).setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
                globals.ui.tabTareas.item(index, 5).setTextAlignment(
                    QtCore.Qt.AlignmentFlag.AlignRight | QtCore.Qt.AlignmentFlag.AlignVCenter)

        except Exception as e:
            print("Error cargando tabla tareas:", e)

    @staticmethod
    def addTarea():
        try:
            # 1. Recuperamos los IDs reales (no los nombres que se ven)
            id_cliente = globals.idCliValido
            id_empleado = globals.idEmpValido

            # 2. Recogemos el resto de datos
            servicio = globals.ui.lineServicio.text()
            horas = globals.ui.lineHoras.text()
            precio = globals.ui.linePrecio_Hora.text()

            # 3. Recogemos el texto del COMBOBOX (Lo que pide el profe)
            estado = globals.ui.cmbEstado.currentText()

            # 4. Validaciones básicas
            if not id_cliente or not id_empleado:
                QtWidgets.QMessageBox.warning(None, "Error", "Selecciona Cliente y Empleado en la pestaña anterior")
                return

            if estado == "":
                QtWidgets.QMessageBox.warning(None, "Error", "Debes seleccionar un estado para la tarea")
                return

            # 5. Guardar en la BD
            # Pasamos: [idCli, idEmp, servicio, horas, precio, estado]
            datos = [id_cliente, id_empleado, servicio, horas, precio, estado]

            if Conexion.addTarea(datos):
                QtWidgets.QMessageBox.information(None, "Éxito", "Tarea guardada correctamente")
                Tareas.cargarTabla()
                # Limpiar tras guardar
                globals.ui.lineServicio.setText("")
                globals.ui.lineHoras.setText("")
                globals.ui.linePrecio_Hora.setText("")
                globals.ui.cmbEstado.setCurrentIndex(0)
            else:
                print("Error al insertar en la base de datos")

        except Exception as e:
            print("Error en addTarea:", e)
    @staticmethod
    def selecTarea():
        """MÉT0DO: selecTarea (según PDF)"""
        try:
            row = globals.ui.tabTareas.currentRow()
            idTarea = globals.ui.tabTareas.item(row, 0).text()
            registro = Conexion.cargarUnaTarea(idTarea)
            if registro:
                globals.ui.lblid.setText(str(registro[0]))  # El label que creaste para el ID
                globals.ui.lineCliente.setText(str(registro[1]))
                globals.ui.lineEdmpleado.setText(str(registro[2]))
                globals.ui.lineServicio.setText(str(registro[3]))
                globals.ui.lineHoras.setText(str(registro[4]))
                globals.ui.linePrecio_Hora.setText(str(registro[5]))
        except Exception as e:
            print("Error seleccionando tarea", e)

    @staticmethod
    def delTarea():
        idTarea = globals.ui.lblid.text()
        if idTarea and Conexion.delTarea(idTarea):
            QtWidgets.QMessageBox.information(None, "Ok", "Tarea eliminada")
            Tareas.cargarTabla()

    @staticmethod
    def modifTarea():
        idTarea = globals.ui.lblid.text()
        datos = [
            idTarea,
            globals.ui.lineCliente.text(),
            globals.ui.lineEdmpleado.text(),
            globals.ui.lineServicio.text(),
            globals.ui.lineHoras.text(),
            globals.ui.linePrecio_Hora.text()
        ]
        if Conexion.modifTarea(datos):
            QtWidgets.QMessageBox.information(None, "Ok", "Tarea modificada")
            Tareas.cargarTabla()

    @staticmethod
    def validarCampos():
        # Validaciones de tipos numéricos
        try:
            float(globals.ui.lineHoras.text())
            float(globals.ui.linePrecio_Hora.text())
        except:
            QtWidgets.QMessageBox.warning(None, "Error", "Horas y Precio deben ser números")
            return False

        if not globals.ui.lineCliente.text() or not globals.ui.lineEdmpleado.text():
            QtWidgets.QMessageBox.warning(None, "Error", "Cliente y Empleado son obligatorios")
            return False
        return True