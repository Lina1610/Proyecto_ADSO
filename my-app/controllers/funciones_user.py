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
from werkzeug.security import generate_password_hash


def cambiar_estado_usuario(user_id, nuevo_estado):
    try:
        with connectionBD() as conexion_MySQLdb:
            with conexion_MySQLdb.cursor() as cursor:
                sql = "UPDATE users SET estado = %s WHERE id = %s"
                cursor.execute(sql, (nuevo_estado, user_id))
                conexion_MySQLdb.commit()
                return cursor.rowcount
    except Exception as e:
        print(f"Error al cambiar estado: {e}")
        return 0

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
                    SELECT id, tipo_documento, documento, nombre, apellido, 
                           telefono, correo, rol, estado, created_user 
                    FROM users 
                    WHERE nombre LIKE %s OR apellido LIKE %s OR documento LIKE %s OR correo LIKE %s
                """
                search_pattern = f"%{search}%"
                cursor.execute(querySQL, (search_pattern, search_pattern, search_pattern, search_pattern))
                return cursor.fetchall()
    except Exception as e:
        print(f"Error en buscarUsuarioBD: {e}")
        return []

def actualizar_password(user_id, nueva_password):
    try:
        # Hashear la nueva contraseña
        hashed_password = generate_password_hash(nueva_password, method='scrypt')

        # Actualizar la contraseña en la base de datos
        with connectionBD() as conexion_MySQLdb:
            with conexion_MySQLdb.cursor() as cursor:
                query = "UPDATE users SET contrasena = %s WHERE id = %s"
                cursor.execute(query, (hashed_password, user_id))
                conexion_MySQLdb.commit()
                return True
    except Exception as e:
        print(f"Error en actualizar_password: {e}")
        return False

def actualizar_datos_usuario(user_id, nombre, apellido, documento, foto_perfil=None):
    try:
        with connectionBD() as conexion_MySQLdb:
            with conexion_MySQLdb.cursor(dictionary=True) as cursor:
                # Procesar la foto de perfil (si se subió una nueva)
                ruta_imagen_db = None
                if foto_perfil:
                    ruta_imagen_db = procesar_imagen_perfil(foto_perfil)

                # Actualizar los datos del perfil
                querySQL = """
                    UPDATE users
                    SET nombre = %s, apellido = %s, documento = %s
                    {foto_usuario}
                    WHERE id = %s
                """.format(foto_usuario=", foto_usuario = %s" if ruta_imagen_db else "")
                
                valores = [nombre, apellido, documento]
                if ruta_imagen_db:
                    valores.append(ruta_imagen_db)
                valores.append(user_id)

                cursor.execute(querySQL, valores)
                conexion_MySQLdb.commit()
                return True
    except Exception as e:
        print(f"Error en actualizar_datos_usuario: {e}")
        return False

def procesar_imagen_perfil(foto_perfil):
    # Asegurarse de que el archivo es una imagen válida y que tiene un nombre seguro
    if foto_perfil and allowed_file(foto_perfil.filename):
        filename = secure_filename(foto_perfil.filename)

        # Definir la ruta completa donde se almacenará la imagen
        ruta_imagen = os.path.join(app.config['UPLOAD_FOLDER'], filename)

        # Guardar la imagen en la carpeta de uploads
        foto_perfil.save(ruta_imagen)

        # Retornar la ruta relativa que se guardará en la base de datos
        return f"uploads/perfil/{filename}"
    
    return None  # Si no se sube una imagen, retornar None

