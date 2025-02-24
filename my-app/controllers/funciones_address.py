from werkzeug.utils import secure_filename
import uuid
from conexion.conexionBD import connectionBD
import re

def validar_claves_foraneas(users_id, departamento_codigo, municipio_id):
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

                # Validar departamento_id por código
                cursor.execute("SELECT id FROM departamento WHERE codigo = %s", (departamento_codigo,))
                departamento = cursor.fetchone()
                if not departamento:
                    return "El departamento_id proporcionado no existe."
                
                departamento_id = departamento['id']  # Obtener el ID real del departamento
                
                # Validar municipio_id
                cursor.execute("SELECT id FROM municipio WHERE id = %s", (municipio_id,))
                if not cursor.fetchone():
                    return "El municipio_id proporcionado no existe."

        return departamento_id  # Retorna el ID real del departamento si todo está bien

    except Exception as e:
        return f"Error al validar claves foráneas: {str(e)}"


def procesar_direccion(dataForm):
    """
    Procesa y guarda una dirección en la base de datos.
    """
    try:
        # Validar que los campos no estén vacíos
        campos_requeridos = [
            'nombre_completo', 'barrio', 'domicilio', 'telefono', 
            'estado', 'costo_domicilio', 'users_id', 'departamento_id', 'municipio_id'
        ]
        for campo in campos_requeridos:
            if campo not in dataForm or not dataForm[campo].strip():
                return f"El campo {campo} es obligatorio."

        # Validar que users_id y municipio_id sean números válidos
        if not (dataForm['users_id'].isdigit() and dataForm['municipio_id'].isdigit()):
            return "Los valores de users_id y municipio_id deben ser números válidos."

        # Validar que el costo_domicilio sea un número
        try:
            costo_domicilio = int(dataForm['costo_domicilio'])
            if costo_domicilio < 0:
                return "El costo del domicilio no puede ser negativo."
        except ValueError:
            return "El costo del domicilio debe ser un número válido."

        # Validar claves foráneas y obtener el ID real del departamento
        departamento_id = validar_claves_foraneas(
            dataForm['users_id'],
            dataForm['departamento_id'],  # Aquí se pasa el código, no el ID
            dataForm['municipio_id']
        )
        if isinstance(departamento_id, str):  # Si retorna un mensaje de error
            return departamento_id

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
                    departamento_id,  # Se inserta el ID real del departamento
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
        print(f"Error en procesar_direccion: {e}")  # Debug
        return f"Se produjo un error en procesar_direccion: {str(e)}"
