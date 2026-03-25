from PyQt6 import QtSql, QtWidgets

class Conexion:
    @staticmethod
    def db_connect(filename):
        db = QtSql.QSqlDatabase.addDatabase('QSQLITE')
        db.setDatabaseName(filename)
        if not db.open():
            QtWidgets.QMessageBox.critical(None, 'Error', 'No se pudo abrir la base de datos')
            return False
        return True

    @staticmethod
    def addUsuario(nuevoUser):
        query = QtSql.QSqlQuery()
        query.prepare("INSERT INTO usuarios (nombre, dni, direccion, email, movil, tipo) "
                      "VALUES (:nombre, :dni, :dir, :mail, :movil, :tipo)")
        query.bindValue(":nombre", nuevoUser[0])
        query.bindValue(":dni", nuevoUser[1])
        query.bindValue(":dir", nuevoUser[2])
        query.bindValue(":mail", nuevoUser[3])
        query.bindValue(":movil", nuevoUser[4])
        query.bindValue(":tipo", nuevoUser[5])
        return query.exec()

    @staticmethod
    def listadoUsuarios(tipo="Todos"):
        listado = []
        query = QtSql.QSqlQuery()
        if tipo == "Todos":
            query.prepare("SELECT nombre, dni, email, movil, tipo FROM usuarios ORDER BY nombre")
        else:
            query.prepare("SELECT nombre, dni, email, movil, tipo FROM usuarios WHERE tipo = :tipo ORDER BY nombre")
            query.bindValue(":tipo", tipo)

        if query.exec():
            while query.next():
                row = [query.value(i) for i in range(5)]
                listado.append(row)
        return listado

    @staticmethod
    def listadoUsuariosPDF():
        """Obtiene los usuarios ordenados por nombre para el informe PDF"""
        listado = []
        query = QtSql.QSqlQuery()
        # Seleccionamos los campos que pide el PDF en orden alfabético
        query.prepare("SELECT nombre, email, movil, tipo FROM usuarios ORDER BY nombre ASC")

        if query.exec():
            while query.next():
                row = [query.value(i) for i in range(4)]
                listado.append(row)
        return listado

    @staticmethod
    def modifUsuario(datos):
        query = QtSql.QSqlQuery()
        query.prepare("UPDATE usuarios SET nombre=:nombre, direccion=:dir, email=:mail, movil=:movil, tipo=:tipo WHERE dni=:dni")
        query.bindValue(":nombre", datos[1])
        query.bindValue(":dir", datos[2])
        query.bindValue(":mail", datos[3])
        query.bindValue(":movil", datos[4])
        query.bindValue(":tipo", datos[5])
        query.bindValue(":dni", datos[0])
        return query.exec()

    @staticmethod
    def delUsuario(dni):
        query = QtSql.QSqlQuery()
        query.prepare("DELETE FROM usuarios WHERE dni = :dni")
        query.bindValue(":dni", dni)
        return query.exec()

    @staticmethod
    def cargarUnUsuario(dni):
        query = QtSql.QSqlQuery()
        query.prepare("SELECT dni, nombre, direccion, email, movil, tipo FROM usuarios WHERE dni = :dni")
        query.bindValue(":dni", dni)
        if query.exec() and query.next():
            return [query.value(i) for i in range(6)]
        return None