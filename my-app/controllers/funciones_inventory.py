
from werkzeug.utils import secure_filename
import uuid
from conexion.conexionBD import connectionBD
import re
from flask import send_file

from datetime import datetime


def procesar_inventario(data_form):
    try:
        # Validar que los campos no estén vacíos
        campos_requeridos = ['cantidad_disponible', 'fecha_actualizacion']
        for campo in campos_requeridos:
            if campo not in data_form or not data_form[campo].strip():
                return f"El campo {campo} es obligatorio."

        # Convertir la cantidad disponible a entero
        cantidad_disponible = int(data_form.get('cantidad_disponible'))

        # Obtener la fecha de actualización (puede venir del formulario o usar la fecha actual)
        fecha_actualizacion = data_form.get('fecha_actualizacion')
        if not fecha_actualizacion:
            fecha_actualizacion = datetime.now().date()  # Usar la fecha actual si no se proporciona

        # Obtener la fecha de registro (usamos la fecha y hora actual)
        fecha_registro = datetime.now()

        # Simulación de inserción en la base de datos (sin conexión explícita)
        # Aquí deberías integrar tu lógica de conexión a la base de datos
        # Por ejemplo, usando una función `connectionBD()` como en tu código original
        with connectionBD() as conexion_MySQLdb:
            with conexion_MySQLdb.cursor(dictionary=True) as cursor:
                # SQL para insertar en la tabla de inventario
                sql = """
                    INSERT INTO tbl_inventario (
                        cantidad_disponible, fecha_actualizacion, fecha_registro
                    ) VALUES (%s, %s, %s)
                """
                # Creando una tupla con los valores del INSERT
                valores = (
                    cantidad_disponible,
                    fecha_actualizacion,
                    fecha_registro
                )
                cursor.execute(sql, valores)
                conexion_MySQLdb.commit()  # Confirmar la transacción
                resultado_insert = cursor.rowcount

                if resultado_insert > 0:
                    return resultado_insert  # Éxito
                else:
                    return "No se pudo insertar el registro en el inventario."

    except Exception as e:
        print(f"Error en procesar_inventario: {e}")  # Debug
        return f"Se produjo un error en procesar_inventario: {str(e)}"
    
# me falta meterle el posth