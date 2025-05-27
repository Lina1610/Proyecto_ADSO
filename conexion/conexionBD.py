from contextlib import contextmanager
import mysql.connector

@contextmanager
def connectionBD():
    conexion = None
    try:
        conexion = mysql.connector.connect(
            host="localhost",
            user="root",
            passwd="",
            database="crud_python",
            charset='utf8mb4',
            collation='utf8mb4_unicode_ci',
            raise_on_warnings=True
        )
        yield conexion
    except mysql.connector.Error as error:
        print(f"No se pudo conectar: {error}")
        yield None
    finally:
        if conexion and conexion.is_connected():
            conexion.close()
