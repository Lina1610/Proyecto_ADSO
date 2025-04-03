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
                # Validar users_id (solo si se proporciona)
                if users_id is not None:
                    if not str(users_id).isdigit():
                        return "El users_id debe ser un número entero."
                    cursor.execute("SELECT id FROM users WHERE id = %s", (users_id,))
                    if not cursor.fetchone():
                        return "El users_id proporcionado no existe."

                # Validar departamento_id
                if not str(departamento_id).isdigit():
                    return "El departamento_id debe ser un número entero."
                cursor.execute("SELECT id FROM departamento WHERE id = %s", (departamento_id,))
                if not cursor.fetchone():
                    return "El departamento_id proporcionado no existe."

                # Validar municipio_id
                if not str(municipio_id).isdigit():
                    return "El municipio_id debe ser un número entero."
                cursor.execute("SELECT id FROM municipio WHERE id = %s AND departamento_id = %s", 
                             (municipio_id, departamento_id))
                if not cursor.fetchone():
                    return "El municipio_id proporcionado no existe o no pertenece al departamento seleccionado."

        return None  # Retorna None si todo está bien

    except Exception as e:
        return f"Error al validar claves foráneas: {str(e)}"

def procesar_direccion(dataForm):
    """
    Procesa y guarda una dirección en la base de datos.
    Valida los campos obligatorios, claves foráneas, tipos de datos, límites de caracteres y unicidad.
    Retorna el resultado de la inserción o un mensaje de error.
    """
    try:
        print("🔍 Sesión ANTES de procesar la dirección:", session)  # 🛠 Depuración
        print("🔍 Datos recibidos en dataForm:", dataForm)  # 🛠 Depuración

        # Validar que los campos no estén vacíos
        campos_requeridos = [
            'nombre_completo', 'barrio', 'domicilio', 
            'departamento_id', 'municipio_id'
        ]
        for campo in campos_requeridos:
            if campo not in dataForm or not dataForm[campo].strip():
                return f"El campo {campo} es obligatorio."

        # Obtener los valores del formulario
        nombre_completo = dataForm.get('nombre_completo').strip()
        barrio = dataForm.get('barrio').strip()
        domicilio = dataForm.get('domicilio').strip()
        referencias = dataForm.get('referencias', '').strip()
        telefono = dataForm.get('telefono', '').strip()
        departamento_id = dataForm.get('departamento_id').strip()
        municipio_id = dataForm.get('municipio_id').strip()

        # Validar que los valores de los <select> no sean "Seleccione"
        if not departamento_id or departamento_id == "":
            return "Debes seleccionar un departamento válido."
        if not municipio_id or municipio_id == "":
            return "Debes seleccionar un municipio válido."

        # Validar longitud de los campos
        if len(nombre_completo) > 160:
            return "El nombre completo no puede exceder los 160 caracteres."
        if len(barrio) > 500:
            return "El barrio no puede exceder los 500 caracteres."
        if len(domicilio) > 500:
            return "El domicilio no puede exceder los 500 caracteres."
        if referencias and len(referencias) > 500:
            return "Las referencias no pueden exceder los 500 caracteres."
        if telefono and len(telefono) > 15:
            return "El teléfono no puede exceder los 15 caracteres."

        # Validar formato del teléfono (si se proporciona)
        if telefono:
            if not telefono.isdigit():
                return "El teléfono debe contener solo números."
            # Validar que el teléfono tenga entre 7 y 15 dígitos (ajusta según tus necesidades)
            if len(telefono) < 7:
                return "El teléfono debe tener al menos 7 dígitos."
        else:
            telefono = None  # Si el campo está vacío, lo dejamos como NULL

        # Validar estado
        estado = dataForm.get('estado', 'Activo').strip()
        print(f"🔍 Estado recibido: {estado}")  # 🛠 Depuración
        if not estado or estado not in ['Activo', 'Inactivo']:
            return "Debes seleccionar un estado válido ('Activo' o 'Inactivo')."

        # Validar users_id desde la sesión o el formulario
        if 'users_id' in dataForm and dataForm['users_id']:
            users_id = dataForm['users_id']
            if not str(users_id).isdigit():
                return "El users_id debe ser un número válido."
        else:
            users_id = session.get('id')
            if users_id is None:
                print("⚠️ Error: La sesión no tiene 'id'")  # 🛠 Depuración
                return "Debes iniciar sesión para registrar una dirección."

        # Validar costo_domicilio (ahora es opcional)
        costo_domicilio = None  # Por defecto, NULL
        if 'costo_domicilio' in dataForm and dataForm['costo_domicilio'].strip():
            try:
                costo_domicilio = int(dataForm['costo_domicilio'])
                if costo_domicilio < 1:  # Confirmado: el mínimo es 1 si se proporciona
                    return "El costo del domicilio debe ser al menos 1."
            except ValueError:
                return "El costo del domicilio debe ser un número válido."

        # Validar claves foráneas
        error_validacion = validar_claves_foraneas(
            users_id,
            departamento_id,
            municipio_id
        )
        if error_validacion:
            return error_validacion

        # Validar unicidad de teléfono y domicilio para el mismo usuario
        with connectionBD() as conexion_MySQLdb:
            with conexion_MySQLdb.cursor(dictionary=True) as cursor:
                if telefono:
                    cursor.execute(
                        "SELECT id FROM direccion WHERE telefono = %s AND users_id = %s",
                        (telefono, users_id)
                    )
                    if cursor.fetchone():
                        return "Ya existe una dirección con este teléfono para este usuario."

                cursor.execute(
                    "SELECT id FROM direccion WHERE domicilio = %s AND users_id = %s",
                    (domicilio, users_id)
                )
                if cursor.fetchone():
                    return "Ya existe una dirección con este domicilio para este usuario."

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
                    nombre_completo,
                    barrio,
                    domicilio,
                    referencias,
                    telefono,  # Ahora puede ser NULL
                    estado,
                    costo_domicilio,  # Ahora puede ser NULL
                    users_id,
                    departamento_id,
                    municipio_id
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
        # Manejar específicamente errores relacionados con el campo telefono
        if "Column 'telefono' cannot be null" in str(e):
            return "Ingresa un número de teléfono."
        return f"Se produjo un error al procesar la dirección: {str(e)}"
    
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

