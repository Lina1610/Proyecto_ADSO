
# Para subir archivo tipo foto al servidor
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

def procesar_producto(dataForm):
    # Asegúrate de procesar el precio y convertirlo a un valor numérico
    precio_sin_puntos = re.sub('[^0-9]+', '', dataForm['precio_producto'])
    # Convertir precio a FLOAT
    precio_float = float(precio_sin_puntos)

    try:
        with connectionBD() as conexion_MySQLdb:
            with conexion_MySQLdb.cursor(dictionary=True) as cursor:

                # Aquí debes usar la tabla de productos
                sql = """
                INSERT INTO productos (nombre_producto, descripcion_producto, categoria_producto, 
                                           cantidad_producto, precio_producto, unidad_medida_producto, 
                                           marca_producto, codigo_producto, proveedor_producto, fecha_ingreso_producto)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                """

                # Creando una tupla con los valores del INSERT para los productos
                valores = (
                    dataForm['nombre_producto'], 
                    dataForm['descripcion_producto'], 
                    dataForm['categoria_producto'], 
                    dataForm['cantidad_producto'], 
                    precio_float, 
                    dataForm['unidad_medida_producto'], 
                    dataForm['marca_producto'], 
                    dataForm['codigo_producto'], 
                    dataForm['proveedor_producto'], 
                    dataForm['fecha_ingreso_producto']
                )
                
                cursor.execute(sql, valores)

                conexion_MySQLdb.commit()
                resultado_insert = cursor.rowcount
                return resultado_insert

    except Exception as e:
        return f'Se produjo un error en procesar_form_producto: {str(e)}'
