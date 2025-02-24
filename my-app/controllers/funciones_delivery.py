
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


def procesar_entrega(data_form):
    try:
        # Validar que los campos no estén vacíos
        campos_requeridos = ['tipo', 'fecha_hora', 'estado', 'costo_domicilio']
        for campo in campos_requeridos:
            if campo not in data_form or not data_form[campo].strip():
                return f"El campo {campo} es obligatorio."

        # Insertar en la tabla entregas
        with connectionBD() as conexion_MySQLdb:
            with conexion_MySQLdb.cursor(dictionary=True) as cursor:
                sql = """
                    INSERT INTO entregas (
                        tipo, fecha_hora, estado, costo_domicilio
                    ) VALUES (%s, %s, %s, %s)
                """
                valores = (
                    data_form.get('tipo'),
                    data_form.get('fecha_hora'),
                    data_form.get('estado'),
                    float(data_form.get('costo_domicilio'))  # Convertir a decimal
                )
                cursor.execute(sql, valores)
                conexion_MySQLdb.commit()
                id_entrega = cursor.lastrowid  # Obtener el ID de la entrega insertada

                if id_entrega:
                    return id_entrega  # Éxito
                else:
                    return "No se pudo insertar la entrega en la base de datos."

    except Exception as e:
        print(f"Error en procesar_entrega: {e}")  # Debug
        return f"Se produjo un error en procesar_entrega: {str(e)}"