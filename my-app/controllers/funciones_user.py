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

def procesar_usuario(dataForm):
    try:
        # Validar que los campos no estén vacíos
        campos_requeridos = ['tipo_documento', 'documento', 'nombre', 'apellido', 'telefono', 'email', 'password', 'rol', 'estado']
        for campo in campos_requeridos:
            if campo not in dataForm or not dataForm[campo].strip():
                return f"El campo {campo} es obligatorio."

        # Validar que el tipo de documento sea uno de los permitidos
        tipo_documento = dataForm['tipo_documento']
        valores_permitidos = ['tarjeta_identidad', 'cedula_ciudadania', 'cedula_extranjera', 'nit']
        if tipo_documento not in valores_permitidos:
            return f"El tipo de documento '{tipo_documento}' no es válido."

        # Validar que el documento y el teléfono sean valores numéricos
        try:
            documento = int(dataForm['documento'])
        except ValueError:
            return 'El documento debe ser un número válido.'
        
        try:
            telefono = int(dataForm['telefono'])
        except ValueError:
            return 'El teléfono debe ser un número válido.'

        with connectionBD() as conexion_MySQLdb:
            with conexion_MySQLdb.cursor(dictionary=True) as cursor:
                # SQL para insertar el usuario
                sql = """
                    INSERT INTO crearusuario (
                        tipo_documento, documento, nombre, apellido, telefono, 
                        correo_electronico, contrasena, rol, estado
                    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                """

                # Creando una tupla con los valores del INSERT
                valores = (
                    tipo_documento, 
                    documento,  
                    dataForm['nombre'], 
                    dataForm['apellido'], 
                    telefono,  
                    dataForm['email'],  
                    dataForm['password'],  
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