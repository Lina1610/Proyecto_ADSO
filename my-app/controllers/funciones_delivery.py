from datetime import datetime
from mysql.connector import Error as MySQLError
from conexion.conexionBD import connectionBD



def validar_campos_obligatorios(data_form, campos_requeridos):
    """
    Valida que los campos obligatorios no estén vacíos.
    
    Parámetros:
        data_form (dict): Diccionario con los datos del formulario.
        campos_requeridos (list): Lista de campos que son obligatorios.
    
    Retorna:
        str: Mensaje de error si algún campo obligatorio está vacío.
        None: Si todos los campos obligatorios están presentes y no están vacíos.
    """
    for campo in campos_requeridos:
        # Verificar si el campo está presente en el formulario
        if campo not in data_form:
            return f"El campo '{campo}' es obligatorio."
        
        # Obtener el valor del campo
        valor = data_form[campo]
        
        # Verificar si el valor es None o una cadena vacía
        if valor is None or (isinstance(valor, str) and not valor.strip()):
            return f"El campo '{campo}' es obligatorio."
    
    # Si todos los campos están presentes y no están vacíos
    return None

def validar_tipo(tipo):
    """Valida que el tipo de entrega sea válido."""
    tipos_validos = ['Domicilio', 'Establecimiento fisico']
    if tipo not in tipos_validos:
        return f"El campo 'tipo' debe ser uno de: {', '.join(tipos_validos)}."
    return None

def validar_estado(estado):
    """Valida que el estado sea válido."""
    estados_validos = ['Pendiente', 'En camino', 'Entregado']
    if estado not in estados_validos:
        return f"El campo 'estado' debe ser uno de: {', '.join(estados_validos)}."
    return None

def validar_costo_domicilio(costo_domicilio_str):
    """Valida y convierte el costo de domicilio."""
    try:
        return float(costo_domicilio_str), None
    except ValueError:
        return None, "El campo 'costo_domicilio' debe ser un número válido."

def validar_direccion_id(direccion_id_str):
    """Valida y convierte el ID de la dirección."""
    try:
        return int(direccion_id_str), None
    except ValueError:
        return None, "El campo 'direccion_id' debe ser un número entero válido."

def verificar_direccion_existe(direccion_id):
    """Verifica que el ID de la dirección exista en la base de datos."""
    try:
        with connectionBD() as conexion_MySQLdb:
            with conexion_MySQLdb.cursor(dictionary=True) as cursor:
                cursor.execute("SELECT id FROM direccion WHERE id = %s", (direccion_id,))
                if not cursor.fetchone():
                    return "El ID de la dirección no es válido."
        return None
    except MySQLError as err:
        return f"Error de MySQL al verificar la dirección: {err}"

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
                return cursor.lastrowid  # Devuelve el ID de la entrega insertada
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
                    'Pendiente',  # Estado por defecto
                    None,  # Costo de domicilio inicialmente nulo
                    direccion_id if tipo_entrega == 'Domicilio' else None
                )
                cursor.execute(sql, valores)
                conexion_MySQLdb.commit()
                return cursor.lastrowid  # Devuelve el ID de la entrega creada
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
                        d.nombre_completo,  # Nombre completo de la tabla direccion
                        d.domicilio,        # Domicilio de la tabla direccion
                        d.telefono,         # Teléfono de la tabla direccion
                        m.nombre AS municipio,  # Municipio de la tabla municipio
                        dp.nombre AS departamento  # Departamento de la tabla departamento
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
                print("Datos obtenidos de la base de datos:", entregas)  # Depuración
                return entregas
    except MySQLError as err:
        print(f"Error de MySQL al obtener las entregas: {err}")
        return []  # Devuelve una lista vacía en caso de error

