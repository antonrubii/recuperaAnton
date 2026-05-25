"""
Módulo de Eventos y Funciones Auxiliares Generales.

Proporciona utilidades globales como validación sintáctica de datos de entrada
(DNI, Teléfono) y el control de salida segura de la aplicación.
"""
import sys
import re
from PyQt6 import QtWidgets

class Events:
    """
        Clase contenedora de validaciones algorítmicas y flujos genéricos del sistema.
        """
    @staticmethod
    def salir(event):
        """
                Finaliza de manera ordenada y segura la ejecución de la aplicación.
                """
        sys.exit()

    @staticmethod
    def acerca_de():
        """
                       Muestra los nombre del proyecto ,  version, fecha y datos dew quien creó el programa
                        """
        QtWidgets.QMessageBox.information(None, "Acerca de",
            "Proyecto: recuperaRubinanRoddriguezAnton\n"
            "Autor: Antón Rubiñán\n"
            "Versión: 1.0\n"
            "Fecha: 2026")

    @staticmethod
    def validarDNI(dni):
        """
                Verifica matemáticamente la validez de un DNI español.
        Format regular de 8 números junto a una letra, calculando si la letra coincide.
        """

        try:
            tabla = "TRWAGMYFPDXBNJZSQVHLCKE"
            dni = dni.upper()
            if len(dni) == 9:
                letra = dni[8]
                numeros = dni[:8]
                if numeros.isdigit() and tabla[int(numeros) % 23] == letra:
                    return True
            return False
        except Exception as e:
            print("Error validando DNI", e)
            return False

    @staticmethod
    def validarMovil(telefono):
        """
        Valida mediante expresiones regulares si una cadena de texto sigue el patrón
        de un teléfono móvil estándar español.
        """
        return bool(re.match(r"^[67]\d{8}$", telefono))

    def resizeTabCustomer(self):

        try:
            # Esto quita las líneas feas de la tabla y la hace parecer una lista web
            globals.ui.tabUsuarios.setShowGrid(False)  # <--- CRÍTICO
            globals.ui.tabUsuarios.setAlternatingRowColors(True)
            globals.ui.tabUsuarios.verticalHeader().setVisible(False)  # Quita los números de fila (1, 2, 3...)

            # Ajusta el ancho para que no haya huecos blancos
            header = globals.ui.tabUsuarios.horizontalHeader()
            header.setSectionResizeMode(QtWidgets.QHeaderView.ResizeMode.Stretch)
        except Exception as e:
            print(e)