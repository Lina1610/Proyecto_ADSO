from werkzeug.utils import secure_filename
import uuid  
from conexion.conexionBD import connectionBD  
import datetime
import re
import os
from os import remove  
from os import path  
import openpyxl  
from flask import send_file

from werkzeug.security import generate_password_hash
from conexion.conexionBD import connectionBD

def procesar_usuario(dataForm):
    try:
        # Validar que los campos no estén vacíos
        campos_requeridos = ['tipo_documento', 'documento', 'nombre', 'apellido', 'telefono', 'correo', 'contrasena', 'rol', 'estado']
        for campo in campos_requeridos:
            if campo not in dataForm or not dataForm[campo].strip():
                return f"El campo {campo} es obligatorio."

        # Validar tipo de documento
        tipo_documento = dataForm['tipo_documento']
        valores_permitidos = ['Cedula ciudadania', 'Tarjeta identidad', 'Cedula extranjeria', 'NIT']
        if tipo_documento not in valores_permitidos:
            return f"El tipo de documento '{tipo_documento}' no es válido."

        # Validar documento y teléfono como números
        try:
            documento = int(dataForm['documento'])
            telefono = int(dataForm['telefono'])
        except ValueError:
            return 'El documento y el teléfono deben ser números válidos.'

        # Encriptar la contraseña
        nueva_password = generate_password_hash(dataForm['contrasena'], method='scrypt')

        with connectionBD() as conexion_MySQLdb:
            with conexion_MySQLdb.cursor(dictionary=True) as cursor:
                # Verificar si el documento o correo ya existen
                querySQL = "SELECT * FROM users WHERE documento = %s OR correo = %s"
                cursor.execute(querySQL, (documento, dataForm['correo']))
                usuario_existente = cursor.fetchone()

                if usuario_existente:
                    return 'El documento o correo ya está registrado.'

                # Insertar en la tabla users
                sql = """
                    INSERT INTO users (
                        tipo_documento, documento, nombre, apellido, telefono, 
                        correo, contrasena, rol, estado, created_user
                    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, NOW())
                """
                valores = (
                    tipo_documento, 
                    documento,  
                    dataForm['nombre'], 
                    dataForm['apellido'], 
                    telefono,  
                    dataForm['correo'],  
                    nueva_password,  
                    dataForm['rol'],  
                    dataForm['estado']  
                )
                
                cursor.execute(sql, valores)
                conexion_MySQLdb.commit()
                resultado_insert = cursor.rowcount
                return resultado_insert

    except Exception as e:
        print(f"Error en procesar_usuario: {e}")  # Debug
        return f'Se produjo un error en crear_usuario: {str(e)}'

def lista_usuariosBD():
    try:
        with connectionBD() as conexion_MySQLdb:
            with conexion_MySQLdb.cursor(dictionary=True) as cursor:
                querySQL = """
                    SELECT id, tipo_documento, documento, nombre, apellido, 
                           telefono, correo, rol, estado, created_user 
                    FROM users
                    ORDER BY id DESC
                """
                cursor.execute(querySQL)
                usuariosBD = cursor.fetchall()
                print("Datos de usuarios obtenidos:", usuariosBD)  # Depuración
                return usuariosBD
    except Exception as e:
        print(f"Error en lista_usuariosBD: {e}")
        return []

def eliminar_usuario(id):
    try:
        with connectionBD() as conexion_MySQLdb:
            with conexion_MySQLdb.cursor(dictionary=True) as cursor:
                querySQL = "DELETE FROM users WHERE id = %s"
                cursor.execute(querySQL, (id,))
                conexion_MySQLdb.commit()
                resultado_eliminar = cursor.rowcount
                return resultado_eliminar
    except Exception as e:
        print(f"Error en eliminar_usuario: {e}")
        return None

def obtener_usuario_por_id(id):
    try:
        with connectionBD() as conexion_MySQLdb:
            with conexion_MySQLdb.cursor(dictionary=True) as cursor:
                querySQL = "SELECT * FROM users WHERE id = %s"
                cursor.execute(querySQL, (id,))
                usuario = cursor.fetchone()
                return usuario
    except Exception as e:
        print(f"Error en obtener_usuario_por_id: {e}")
        return None

def buscarUsuarioBD(search):
    try:
        with connectionBD() as conexion_MySQLdb:
            with conexion_MySQLdb.cursor(dictionary=True) as cursor:
                querySQL = """
                    SELECT id, nombre, apellido, documento, correo 
                    FROM users 
                    WHERE nombre LIKE %s OR apellido LIKE %s OR documento LIKE %s OR correo LIKE %s
                """
                search_pattern = f"%{search}%"
                cursor.execute(querySQL, (search_pattern, search_pattern, search_pattern, search_pattern))
                resultado_busqueda = cursor.fetchall()
                return resultado_busqueda
    except Exception as e:
        print(f"Error en buscarUsuarioBD: {e}")
        return []