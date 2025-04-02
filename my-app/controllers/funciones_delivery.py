from datetime import datetime
from mysql.connector import Error as MySQLError
from conexion.conexionBD import connectionBD

def validar_campos_obligatorios(data_form, campos_requeridos):
    """Valida que los campos obligatorios no estén vacíos."""
    for campo in campos_requeridos:
        if campo not in data_form:
            return f"El campo '{campo}' es obligatorio y no puede estar vacío."
        valor = data_form[campo]
        if valor is None or (isinstance(valor, str) and not valor.strip()):
            return f"El campo '{campo}' es obligatorio y no puede estar vacío."
    return None

def validar_tipo(tipo):
    """Valida que el tipo de entrega sea válido."""
    tipos_validos = ['Domicilio', 'Presencial']
    if tipo not in tipos_validos:
        return f"El tipo de entrega debe ser 'Domicilio' o 'Presencial'."
    return None

def validar_estado(estado):
    """Valida que el estado sea válido."""
    estados_validos = ['Pendiente', 'En Proceso', 'En camino', 'Entregado']
    if estado not in estados_validos:
        return f"El estado debe ser 'Pendiente', 'En Proceso', 'En camino' o 'Entregado'."
    return None

def validar_costo_domicilio(costo_domicilio_str):
    """Valida y convierte el costo de domicilio."""
    if not costo_domicilio_str or not costo_domicilio_str.strip():
        return None, None  # Opcional, puede ser None

    # Permitir hasta 13 caracteres (10 dígitos enteros + 1 punto + 2 decimales)
    if len(str(costo_domicilio_str)) > 13:
        return None, "El costo de domicilio no puede exceder 13 caracteres (10 dígitos enteros, 1 punto, 2 decimales)."

    try:
        costo = float(costo_domicilio_str)
        if costo < 0:
            return None, "El costo de domicilio no puede ser un número negativo."
        if costo > 9999999999.99:  # Máximo valor para DECIMAL(12,2)
            return None, "El costo de domicilio no puede exceder 9999999999.99."
        
        # Validar el formato DECIMAL(12,2)
        parts = str(costo_domicilio_str).split('.')
        parte_entera = parts[0]
        parte_decimal = parts[1] if len(parts) > 1 else ''

        if len(parte_entera) > 10:
            return None, "La parte entera del costo de domicilio no puede exceder 10 dígitos."
        if parte_decimal and len(parte_decimal) > 2:
            return None, "La parte decimal del costo de domicilio no puede exceder 2 dígitos."

        return costo, None
    except ValueError:
        return None, "El costo de domicilio debe ser un número válido."

def validar_direccion_id(direccion_id_str, tipo):
    """Valida y convierte el ID de la dirección, pero ahora es opcional."""
    # Si no se proporciona direccion_id, lo tratamos como opcional
    if not direccion_id_str or not direccion_id_str.strip():
        return None, None  # No hay error, simplemente no se proporciona dirección

    try:
        direccion_id = int(direccion_id_str)
        if direccion_id <= 0:
            return None, "El ID de la dirección debe ser un número entero positivo."
        return direccion_id, None
    except ValueError:
        return None, "El ID de la dirección debe ser un número entero válido."

def verificar_direccion_existe(direccion_id):
    """Verifica que el ID de la dirección exista en la base de datos."""
    try:
        with connectionBD() as conexion_MySQLdb:
            with conexion_MySQLdb.cursor(dictionary=True) as cursor:
                cursor.execute("SELECT id FROM direccion WHERE id = %s", (direccion_id,))
                if not cursor.fetchone():
                    return "La dirección seleccionada no existe."
        return None
    except MySQLError as err:
        return f"Error al verificar la dirección: {err}"

def insertar_entrega(tipo, estado, costo_domicilio, direccion_id):
    """Inserta una nueva entrega en la base de datos."""
    try:
        with connectionBD() as conexion_MySQLdb:
            with conexion_MySQLdb.cursor(dictionary=True) as cursor:
                sql = """
                    INSERT INTO entrega (
                        tipo, estado, costo_domicilio, direccion_id
                    ) VALUES (%s, %s, %s, %s)
                """
                valores = (
                    tipo,
                    estado,
                    costo_domicilio,
                    direccion_id
                )
                cursor.execute(sql, valores)
                conexion_MySQLdb.commit()
                return cursor.lastrowid
    except MySQLError as err:
        return f"Error de MySQL al insertar la entrega: {err}"

def procesar_entrega(tipo_entrega, direccion_id=None):
    """Crea un registro en la tabla 'entrega' y devuelve el ID."""
    try:
        with connectionBD() as conexion_MySQLdb:
            with conexion_MySQLdb.cursor(dictionary=True) as cursor:
                sql = """
                    INSERT INTO entrega (
                        tipo, estado, costo_domicilio, direccion_id, fecha_hora
                    ) VALUES (%s, %s, %s, %s, NOW())
                """
                valores = (
                    tipo_entrega,
                    'Pendiente',
                    None,
                    direccion_id if tipo_entrega == 'Domicilio' else None
                )
                cursor.execute(sql, valores)
                conexion_MySQLdb.commit()
                return cursor.lastrowid
    except Exception as e:
        return f"Error al crear la entrega: {str(e)}"

