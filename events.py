import sys
import re
from PyQt6 import QtWidgets

class Events:
    @staticmethod
    def salir(event):
        sys.exit()

    @staticmethod
    def acerca_de():
        QtWidgets.QMessageBox.information(None, "Acerca de",
            "Proyecto: recuperaRubinanRoddriguezAnton\n"
            "Autor: Antón Rubiñán\n"
            "Versión: 1.0\n"
            "Fecha: 2026")

    @staticmethod
    def validarDNI(dni):
        """ Algoritmo de validación de NIF (8 números + letra) """
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
        """ Valida que tenga 9 dígitos y empiece por 6 o 7 """
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