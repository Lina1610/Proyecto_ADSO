
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
        campos_requeridos = ['tipo', 'fecha_hora', 'estado', 'costo_domicilio', 'direccion_id']
        for campo in campos_requeridos:
            if campo not in data_form or not data_form[campo].strip():
                return f"El campo {campo} es obligatorio."

        # Validar y convertir los datos según los tipos de la base de datos
        tipo = data_form.get('tipo')
        if tipo not in ['Domicilio', 'Establecimiento fisico']:
            return "El campo 'tipo' tiene un valor no válido."

        try:
            fecha_hora = datetime.strptime(data_form.get('fecha_hora'), '%Y-%m-%dT%H:%M')
        except ValueError:
            return "El campo 'fecha_hora' debe estar en el formato 'YYYY-MM-DDTHH:MM'."

        estado = data_form.get('estado')
        if estado not in ['Pendiente', 'En camino', 'Entregado']:
            return "El campo 'estado' tiene un valor no válido."

        try:
            costo_domicilio = float(data_form.get('costo_domicilio'))
        except ValueError:
            return "El campo 'costo_domicilio' debe ser un número válido."

        try:
            direccion_id = int(data_form.get('direccion_id'))
        except ValueError:
            return "El campo 'direccion_id' debe ser un número entero válido."

        # Verificar que el direccion_id exista en la tabla direccion
        with connectionBD() as conexion_MySQLdb:
            with conexion_MySQLdb.cursor(dictionary=True) as cursor:
                cursor.execute("SELECT id FROM direccion WHERE id = %s", (direccion_id,))
                if not cursor.fetchone():
                    return "El ID de la dirección no es válido."

                # Insertar en la tabla entregas
                sql = """
                    INSERT INTO entregas (
                        tipo, fecha_hora, estado, costo_domicilio, direccion_id
                    ) VALUES (%s, %s, %s, %s, %s)
                """
                valores = (
                    tipo,
                    fecha_hora.strftime('%Y-%m-%d %H:%M:%S'),  # Convertir a formato MySQL
                    estado,
                    costo_domicilio,
                    direccion_id
                )
                cursor.execute(sql, valores)
                conexion_MySQLdb.commit()
                id_entrega = cursor.lastrowid  # Obtener el ID de la entrega insertada

                if id_entrega:
                    return id_entrega  # Éxito
                else:
                    return "No se pudo insertar la entrega en la base de datos."

    except mysql.connector.Error as err:
        print(f"Error de MySQL: {err}")  # Debug
        return f"Error de MySQL: {err}"
    except Exception as e:
        print(f"Error en procesar_entrega: {e}")  # Debug
        return f"Se produjo un error en procesar_entrega: {str(e)}"