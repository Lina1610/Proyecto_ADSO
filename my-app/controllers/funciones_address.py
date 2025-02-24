from werkzeug.utils import secure_filename
import uuid
from conexion.conexionBD import connectionBD
import re
from flask import send_file

def procesar_direccion(dataForm):
    try:
        # Validar que los campos no estén vacíos
        campos_requeridos = [
            'nombre_completo', 'barrio', 'domicilio', 'telefono', 
            'estado', 'costo_domicilio', 'users_id', 'departamento_id', 'municipio_id'
        ]
        for campo in campos_requeridos:
            if campo not in dataForm or not dataForm[campo].strip():
                return f"El campo {campo} es obligatorio."

        # Validar que el costo_domicilio sea un número
        try:
            costo_domicilio = int(dataForm['costo_domicilio'])
        except ValueError:
            return "El costo del domicilio debe ser un número válido."

        # Validar claves foráneas
        error = validar_claves_foraneas(
            dataForm['users_id'],
            dataForm['departamento_id'],
            dataForm['municipio_id']
        )
        if error:
            return error

        # Insertar en la tabla direccion
        with connectionBD() as conexion_MySQLdb:
            with conexion_MySQLdb.cursor(dictionary=True) as cursor:
                sql = """
                    INSERT INTO direccion (
                        nombre_completo, barrio, domicilio, referencias, 
                        telefono, estado, costo_domicilio, users_id,
                        departamento_id, municipio_id
                    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """
                valores = (
                    dataForm.get('nombre_completo'),
                    dataForm.get('barrio'),
                    dataForm.get('domicilio'),
                    dataForm.get('referencias', ''),  # Campo opcional
                    dataForm.get('telefono'),
                    dataForm.get('estado'),
                    costo_domicilio,
                    dataForm.get('users_id'),
                    dataForm.get('departamento_id'),
                    dataForm.get('municipio_id')
                )
                cursor.execute(sql, valores)
                conexion_MySQLdb.commit()
                resultado_insert = cursor.rowcount

                if resultado_insert > 0:
                    return resultado_insert  # Éxito
                else:
                    return "No se pudo insertar la dirección en la base de datos."

    except Exception as e:
        print(f"Error en procesar_form_direccion: {e}")  # Debug
        return f"Se produjo un error en procesar_form_direccion: {str(e)}"