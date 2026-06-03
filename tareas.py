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
            from PyQt6 import QtGui, QtCore, QtWidgets

            listado = Conexion.listadoTareas()
            globals.ui.tabTareas.setRowCount(0)

            for index, registro in enumerate(listado):
                globals.ui.tabTareas.insertRow(index)

                # 🔍 Capturamos el estado de forma segura (posición 6 de la base de datos)
                estado_texto = str(registro[6]).strip() if len(registro) > 6 and registro[
                    6] is not None else "pendiente"
                estado_lower = estado_texto.lower()

                # Creamos los ítems uno a uno utilizando variables
                item_id = QtWidgets.QTableWidgetItem(str(registro[0]))
                item_cliente = QtWidgets.QTableWidgetItem(str(registro[1]))
                item_empleado = QtWidgets.QTableWidgetItem(str(registro[2]))
                item_servicio = QtWidgets.QTableWidgetItem(str(registro[3]))

                # Horas
                item_horas = QtWidgets.QTableWidgetItem(str(registro[4]))

                # NUEVA COLUMNA VISUAL: Estado
                item_estado = QtWidgets.QTableWidgetItem(estado_texto)

                # Total calculado (Precio * Horas)
                total = float(registro[4]) * float(registro[5])
                item_total = QtWidgets.QTableWidgetItem(f"{total:.2f} €")

                # Metemos todos los ítems de esta fila en una lista para aplicarles el color de golpe
                items_fila = [item_id, item_cliente, item_empleado, item_servicio, item_horas, item_estado, item_total]

                # 🔥 SI ESTÁ PENDIENTE, TODA LA FILA SE PONE EN ROJO PASTEL
                if estado_lower == "pendiente":
                    for item in items_fila:
                        item.setBackground(QtGui.QColor(255, 204, 204))  # Fondo rojo suave
                        item.setForeground(QtGui.QColor("black"))  # Letra negra clara

                # Asignamos los ítems a sus respectivas columnas (0 a 6)
                globals.ui.tabTareas.setItem(index, 0, item_id)
                globals.ui.tabTareas.setItem(index, 1, item_cliente)
                globals.ui.tabTareas.setItem(index, 2, item_empleado)
                globals.ui.tabTareas.setItem(index, 3, item_servicio)
                globals.ui.tabTareas.setItem(index, 4, item_horas)
                globals.ui.tabTareas.setItem(index, 5, item_estado)  # Columna 5: Estado
                globals.ui.tabTareas.setItem(index, 6, item_total)  # Columna 6: Total (€)

                # Alineaciones (usando tus variables de forma segura)
                item_id.setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
                item_horas.setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
                item_estado.setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
                item_total.setTextAlignment(
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
                globals.ui.lineCliente.setText(str(registro[1]))
                globals.ui.lineEdmpleado.setText(str(registro[2]))
                globals.ui.lineServicio.setText(str(registro[3]))
                globals.ui.lineHoras.setText(str(registro[4]))
                globals.ui.linePrecio_Hora.setText(str(registro[5]))

                # 🎯 ¡AHORA SÍ! Como conexion.py ya devuelve el estado, lo leemos directamente:
                estado_real = str(registro[6]).strip()

                # Seteamos el combobox con el valor real ("en curso", "pendiente", "finalizado", etc.)
                globals.ui.cmbEstado.setCurrentText(estado_real)

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
        try:
            # 1. Recuperamos el ID de la tarea
            idTarea = globals.ui.lblid.text().strip()

            # 2. Recuperamos los textos de los campos de la pantalla
            nombreCliente = globals.ui.lineCliente.text().strip()
            nombreEmpleado = globals.ui.lineEdmpleado.text().strip()

            servicio = globals.ui.lineServicio.text().strip()
            horas = globals.ui.lineHoras.text().strip()
            precio = globals.ui.linePrecio_Hora.text().strip()
            estado = globals.ui.cmbEstado.currentText().strip()

            # ==========================================================
            # 🔍 ESTRATEGIA INTELIGENTE: ¿Es ya un ID numérico o es un Nombre?
            # ==========================================================
            # Para el Cliente:
            if nombreCliente.isdigit():
                cliente = int(nombreCliente)  # Si es un número (ej: "1"), lo usamos directamente
            else:
                cliente = Conexion.obtenerIdPorNombre(nombreCliente)  # Si es texto, buscamos su ID

            # Para el Empleado:
            if nombreEmpleado.isdigit():
                empleado = int(nombreEmpleado)
            else:
                empleado = Conexion.obtenerIdPorNombre(nombreEmpleado)
            # ==========================================================

            # Controles de seguridad descriptivos
            if not cliente:
                QtWidgets.QMessageBox.warning(
                    None, "Error", f"No se pudo validar el cliente '{nombreCliente}'."
                )
                return

            if not empleado:
                QtWidgets.QMessageBox.warning(
                    None, "Error", f"No se pudo validar el empleado '{nombreEmpleado}'."
                )
                return

            if not servicio:
                QtWidgets.QMessageBox.warning(None, "Error", "Servicio obligatorio")
                return

            try:
                horas_float = float(horas)
                precio_float = float(precio)
            except ValueError:
                QtWidgets.QMessageBox.warning(None, "Error", "Horas o Precio incorrectos")
                return

            # 3. Empaquetamos los 7 datos para conexion.py
            row = [idTarea, cliente, empleado, servicio, horas_float, precio_float, estado]

            if idTarea != "":
                if Conexion.modifTarea(row):
                    QtWidgets.QMessageBox.information(None, "Éxito", "Tarea modificada con éxito")
                    Tareas.cargarTabla()
                    Tareas.limpiarFormulario()
                else:
                    QtWidgets.QMessageBox.warning(None, "Error", "No se pudo modificar en la base de datos")
            else:
                QtWidgets.QMessageBox.warning(None, "Aviso", "No se ha seleccionado ninguna tarea para modificar")

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