def obtener_entregas():
    """Obtiene todas las entregas de la base de datos."""
    try:
        with connectionBD() as conexion_MySQLdb:
            with conexion_MySQLdb.cursor(dictionary=True) as cursor:
                querySQL = """
                    SELECT 
                        e.id, 
                        e.tipo, 
                        e.estado, 
                        e.costo_domicilio, 
                        e.direccion_id,
                        d.nombre_completo,
                        d.domicilio,
                        d.telefono,
                        m.nombre AS municipio,
                        dp.nombre AS departamento
                    FROM 
                        entrega e
                    LEFT JOIN 
                        direccion d ON e.direccion_id = d.id
                    LEFT JOIN 
                        municipio m ON d.municipio_id = m.id
                    LEFT JOIN 
                        departamento dp ON d.departamento_id = dp.id
                """
                cursor.execute(querySQL)
                entregas = cursor.fetchall()
                print("Datos obtenidos de la base de datos:", entregas)
                return entregas
    except MySQLError as err:
        print(f"Error de MySQL al obtener las entregas: {err}")
        return []

def buscar_entrega_por_id(id):
    """Busca una entrega por su ID."""
    try:
        with connectionBD() as conexion_MySQLdb:
            with conexion_MySQLdb.cursor(dictionary=True) as cursor:
                querySQL = """
                    SELECT 
                        e.*, 
                        d.nombre_completo,
                        d.domicilio,
                        d.telefono,
                        m.nombre AS municipio,
                        dp.nombre AS departamento,
                        u.nombre AS nombre_usuario
                    FROM 
                        entrega e
                    LEFT JOIN 
                        direccion d ON e.direccion_id = d.id
                    LEFT JOIN 
                        municipio m ON d.municipio_id = m.id
                    LEFT JOIN 
                        departamento dp ON d.departamento_id = dp.id
                    LEFT JOIN 
                        users u ON d.users_id = u.id
                    WHERE 
                        e.id = %s
                """
                cursor.execute(querySQL, (id,))
                return cursor.fetchone()
    except MySQLError as err:
        print(f"Error de MySQL al buscar la entrega: {err}")
        return None

def actualizar_entrega(id, data_form):
    """Actualiza una entrega existente."""
    campos_requeridos = ['tipo', 'estado']
    error = validar_campos_obligatorios(data_form, campos_requeridos)
    if error:
        return error

    tipo = data_form['tipo']
    estado = data_form['estado']
    costo_domicilio_str = data_form.get('costo_domicilio', None)
    direccion_id_str = data_form.get('direccion_id')

    error = validar_tipo(tipo)
    if error:
        return error

    error = validar_estado(estado)
    if error:
        return error

    costo_domicilio, error = validar_costo_domicilio(costo_domicilio_str)
    if error:
        return error

    direccion_id, error = validar_direccion_id(direccion_id_str, tipo)
    if error:
        return error

    if direccion_id:  # Solo verificamos si se proporcionó un direccion_id
        error = verificar_direccion_existe(direccion_id)
        if error:
            return error

    try:
        with connectionBD() as conexion_MySQLdb:
            with conexion_MySQLdb.cursor(dictionary=True) as cursor:
                sql = """
                    UPDATE entrega
                    SET tipo = %s, estado = %s, costo_domicilio = %s, direccion_id = %s
                    WHERE id = %s
                """
                valores = (
                    tipo,
                    estado,
                    costo_domicilio if costo_domicilio is not None else None,
                    direccion_id,
                    id
                )
                cursor.execute(sql, valores)
                conexion_MySQLdb.commit()
                return cursor.rowcount
    except MySQLError as err:
        return f"Error de MySQL al actualizar la entrega: {err}"

def eliminar_entrega(id):
    """Elimina una entrega por su ID."""
    try:
        with connectionBD() as conexion_MySQLdb:
            with conexion_MySQLdb.cursor() as cursor:
                cursor.execute("SELECT id FROM entrega WHERE id = %s", (id,))
                existe_antes = cursor.fetchone() is not None

                if not existe_antes:
                    return False

                cursor.execute("DELETE FROM entrega WHERE id = %s", (id,))
                conexion_MySQLdb.commit()

                cursor.execute("SELECT id FROM entrega WHERE id = %s", (id,))
                existe_despues = cursor.fetchone() is not None

                return existe_antes and not existe_despues
    except Exception as e:
        print(f"Error en eliminar_entrega: {e}")
        return False

def buscar_entregaBD(search_query):
    """Busca entregas en la base de datos según un término de búsqueda."""
    try:
        with connectionBD() as conexion_MySQLdb:
            with conexion_MySQLdb.cursor(dictionary=True) as cursor:
                querySQL = """
                    SELECT 
                        e.id, 
                        e.tipo, 
                        e.estado, 
                        e.costo_domicilio, 
                        e.direccion_id,
                        d.nombre_completo,
                        d.domicilio,
                        d.telefono,
                        m.nombre AS municipio,
                        dp.nombre AS departamento
                    FROM 
                        entrega e
                    LEFT JOIN 
                        direccion d ON e.direccion_id = d.id
                    LEFT JOIN 
                        municipio m ON d.municipio_id = m.id
                    LEFT JOIN 
                        departamento dp ON d.departamento_id = dp.id
                    WHERE 
                        e.tipo LIKE %s OR 
                        e.estado LIKE %s OR 
                        d.nombre_completo LIKE %s OR 
                        d.domicilio LIKE %s OR 
                        d.telefono LIKE %s OR 
                        m.nombre LIKE %s OR 
                        dp.nombre LIKE %s
                    ORDER BY e.id DESC
                """
                search_pattern = f"%{search_query}%"
                cursor.execute(querySQL, (search_pattern, search_pattern, search_pattern, search_pattern, search_pattern, search_pattern, search_pattern))
                return cursor.fetchall()
    except MySQLError as err:
        print(f"Error en buscar_entregaBD: {err}")
        return []