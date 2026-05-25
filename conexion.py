"""
Módulo de Conexión de la Aplicación.

Este módulo gestiona la base de datos SQLite a través de la librería QtSql.
Proporciona los métodos necesarios para la persistencia de datos (CRUD) 
tanto de usuarios como de tareas.
"""

from PyQt6 import QtSql, QtWidgets


class Conexion:
    """
    Clase estática encargada de centralizar todas las consultas SQL de la aplicación.
    """

    @staticmethod
    def db_connect(filename):
        """
        Establece la conexión con el archivo de base de datos SQLite.

        Args:
            filename (str): Ruta del archivo de la base de datos (ej. 'data/recupera.db').
        Returns:
            bool: True si la conexión se abrió con éxito, False en caso contrario.
        """
        db = QtSql.QSqlDatabase.addDatabase('QSQLITE')
        db.setDatabaseName(filename)
        if not db.open():
            QtWidgets.QMessageBox.critical(None, 'Error', 'No se pudo abrir la base de datos')
            return False
        return True

    @staticmethod
    def addUsuario(nuevoUser):
        """
        Inserta un nuevo registro de usuario en la tabla 'usuarios'.

        Args:
            nuevoUser (list): Lista con los datos [nombre, dni, direccion, email, movil, tipo].
        Returns:
            bool: True si el registro fue exitoso, False si falló.
        """
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
        """
        Recupera los usuarios guardados filtrándolos opcionalmente por su rol.

        Args:
            tipo (str): Filtro por rol ('Todos', 'Administrador', etc.). Por defecto 'Todos'.
        Returns:
            list: Lista de listas, donde cada sublista contiene los datos de un usuario.
        """
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
        """
        Obtiene los usuarios ordenados por nombre optimizado para la creación del informe PDF.

        Returns:
            list: Lista con registros de formato [nombre, email, movil, tipo].
        """
        listado = []
        query = QtSql.QSqlQuery()
        query.prepare("SELECT nombre, email, movil, tipo FROM usuarios ORDER BY nombre ASC")

        if query.exec():
            while query.next():
                row = [query.value(i) for i in range(4)]
                listado.append(row)
        return listado

    @staticmethod
    def modifUsuario(datos):
        """
        Actualiza la información de un usuario existente usando el DNI como clave primaria.

        Args:
            datos (list): Lista con formato [dni, nombre, direccion, email, movil, tipo].
        Returns:
            bool: True si se modificó correctamente, False si falló.
        """
        query = QtSql.QSqlQuery()
        query.prepare(
            "UPDATE usuarios SET nombre=:nombre, direccion=:dir, email=:mail, movil=:movil, tipo=:tipo WHERE dni=:dni")
        query.bindValue(":nombre", datos[1])
        query.bindValue(":dir", datos[2])
        query.bindValue(":mail", datos[3])
        query.bindValue(":movil", datos[4])
        query.bindValue(":tipo", datos[5])
        query.bindValue(":dni", datos[0])
        return query.exec()

    @staticmethod
    def delUsuario(dni):
        """
        Elimina un registro de la tabla 'usuarios' a través de su DNI.

        Args:
            dni (str): Documento de identidad del usuario a borrar.
        Returns:
            bool: Resultado de la ejecución de la consulta.
        """
        query = QtSql.QSqlQuery()
        query.prepare("DELETE FROM usuarios WHERE dni = :dni")
        query.bindValue(":dni", dni)
        return query.exec()

    @staticmethod
    def cargarUnUsuario(dni):
        """
        Busca y devuelve la información completa de un único usuario por su DNI.

        Args:
            dni (str): DNI a consultar.
        Returns:
            list/None: Lista con los 6 campos del usuario o None si no se encuentra.
        """
        query = QtSql.QSqlQuery()
        query.prepare("SELECT dni, nombre, direccion, email, movil, tipo FROM usuarios WHERE dni = :dni")
        query.bindValue(":dni", dni)
        if query.exec() and query.next():
            return [query.value(i) for i in range(6)]
        return None

    @staticmethod
    def addTarea(nueva):
        """
        Inserta un nuevo registro de orden de trabajo en la tabla 'tareas'.

        Args:
            nueva (list): Lista con datos [idCliente, idEmpleado, servicio, horas, precio, estado].
        Returns:
            bool: True si se ejecutó con éxito.
        """
        query = QtSql.QSqlQuery()
        query.prepare("""INSERT INTO tareas (idCliente, idEmpleado, servicio, horas, precio, estado) 
                            VALUES (:idC, :idE, :serv, :h, :p, :est)""")
        query.bindValue(":idC", nueva[0])
        query.bindValue(":idE", nueva[1])
        query.bindValue(":serv", nueva[2])
        query.bindValue(":h", nueva[3])
        query.bindValue(":p", nueva[4])
        query.bindValue(":est", nueva[5])
        return query.exec()

    @staticmethod
    def listadoTareas():
        """
        Recupera el listado completo de tareas registradas para mostrarlas en la tabla.

        Returns:
            list: Colección de tareas en listas individuales de 6 columnas.
        """
        listado = []
        query = QtSql.QSqlQuery()
        query.prepare("SELECT idTarea, idCliente, idEmpleado, servicio, horas, precio FROM tareas")
        if query.exec():
            while query.next():
                listado.append([query.value(i) for i in range(6)])
        return listado

    @staticmethod
    def cargarUnaTarea(idTarea):
        """
        Obtiene los datos completos de una tarea específica localizándola por su clave numérica.

        Args:
            idTarea (int/str): Identificador único de la tarea.
        Returns:
            list/None: Registro de la tarea o None si no existe.
        """
        query = QtSql.QSqlQuery()
        query.prepare("SELECT * FROM tareas WHERE idTarea = :id")
        query.bindValue(":id", idTarea)
        if query.exec() and query.next():
            return [query.value(i) for i in range(6)]
        return None

    @staticmethod
    def delTarea(idTarea):
        """
        Elimina de forma permanente una tarea de la base de datos basándose en su ID.

        Args:
            idTarea (int/str): ID de la tarea a eliminar.
        Returns:
            bool: Estado final de la transacción.
        """
        query = QtSql.QSqlQuery()
        query.prepare("DELETE FROM tareas WHERE idTarea = :id")
        query.bindValue(":id", idTarea)
        return query.exec()

    @staticmethod
    def modifTarea(datos):
        """
        Actualiza el contenido de una tarea en base a su ID.

        Args:
            datos (list): Campos modificados ordenados [idTarea, cliente, empleado, servicio, horas, precio].
        Returns:
            bool: True en caso de éxito.
        """
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
        """
        Calcula el próximo identificador autoincremental analizando el ID de servicio máximo.

        Returns:
            int: Siguiente número de ID disponible.
        """
        query = QtSql.QSqlQuery()
        query.prepare("SELECT MAX(idServicio) FROM tareas")
        if query.exec() and query.next():
            res = query.value(0)
            return (int(res) + 1) if res else 1
        return 1

    @staticmethod
    def obtenerIdPorDni(dni):
        """
        Busca la clave primaria interna (numérica) ligada a un DNI de usuario.

        Args:
            dni (str): DNI asignado.
        Returns:
            int/None: Identificador numérico o None.
        """
        query = QtSql.QSqlQuery()
        query.prepare("SELECT idUsuario FROM usuarios WHERE dni = :dni")
        query.bindValue(":dni", dni)
        if query.exec() and query.next():
            return query.value(0)
        return None

    @staticmethod
    def obtenerIdPorNombre(nombre):
        """
        Busca el ID de un usuario/cliente en la base de datos filtrando por su nombre completo.

        Args:
            nombre (str): Nombre completo del usuario a buscar.
        Returns:
            int/None: ID numérico correspondiente o None si no se encuentra.
        """
        query = QtSql.QSqlQuery()
        query.prepare("SELECT idUsuario FROM usuarios WHERE nombre = :nombre")
        query.bindValue(":nombre", nombre)
        if query.exec() and query.next():
            return query.value(0)
        return None