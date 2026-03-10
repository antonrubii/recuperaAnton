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