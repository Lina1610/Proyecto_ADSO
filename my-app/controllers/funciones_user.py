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
        tipo_documento = dataForm['tipo_documento']  # Asegúrate de que esto se ejecute
        valores_permitidos = ['Cedula ciudadania', 'Tarjeta identidad', 'Cedula extranjeria', 'NIT']
        if tipo_documento not in valores_permitidos:
            return f"El tipo de documento '{tipo_documento}' no es válido."

        # Validar documento y teléfono como números
        try:
            documento = int(dataForm['documento'])
            telefono = int(dataForm['telefono'])
        except ValueError:
            return 'El documento y el teléfono deben ser números válidos.'

        # Resto de las validaciones...
        if documento <= 0:
            return "El documento debe ser mayor a 0."
        doc_str = str(documento)
        if len(doc_str) < 10 or len(doc_str) > 15:
            return "El documento debe tener entre 10 y 15 dígitos."

        if telefono <= 0:
            return "El teléfono debe ser mayor a 0."
        tel_str = str(telefono)
        if len(tel_str) < 7 or len(tel_str) > 13:
            return "El teléfono debe tener entre 7 y 13 dígitos."

        if len(dataForm['nombre']) < 2 or len(dataForm['apellido']) < 2:
            return "El nombre y apellido deben tener al menos 2 caracteres."
        if len(dataForm['nombre']) > 100 or len(dataForm['apellido']) > 100:
            return "El nombre o apellido no puede exceder los 100 caracteres."

        if len(dataForm['correo']) > 50:
            return "El correo no puede exceder los 50 caracteres."
        email_pattern = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
        if not re.match(email_pattern, dataForm['correo']):
            return "El correo no tiene un formato válido."

        contrasena = dataForm['contrasena']
        if len(contrasena) < 8 or len(contrasena) > 20:
            return "La contraseña debe tener entre 8 y 20 caracteres."
        if contrasena.isalpha():
            return "La contraseña no puede contener solo letras."
        if contrasena.isdigit():
            return "La contraseña no puede contener solo números."

        # Encriptar la contraseña
        nueva_password = generate_password_hash(contrasena, method='scrypt')

        # Insertar en la base de datos
        with connectionBD() as conexion_MySQLdb:
            with conexion_MySQLdb.cursor(dictionary=True) as cursor:
                querySQL_doc = "SELECT * FROM users WHERE documento = %s"
                cursor.execute(querySQL_doc, (documento,))
                if cursor.fetchone():
                    return 'El documento ya está registrado en el sistema.'

                querySQL_correo = "SELECT * FROM users WHERE correo = %s"
                cursor.execute(querySQL_correo, (dataForm['correo'],))
                if cursor.fetchone():
                    return 'El correo ya está registrado en el sistema.'

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
                return cursor.rowcount

    except KeyError as e:
        return f"Error: Falta el campo {str(e)} en el formulario."
    except Exception as e:
        print(f"Error en procesar_usuario: {str(e)}")  # Más detalle en el log
        return f"Se produjo un error en procesar_usuario: {str(e)}"

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
                # Primero verificar si el usuario existe
                cursor.execute("SELECT id FROM users WHERE id = %s", (id,))
                existe_antes = cursor.fetchone() is not None
                
                if not existe_antes:
                    return False  # El usuario no existía para empezar
                
                # Intentar eliminar
                querySQL = "DELETE FROM users WHERE id = %s"
                cursor.execute(querySQL, (id,))
                conexion_MySQLdb.commit()
                
                # Verificar si aún existe
                cursor.execute("SELECT id FROM users WHERE id = %s", (id,))
                existe_despues = cursor.fetchone() is not None
                
                # Si ya no existe, la eliminación fue exitosa
                return existe_antes and not existe_despues
    except Exception as e:
        print(f"Error en eliminar_usuario: {e}")
        return False

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
                return Truep
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