def actualizar_direccion(id, dataForm):
    """
    Actualiza una dirección existente en la base de datos.
    Valida los campos obligatorios, claves foráneas, tipos de datos, límites de caracteres y unicidad.
    Retorna un mensaje de éxito o error.
    """
    try:
        # Validar que los campos obligatorios no estén vacíos
        campos_requeridos = [
            'nombre_completo', 'barrio', 'domicilio', 
            'departamento_id', 'municipio_id'
        ]
        for campo in campos_requeridos:
            if campo not in dataForm or not dataForm[campo].strip():
                return f"El campo {campo} es obligatorio."

        # Obtener los valores del formulario
        nombre_completo = dataForm.get('nombre_completo').strip()
        barrio = dataForm.get('barrio').strip()
        domicilio = dataForm.get('domicilio').strip()
        referencias = dataForm.get('referencias', '').strip()
        telefono = dataForm.get('telefono', '').strip()
        departamento_id = dataForm.get('departamento_id').strip()
        municipio_id = dataForm.get('municipio_id').strip()

        # Validar que los valores de los <select> no sean "Seleccione"
        if departamento_id == "" or not departamento_id:
            return "Debes seleccionar un departamento válido."
        if municipio_id == "" or not municipio_id:
            return "Debes seleccionar un municipio válido."

        # Validar longitud de los campos
        if len(nombre_completo) > 160:
            return "El nombre completo no puede exceder los 160 caracteres."
        if len(barrio) > 500:
            return "El barrio no puede exceder los 500 caracteres."
        if len(domicilio) > 500:
            return "El domicilio no puede exceder los 500 caracteres."
        if referencias and len(referencias) > 500:
            return "Las referencias no pueden exceder los 500 caracteres."
        if telefono and len(telefono) > 15:
            return "El teléfono no puede exceder los 15 caracteres."

        # Validar formato del teléfono (si se proporciona)
        if telefono:
            if not telefono.isdigit():
                return "El teléfono debe contener solo números."
            if len(telefono) < 7:
                return "El teléfono debe tener al menos 7 dígitos."
        else:
            telefono = None

        # Validar estado
        estado = dataForm.get('estado', 'Activo')
        if estado not in ['Activo', 'Inactivo']:
            return "El estado debe ser 'Activo' o 'Inactivo'."

        # Validar costo_domicilio
        try:
            costo_domicilio = int(dataForm.get('costo_domicilio', 0))
            if costo_domicilio < 0:  # Cambiado a permitir 0
                return "El costo del domicilio no puede ser negativo."
        except ValueError:
            return "El costo del domicilio debe ser un número válido."

        # Obtener users_id de la dirección original si no se proporciona
        with connectionBD() as conexion_MySQLdb:
            with conexion_MySQLdb.cursor(dictionary=True) as cursor:
                cursor.execute("SELECT users_id FROM direccion WHERE id = %s", (id,))
                direccion_original = cursor.fetchone()
                if not direccion_original:
                    return "La dirección no existe."
                
                users_id = dataForm.get('users_id', direccion_original['users_id'])

        # Validar claves foráneas (excepto users_id si no se está cambiando)
        error_validacion = validar_claves_foraneas(
            None,  # No validar users_id si no se está cambiando
            departamento_id,
            municipio_id
        )
        if error_validacion:
            return error_validacion

        # Validar unicidad de teléfono y domicilio para el mismo usuario (excluyendo la dirección actual)
        with connectionBD() as conexion_MySQLdb:
            with conexion_MySQLdb.cursor(dictionary=True) as cursor:
                if telefono:
                    cursor.execute(
                        "SELECT id FROM direccion WHERE telefono = %s AND users_id = %s AND id != %s",
                        (telefono, users_id, id)
                    )
                    if cursor.fetchone():
                        return "Ya existe otra dirección con este teléfono para este usuario."

                cursor.execute(
                    "SELECT id FROM direccion WHERE domicilio = %s AND users_id = %s AND id != %s",
                    (domicilio, users_id, id)
                )
                if cursor.fetchone():
                    return "Ya existe otra dirección con este domicilio para este usuario."

        # Actualizar la dirección
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
                    nombre_completo,
                    barrio,
                    domicilio,
                    referencias,
                    telefono,
                    estado,
                    costo_domicilio,
                    departamento_id,
                    municipio_id,
                    id
                )
                cursor.execute(sql, valores)
                conexion_MySQLdb.commit()

                if cursor.rowcount > 0:
                    return "Dirección actualizada correctamente."
                else:
                    return "No se encontró la dirección o no se realizaron cambios."

    except Exception as e:
        print(f"Error en actualizar_direccion: {e}")
        return f"Se produjo un error al actualizar la dirección: {str(e)}"

