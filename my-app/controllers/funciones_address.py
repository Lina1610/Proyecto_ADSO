
from werkzeug.utils import secure_filename
import uuid
from conexion.conexionBD import connectionBD
import re
from flask import send_file

def validar_claves_foraneas(users_id, departamento_id, municipio_id):
    """
    Valida que las claves foráneas existan en la base de datos.
    Retorna un mensaje de error si alguna no existe, o None si todo está bien.
    """
    try:
        with connectionBD() as conexion_MySQLdb:
            with conexion_MySQLdb.cursor(dictionary=True) as cursor:
                # Validar users_id
                cursor.execute("SELECT id FROM users WHERE id = %s", (users_id,))
                if not cursor.fetchone():
                    return "El users_id proporcionado no existe."

                # Validar departamento_id
                cursor.execute("SELECT id FROM departamento WHERE id = %s", (departamento_id,))
                if not cursor.fetchone():
                    return "El departamento_id proporcionado no existe."

                # Validar municipio_id
                cursor.execute("SELECT id FROM municipio WHERE id = %s", (municipio_id,))
                if not cursor.fetchone():
                    return "El municipio_id proporcionado no existe."

        return None  # Si todo está bien, retorna None

    except Exception as e:
        return f"Error al validar claves foráneas: {str(e)}"
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

        # Validar que users_id, departamento_id y municipio_id sean números válidos
        if not (dataForm['users_id'].isdigit() and dataForm['departamento_id'].isdigit() and dataForm['municipio_id'].isdigit()):
            return "Los valores de users_id, departamento_id y municipio_id deben ser números válidos."

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