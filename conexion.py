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
    def listadoTareasPDF():

        listado = []

        query = QtSql.QSqlQuery()

        query.prepare("""

            SELECT
            idTarea,
            idCliente,
            idEmpleado,
            servicio,
            horas,
            precio,
            estado

            FROM tareas

            ORDER BY idTarea

        """)

        if query.exec():

            while query.next():
                fila = [
                    query.value(0),
                    query.value(1),
                    query.value(2),
                    query.value(3),
                    query.value(4),
                    query.value(5),
                    query.value(6)
                ]

                listado.append(fila)

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

    @staticmethod
    def addTarea(nueva):

        query = QtSql.QSqlQuery()

        query.prepare("""
            INSERT INTO tareas
            (idCliente,idEmpleado,servicio,horas,precio,estado)

            VALUES
            (:idC,:idE,:serv,:h,:p,:est)
        """)

        query.bindValue(":idC", nueva[0])
        query.bindValue(":idE", nueva[1])
        query.bindValue(":serv", nueva[2])
        query.bindValue(":h", nueva[3])
        query.bindValue(":p", nueva[4])
        query.bindValue(":est", nueva[5])


        ok = query.exec()

        if not ok:
            print(query.lastError().text())

        return ok

    @staticmethod
    def listadoTareas():
        listado = []
        query = QtSql.QSqlQuery()
        query.prepare("SELECT idTarea, idCliente, idEmpleado, servicio, horas, precio FROM tareas")
        if query.exec():
            while query.next():
                listado.append([query.value(i) for i in range(6)])
        return listado

    @staticmethod
    def cargarUnaTarea(idTarea):
        query = QtSql.QSqlQuery()
        query.prepare("SELECT * FROM tareas WHERE idTarea = :id")
        query.bindValue(":id", idTarea)
        if query.exec() and query.next():
            return [query.value(i) for i in range(6)]
        return None

    @staticmethod
    def delTarea(idTarea):
        query = QtSql.QSqlQuery()
        query.prepare("DELETE FROM tareas WHERE idTarea = :id")
        query.bindValue(":id", idTarea)
        return query.exec()

    @staticmethod
    def modifTarea(datos):
        query = QtSql.QSqlQuery()
        query.prepare("UPDATE tareas SET idCliente=:cli, idEmpleado=:emp, servicio=:serv, "
                      "horas=:h, precio=:p WHERE idTarea=:id")
        query.bindValue(":cli", datos[1])
        query.bindValue(":emp", datos[2])
        query.bindValue(":serv", datos[3])
        query.bindValue(":h", datos[4])
        query.bindValue(":p", datos[5])
        query.bindValue(":id", datos[0])
        return query.exec()

    @staticmethod
    def proximoIdTarea():
        """Mira en la tabla tareas cuál es el ID más alto y le suma 1"""
        query = QtSql.QSqlQuery()
        query.prepare("SELECT MAX(idServicio) FROM tareas")
        if query.exec() and query.next():
            res = query.value(0)
            return (int(res) + 1) if res else 1
        return 1

    @staticmethod
    def obtenerIdPorDni(dni):
        """Busca el idUsuario (numérico) que tiene un DNI concreto"""
        query = QtSql.QSqlQuery()
        query.prepare("SELECT idUsuario FROM usuarios WHERE dni = :dni")
        query.bindValue(":dni", dni)
        if query.exec() and query.next():
            return query.value(0)
        return None

    @staticmethod
    def obtenerIdPorNombre(nombre):

        query = QtSql.QSqlQuery()

        query.prepare("""
            SELECT idUusario
            FROM usuarios
            WHERE nombre = :nombre
        """)

        query.bindValue(":nombre", nombre)

        if query.exec() and query.next():
            return query.value(0)

        return None

