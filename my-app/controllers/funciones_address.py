from werkzeug.utils import secure_filename
import uuid
from conexion.conexionBD import connectionBD
from flask import session
import re

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

                # Validar departamento_id por ID
                cursor.execute("SELECT id FROM departamento WHERE id = %s", (departamento_id,))
                if not cursor.fetchone():
                    return "El departamento_id proporcionado no existe."

                # Validar municipio_id
                cursor.execute("SELECT id FROM municipio WHERE id = %s", (municipio_id,))
                if not cursor.fetchone():
                    return "El municipio_id proporcionado no existe."

        return None  # Retorna None si todo está bien

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
            'departamento_id', 'municipio_id'
        ]
        for campo in campos_requeridos:
            if campo not in dataForm or not dataForm[campo].strip():
                return f"El campo {campo} es obligatorio."

        # Si el formulario es del sitio web, el estado, users_id y costo_domicilio se manejan automáticamente
        if 'estado' not in dataForm:
            estado = 'activo'  # Valor predeterminado para el estado
        else:
            estado = dataForm.get('estado')

        if 'users_id' not in dataForm:
            users_id = session.get('id')  # Obtener el ID del cliente desde la sesión
            if users_id is None:
                return "Debes iniciar sesión para registrar una dirección."
        else:
            users_id = dataForm.get('users_id')

        if 'costo_domicilio' not in dataForm:
            costo_domicilio = 0  # Valor predeterminado para el costo_domicilio
        else:
            try:
                costo_domicilio = int(dataForm['costo_domicilio'])
                if costo_domicilio < 0:
                    return "El costo del domicilio no puede ser negativo."
            except ValueError:
                return "El costo del domicilio debe ser un número válido."

        # Validar que users_id y municipio_id sean números válidos
        if not (str(users_id).isdigit() and dataForm['municipio_id'].isdigit()):
            return "Los valores de users_id y municipio_id deben ser números válidos."

        # Validar claves foráneas
        error_validacion = validar_claves_foraneas(
            users_id,
            dataForm['departamento_id'],  # Aquí se pasa el ID, no el código
            dataForm['municipio_id']
        )
        if error_validacion:  # Si retorna un mensaje de error
            return error_validacion

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
                    estado,  # Usar el valor predeterminado o el proporcionado
                    costo_domicilio,  # Usar el valor predeterminado o el proporcionado
                    users_id,  # Usar el ID de la sesión o el proporcionado
                    dataForm.get('departamento_id'),  # Usar el ID del departamento
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
    

def obtener_direcciones_usuario(user_id):
    try:
        with connectionBD() as conexion_MySQLdb:
            with conexion_MySQLdb.cursor(dictionary=True) as cursor:
                cursor.execute("""
                    SELECT d.id, d.nombre_completo, d.barrio, d.domicilio, d.referencias, d.telefono, 
                           dep.nombre AS nombre_departamento, mun.nombre AS nombre_municipio
                    FROM direccion d
                    LEFT JOIN departamento dep ON d.departamento_id = dep.id
                    LEFT JOIN municipio mun ON d.municipio_id = mun.id
                    WHERE d.users_id = %s
                    ORDER BY d.id DESC
                """, (user_id,))
                direcciones = cursor.fetchall()

                # 🚀 Debug: Ver qué devuelve la consulta
                print(f"Direcciones para usuario {user_id}:", direcciones)

                return direcciones
    except Exception as e:
        print(f"Error en obtener_direcciones_usuario: {e}")
        return []



def obtener_direccion():
    """
    Obtiene todas las direcciones de la base de datos con los nombres de municipio, departamento y documento del usuario.
    """
    try:
        with connectionBD() as conexion_MySQLdb:
            with conexion_MySQLdb.cursor(dictionary=True) as cursor:
                sql = """
                    SELECT 
                        d.id, 
                        d.nombre_completo, 
                        d.barrio, 
                        d.domicilio, 
                        d.referencias, 
                        d.telefono,
                        d.estado,
                        d.costo_domicilio,
                        u.documento AS usuario_documento,  # Obtener el documento del usuario
                        m.nombre AS municipio_nombre,      # Obtener el nombre del municipio
                        dep.nombre AS departamento_nombre  # Obtener el nombre del departamento
                    FROM direccion d
                    LEFT JOIN users u ON d.users_id = u.id
                    LEFT JOIN municipio m ON d.municipio_id = m.id
                    LEFT JOIN departamento dep ON d.departamento_id = dep.id
                    ORDER BY d.id DESC
                """
                print("Ejecutando consulta SQL:", sql)  # Depuración
                cursor.execute(sql)
                direcciones = cursor.fetchall()
                print("Datos de direcciones obtenidos:", direcciones)  # Depuración
                return direcciones
    except Exception as e:
        print(f"Error en obtener_direccion: {e}")  # Depuración
        return []
    
def obtener_direccion_por_id(id):
    try:
        with connectionBD() as conexion_MySQLdb:
            with conexion_MySQLdb.cursor(dictionary=True) as cursor:
                sql = """
                    SELECT 
                        d.id, 
                        d.nombre_completo, 
                        d.barrio, 
                        d.domicilio, 
                        d.referencias, 
                        d.telefono,
                        d.estado,
                        d.costo_domicilio,
                        d.created_at,
                        u.documento AS usuario_documento,
                        m.nombre AS municipio_nombre,
                        dep.nombre AS departamento_nombre
                    FROM direccion d
                    LEFT JOIN users u ON d.users_id = u.id
                    LEFT JOIN municipio m ON d.municipio_id = m.id
                    LEFT JOIN departamento dep ON d.departamento_id = dep.id
                    WHERE d.id = %s
                """
                cursor.execute(sql, (id,))
                direccion = cursor.fetchone()
                return direccion
    except Exception as e:
        print(f"Error en obtener_direccion_por_id: {e}")
        return None