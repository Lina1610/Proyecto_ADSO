from werkzeug.utils import secure_filename
import uuid
from conexion.conexionBD import connectionBD
from flask import session
import re

def validar_claves_foraneas(users_id, departamento_id, municipio_id):
    """
    Valida que las claves foráneas (users_id, departamento_id, municipio_id) existan en la base de datos.
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

        return None  # Retorna None si todo está bien

    except Exception as e:
        return f"Error al validar claves foráneas: {str(e)}"

from flask import session  # Asegúrate de importar session

def procesar_direccion(dataForm):
    """
    Procesa y guarda una dirección en la base de datos.
    Valida los campos obligatorios, claves foráneas y realiza la inserción.
    Retorna el resultado de la inserción o un mensaje de error.
    """
    try:
        print("🔍 Sesión ANTES de procesar la dirección:", session)  # 🛠 Depuración

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
                print("⚠️ Error: La sesión no tiene 'id'")  # 🛠 Depuración
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

                print("✅ Dirección procesada correctamente")  # 🛠 Depuración
                print("🔍 Sesión DESPUÉS de procesar la dirección:", session)  # 🛠 Depuración

                if resultado_insert > 0:
                    return resultado_insert  # Éxito
                else:
                    return "No se pudo insertar la dirección en la base de datos."

    except Exception as e:


        print(f"Error en procesar_form_direccion: {e}")  # Debug
        return f"Se produjo un error en procesar_form_direccion: {str(e)}"
    
# controllers/funciones_address.py

def obtener_direccion(user_id=None):
    """
    Obtiene todas las direcciones de la base de datos.
    Si se proporciona un user_id, filtra las direcciones por ese usuario.
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
                        d.created_at,
                        u.nombre AS usuario_nombre,
                        m.nombre AS municipio_nombre,
                        dep.nombre AS departamento_nombre
                    FROM direccion d
                    LEFT JOIN users u ON d.users_id = u.id
                    LEFT JOIN municipio m ON d.municipio_id = m.id
                    LEFT JOIN departamento dep ON d.departamento_id = dep.id
                """
                if user_id:
                    sql += " WHERE d.users_id = %s"
                    cursor.execute(sql, (user_id,))
                else:
                    cursor.execute(sql)
                direcciones = cursor.fetchall()
                return direcciones
    except Exception as e:
        print(f"Error en obtener_direccion: {e}")
        return []
    
    
    
    
    
    
    
def actualizar_direccion(data_form, id_direccion):
    """
    Actualiza una dirección existente en la base de datos.
    """
    try:
        with connectionBD() as conexion_MySQLdb:
            with conexion_MySQLdb.cursor(dictionary=True) as cursor:
                # Consulta SQL para actualizar una dirección
                sql = """
                    UPDATE direcciones
                    SET nombre_completo = %s, barrio = %s, domicilio = %s, referencias = %s,
                        telefono = %s, estado = %s, costo_domicilio = %s, departamento_id = %s, municipio_id = %s, users_id = %s
                    WHERE id = %s
                """
                valores = (
                    data_form['nombre_completo'],
                    data_form['barrio'],
                    data_form['domicilio'],
                    data_form['referencias'],
                    data_form['telefono'],
                    data_form['estado'],
                    data_form['costo_domicilio'],
                    data_form['departamento_id'],
                    data_form['municipio_id'],
                    data_form['users_id'],
                    id_direccion
                )
                cursor.execute(sql, valores)
                conexion_MySQLdb.commit()
                return True  # Retorna True si la actualización fue exitosa
    except Exception as e:
        print(f"Error en actualizar_direccion: {e}")
        return False


def eliminar_direccion(id_direccion):
    """
    Elimina una dirección de la base de datos.
    """
    try:
        with connectionBD() as conexion_MySQLdb:
            with conexion_MySQLdb.cursor(dictionary=True) as cursor:
                # Consulta SQL para eliminar una dirección
                sql = "DELETE FROM direcciones WHERE id = %s"
                cursor.execute(sql, (id_direccion,))
                conexion_MySQLdb.commit()
                return True  # Retorna True si la eliminación fue exitosa
    except Exception as e:
        print(f"Error en eliminar_direccion: {e}")
        return False

        print(f"❌ Error en procesar_direccion: {e}")  # Debug
        return f"Se produjo un error en procesar_direccion: {str(e)}"



def obtener_direcciones_usuario(user_id):
    """
    Obtiene todas las direcciones activas de un usuario específico.
    Retorna una lista de direcciones con detalles como nombre, barrio, domicilio, etc.
    """
    try:
        with connectionBD() as conexion_MySQLdb:
            with conexion_MySQLdb.cursor(dictionary=True) as cursor:
                cursor.execute("""
                    SELECT d.id, d.nombre_completo, d.barrio, d.domicilio, d.referencias, d.telefono, 
                           dep.nombre AS nombre_departamento, mun.nombre AS nombre_municipio
                    FROM direccion d
                    LEFT JOIN departamento dep ON d.departamento_id = dep.id
                    LEFT JOIN municipio mun ON d.municipio_id = mun.id
                    WHERE d.users_id = %s AND d.estado = 'Activo'  -- Filtro para mostrar solo direcciones activas
                    ORDER BY d.id DESC
                """, (user_id,))
                direcciones = cursor.fetchall()

                # 🚀 Debug: Ver qué devuelve la consulta
                print(f"Direcciones para usuario {user_id}:", direcciones)

                return direcciones
    except Exception as e:
        print(f"Error en obtener_direcciones_usuario: {e}")
        return []

def buscar_direccionBD(search):
    """
    Busca direcciones en la base de datos que coincidan con el término de búsqueda.
    Retorna una lista de direcciones que coinciden con el término de búsqueda.
    """
    try:
        with connectionBD() as conexion_MySQLdb:
            with conexion_MySQLdb.cursor(dictionary=True) as cursor:
                querySQL = """
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
                        u.nombre AS usuario_nombre,
                        m.nombre AS municipio_nombre,
                        dep.nombre AS departamento_nombre
                    FROM direccion d
                    LEFT JOIN users u ON d.users_id = u.id
                    LEFT JOIN municipio m ON d.municipio_id = m.id
                    LEFT JOIN departamento dep ON d.departamento_id = dep.id
                    WHERE d.nombre_completo LIKE %s 
                       OR d.barrio LIKE %s 
                       OR d.domicilio LIKE %s 
                       OR d.telefono LIKE %s 
                       OR u.nombre LIKE %s 
                       OR m.nombre LIKE %s 
                       OR dep.nombre LIKE %s
                """
                search_pattern = f"%{search}%"
                cursor.execute(querySQL, (
                    search_pattern, search_pattern, search_pattern, 
                    search_pattern, search_pattern, search_pattern, search_pattern
                ))
                return cursor.fetchall()
    except Exception as e:
        print(f"Error en buscar_direccionBD: {e}")
        return []

def obtener_direccion_por_id(id):
    """
    Obtiene una dirección específica por su ID, incluyendo los nombres de municipio, departamento y documento del usuario.
    Retorna un diccionario con los detalles de la dirección.
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
                        d.created_at,
                        u.nombre AS usuario_nombre,
                        m.nombre AS municipio_nombre,
                        dep.nombre AS departamento_nombre
                    FROM direccion d
                    LEFT JOIN users u ON d.users_id = u.id
                    LEFT JOIN municipio m ON d.municipio_id = m.id
                    LEFT JOIN departamento dep ON d.departamento_id = dep.id
                    WHERE d.id = %s
                """
                print("Ejecutando consulta SQL:", sql)  # Depuración
                cursor.execute(sql, (id,))
                direccion = cursor.fetchone()
                print("Datos de la dirección obtenidos:", direccion)  # Depuraciónw
                return direccion
    except Exception as e:
        print(f"Error en obtener_direccion_por_id: {e}")  # Depuración
        return None

def obtener_direccion():
    """
    Obtiene todas las direcciones de la base de datos con los nombres de municipio, departamento y documento del usuario.
    Retorna una lista de todas las direcciones.
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
                        d.created_at,
                        u.nombre AS usuario_nombre,
                        m.nombre AS municipio_nombre,
                        dep.nombre AS departamento_nombre
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
    

