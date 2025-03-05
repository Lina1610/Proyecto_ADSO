
from werkzeug.utils import secure_filename
import uuid
from conexion.conexionBD import connectionBD
import re
from flask import send_file
from datetime import datetime

def procesar_stock(dataForm):
    try:
        campos_requeridos = ['cantidad_disponible','producto_id', 'users_id']
        for campo in campos_requeridos:
            if campo not in dataForm or not dataForm[campo].strip():
                return f"El campo {campo.replace('_', ' ').title()} es requerido"

        # Validar que la cantidad disponible sea mayor a cero
        cantidad_disponible = int(dataForm['cantidad_disponible'])
        if cantidad_disponible <= 0:
            return "La cantidad disponible debe ser mayor a cero"

        producto_id = int(dataForm['producto_id'])
        users_id = int(dataForm['users_id'])

        with connectionBD() as conexion_MySQLdb:
            with conexion_MySQLdb.cursor(dictionary=True) as cursor:
                sql = """
                    INSERT INTO stock (
                        cantidad_disponible,
                        producto_id,
                        users_id
                    ) VALUES (%s, %s, %s)
                """
                valores = (
                    cantidad_disponible,
                    producto_id,
                    users_id
                )

                cursor.execute(sql, valores)
                conexion_MySQLdb.commit()
                resultado_insert = cursor.rowcount

                if resultado_insert > 0:
                    return resultado_insert
                else:
                    return "No se pudo insertar el stock en la base de datos"

    except Exception as e:
        print(f"Error en procesar_stock: {e}")
        return f"Se produjo un error en procesar_stock: {str(e)}"
    
def obtener_stock():
    try:
        with connectionBD() as conexion_MySQLdb:
            with conexion_MySQLdb.cursor(dictionary=True) as cursor:
                cursor.execute("""
                    SELECT s.id, s.cantidad_disponible,
                           p.nombre AS producto_nombre, p.id AS producto_id,
                           u.nombre AS usuario_nombre, u.id AS users_id
                    FROM stock s
                    JOIN producto p ON s.producto_id = p.id
                    JOIN users u ON s.users_id = u.id
                """)
                stock = cursor.fetchall()
                print("Datos obtenidos de la base de datos:", stock)  # Depuración
                return stock
    except Exception as e:
        print(f"Error en obtener_stock: {e}")
        return []

def obtener_stock_por_id(id):
    try:
        with connectionBD() as conexion_MySQLdb:
            with conexion_MySQLdb.cursor(dictionary=True) as cursor:
                cursor.execute("""
                    SELECT s.id, s.cantidad_disponible, s.fecha_registro,
                           p.nombre AS producto_nombre, p.id AS producto_id,
                           u.nombre AS usuario_nombre, u.id AS users_id
                    FROM stock s
                    JOIN producto p ON s.producto_id = p.id
                    JOIN users u ON s.users_id = u.id
                    WHERE s.id = %s
                """, (id,))
                stock = cursor.fetchone()
                return stock
    except Exception as e:
        print(f"Error en obtener_stock_por_id: {e}")
        return None

def obtener_productos():
    try:
        with connectionBD() as conexion_MySQLdb:
            with conexion_MySQLdb.cursor(dictionary=True) as cursor:
                cursor.execute("SELECT id, nombre FROM producto")
                productos = cursor.fetchall()
                return productos
    except Exception as e:
        print(f"Error en obtener_productos: {e}")
        return []

def obtener_usuarios():
    try:
        with connectionBD() as conexion_MySQLdb:
            with conexion_MySQLdb.cursor(dictionary=True) as cursor:
                cursor.execute("SELECT id, nombre FROM users")
                usuarios = cursor.fetchall()
                return usuarios
    except Exception as e:
        print(f"Error en obtener_usuarios: {e}")
        return []