def eliminar_direccion(id_direccion):
    """Elimina una dirección por su ID."""
    try:
        with connectionBD() as conexion_MySQLdb:
            with conexion_MySQLdb.cursor(dictionary=True) as cursor:
                # Verificar si la dirección existe antes de eliminar
                cursor.execute("SELECT id FROM direccion WHERE id = %s", (id_direccion,))
                existe_antes = cursor.fetchone() is not None

                if not existe_antes:
                    return False  # La dirección no existía para empezar

                # Intentar eliminar
                cursor.execute("DELETE FROM direccion WHERE id = %s", (id_direccion,))
                conexion_MySQLdb.commit()

                # Verificar si la dirección ya no existe
                cursor.execute("SELECT id FROM direccion WHERE id = %s", (id_direccion,))
                existe_despues = cursor.fetchone() is not None

                # Si ya no existe, la eliminación fue exitosa
                return existe_antes and not existe_despues
    except Exception as e:
        print(f"Error en eliminar_direccion: {e}")
        return False

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
                        dep.nombre AS departamento_nombre,
                        d.departamento_id,  -- Asegúrate de incluir estos campos
                        d.municipio_id
                    FROM direccion d
                    LEFT JOIN users u ON d.users_id = u.id
                    LEFT JOIN municipio m ON d.municipio_id = m.id
                    LEFT JOIN departamento dep ON d.departamento_id = dep.id
                    WHERE d.id = %s
                """
                print("Ejecutando consulta SQL:", sql)  # Depuración
                cursor.execute(sql, (id,))
                direccion = cursor.fetchone()
                print("Datos de la dirección obtenidos:", direccion)  # Depuración
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
