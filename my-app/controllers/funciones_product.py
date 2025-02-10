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
    # Asegúrate de procesar el precio y convertirlo a un valor numérico decimal
    precio_sin_puntos = re.sub('[^0-9,\.]', '', dataForm['precio'])  # Limpiar cualquier carácter no numérico
    precio_decimal = float(precio_sin_puntos.replace(',', '.'))  # Reemplazar coma por punto para el decimal

    # Convertir unidad de medida a float si es necesario
    try:
        unidad_medida_float = float(dataForm['unidad_medida'])  # Convertir unidad de medida a float
    except ValueError:
        return 'La unidad de medida debe ser un número válido.'

    # Convertir el total a decimal (float) para asegurar su formato adecuado
    try:
        total_decimal = float(dataForm['total'])  # Convertir total a float (decimal)
    except ValueError:
        return 'El total debe ser un número válido.'

    try:
        with connectionBD() as conexion_MySQLdb:
            with conexion_MySQLdb.cursor(dictionary=True) as cursor:
                
                # SQL para insertar el producto
          
                sql = "INSERT INTO producto (nombre, descripcion, precio, estado, unidad_medida, cantidad, marca, tipo, total) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"

                # Creando una tupla con los valores del INSERT
                valores = (
                    dataForm['nombre'], 
                    dataForm['descripcion'], 
                    precio_decimal,  # Usar el precio decimal procesado
                    dataForm['estado'], 
                    unidad_medida_float,  # Usar la unidad de medida como float
                    dataForm['cantidad'], 
                    dataForm['marca'], 
                    dataForm['tipo'],
                    total_decimal) # Usar el total como decimal
                
                cursor.execute(sql, valores)

                conexion_MySQLdb.commit()
                resultado_insert = cursor.rowcount
                return resultado_insert

    except Exception as e:
        return f'Se produjo un error en procesar_producto: {str(e)}'