def actualizar_direccion(id, dataForm):
    """
    Actualiza una dirección existente en la base de datos.
    Retorna un mensaje de éxito o error.
    """
    try:
        # Validar que los campos obligatorios no estén vacíos
        campos_requeridos = [
            'nombre_completo', 'barrio', 'domicilio', 'telefono', 
            'departamento_id', 'municipio_id'
        ]
        for campo in campos_requeridos:
            if campo not in dataForm or not dataForm[campo].strip():
                return f"El campo {campo} es obligatorio."

        # Validar claves foráneas
        error_validacion = validar_claves_foraneas(
            dataForm.get('users_id', session.get('id')), 
            dataForm['departamento_id'], 
            dataForm['municipio_id']
        )
        if error_validacion:
            return error_validacion

        with connectionBD() as conexion_MySQLdb:
            with conexion_MySQLdb.cursor() as cursor:
                sql = """
                    UPDATE direccion SET 
                        nombre_completo = %s,
                        barrio = %s,
                        domicilio = %s,
                        referencias = %s,
                        telefono = %s,
                        estado = %s,
                        costo_domicilio = %s,
                        departamento_id = %s,
                        municipio_id = %s
                    WHERE id = %s
                """
                valores = (
                    dataForm.get('nombre_completo'),
                    dataForm.get('barrio'),
                    dataForm.get('domicilio'),
                    dataForm.get('referencias', ''),  # Campo opcional
                    dataForm.get('telefono'),
                    dataForm.get('estado', 'Activo'),
                    int(dataForm.get('costo_domicilio', 0)),
                    dataForm.get('departamento_id'),
                    dataForm.get('municipio_id'),
                    id
                )
                cursor.execute(sql, valores)
                conexion_MySQLdb.commit()

                if cursor.rowcount > 0:
                    return "Dirección actualizada correctamente."
                else:
                    return "No se encontró la dirección o no se realizaron cambios."

    except Exception as e:
        print(f"Error en actualizar_direccion: {e}")  # Depuración
        return f"Se produjo un error al actualizar la dirección: {str(e)}"

