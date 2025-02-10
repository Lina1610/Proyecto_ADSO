from werkzeug.utils import secure_filename
import uuid  # Modulo de python para crear un string

from conexion.conexionBD import connectionBD  # Conexión a BD

import datetime
import re
import os

from os import remove  # Modulo  para remover archivo
from os import path  # Modulo para obtener la ruta o directorio


import openpyxl  # Para generar el excel
# biblioteca o modulo send_file para forzar la descarga
from flask import send_file


def procesar_proveedor(dataForm):
    try:
        # Si persona_id está presente en el formulario, lo capturamos
        persona_id = dataForm.get('persona_id')  # Asegúrate de que este campo esté en el formulario

        with connectionBD() as conexion_MySQLdb:
            with conexion_MySQLdb.cursor(dictionary=True) as cursor:
                
                # SQL para insertar el proveedor
                sql = """
                    INSERT INTO proveedor (tipo_persona, razon_social, nombre_comercial, representante_legal, telefono_proveedor)
                    VALUES (%s, %s, %s, %s, %s)
                """
                
                # Tupla con los valores del formulario, incluyendo persona_id
                valores = (
                    dataForm['tipo_persona'], 
                    dataForm['razon_social'], 
                    dataForm['nombre_comercial'], 
                    dataForm['representante_legal'], 
                    dataForm['telefono_proveedor']                   
                )
                
                cursor.execute(sql, valores)
                conexion_MySQLdb.commit()
                resultado_insert = cursor.rowcount
                return resultado_insert  # Retorna el número de filas afectadas

    except Exception as e:
        return f'Se produjo un error en procesar_proveedor: {str(e)}'