def buscar_entrega_por_id(id):
    """Busca una entrega por su ID."""
    try:
        with connectionBD() as conexion_MySQLdb:
            with conexion_MySQLdb.cursor(dictionary=True) as cursor:
                querySQL = """
                    SELECT 
                        e.*, 
                        d.nombre_completo,  # Nombre completo de la tabla direccion
                        d.domicilio,        # Domicilio de la tabla direccion
                        d.telefono,         # Teléfono de la tabla direccion
                        m.nombre AS municipio,  # Municipio de la tabla municipio
                        dp.nombre AS departamento,  # Departamento de la tabla departamento
                        u.nombre AS nombre_usuario  # Nombre del usuario de la tabla users
                    FROM 
                        entrega e
                    LEFT JOIN 
                        direccion d ON e.direccion_id = d.id
                    LEFT JOIN 
                        municipio m ON d.municipio_id = m.id
                    LEFT JOIN 
                        departamento dp ON d.departamento_id = dp.id
                    LEFT JOIN 
                        users u ON d.users_id = u.id  # Relación con la tabla users
                    WHERE 
                        e.id = %s
                """
                cursor.execute(querySQL, (id,))
                return cursor.fetchone()
    except MySQLError as err:
        print(f"Error de MySQL al buscar la entrega: {err}")
        return None  # Devuelve None en caso de error

def actualizar_entrega(id, data_form):
    """Actualiza una entrega existente."""
    # Campos obligatorios base
    campos_requeridos = ['tipo', 'estado']

    # Validar campos obligatorios
    error = validar_campos_obligatorios(data_form, campos_requeridos)
    if error:
        return error

    tipo = data_form['tipo']
    estado = data_form['estado']
    costo_domicilio_str = data_form.get('costo_domicilio', '0')  # Valor por defecto si no está presente
    direccion_id_str = data_form.get('direccion_id')  # Puede ser None si no está presente

    # Validar tipo y estado
    error = validar_tipo(tipo)
    if error:
        return error

    error = validar_estado(estado)
    if error:
        return error

    # Validar costo_domicilio (opcional)
    if costo_domicilio_str and costo_domicilio_str.strip():
        costo_domicilio, error = validar_costo_domicilio(costo_domicilio_str)
        if error:
            return error
    else:
        costo_domicilio = None  # Si no se proporciona, se establece como None

    # Validar direccion_id (opcional)
    if direccion_id_str and direccion_id_str.strip():
        direccion_id, error = validar_direccion_id(direccion_id_str)
        if error:
            return error
        error = verificar_direccion_existe(direccion_id)
        if error:
            return error
    else:
        direccion_id = None  # Si no se proporciona, se establece como None

    # Actualizar la entrega en la base de datos
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
                    costo_domicilio,
                    direccion_id,
                    id
                )
                cursor.execute(sql, valores)
                conexion_MySQLdb.commit()
                return cursor.rowcount  # Devuelve el número de filas afectadas
    except MySQLError as err:
        return f"Error de MySQL al actualizar la entrega: {err}"

def eliminar_entrega(id):
    """Elimina una entrega por su ID."""
    try:
        with connectionBD() as conexion_MySQLdb:
            with conexion_MySQLdb.cursor() as cursor:
                # Verificar si la entrega existe antes de eliminar
                cursor.execute("SELECT id FROM entrega WHERE id = %s", (id,))
                existe_antes = cursor.fetchone() is not None

                if not existe_antes:
                    return False  # La entrega no existía para empezar

                # Intentar eliminar
                cursor.execute("DELETE FROM entrega WHERE id = %s", (id,))
                conexion_MySQLdb.commit()

                # Verificar si la entrega ya no existe
                cursor.execute("SELECT id FROM entrega WHERE id = %s", (id,))
                existe_despues = cursor.fetchone() is not None

                # Si ya no existe, la eliminación fue exitosa
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
                        d.nombre_completo,  # Nombre completo de la tabla direccion
                        d.domicilio,        # Domicilio de la tabla direccion
                        d.telefono,         # Teléfono de la tabla direccion
                        m.nombre AS municipio,  # Municipio de la tabla municipio
                        dp.nombre AS departamento  # Departamento de la tabla departamento
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