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
    tipos_validos = ['Domicilio', 'Establecimiento fisico', 'Presencial']
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

def validar_direccion_id(direccion_id_str, tipo_entrega):
    """
    Valida el ID de dirección solo para entregas a domicilio
    
    Args:
        direccion_id_str (str): ID en formato texto
        tipo_entrega (str): Tipo de entrega ('Domicilio' o 'Presencial')
    
    Returns:
        tuple: (id_validado, error_message)
    """
    # Si no es entrega a domicilio, no necesita validación de dirección
    if tipo_entrega != 'Domicilio':
        return None, None
    
    # Validación para entregas a domicilio
    try:
        if not direccion_id_str or not direccion_id_str.strip():
            return None, "Para entregas a domicilio, se requiere una dirección válida"
        
        direccion_id = int(direccion_id_str)
        
        if direccion_id <= 0:
            return None, "El ID de dirección debe ser un número positivo"
        
        # Verificar que la dirección existe y está activa
        with connectionBD() as conexion_MySQLdb:
            with conexion_MySQLdb.cursor(dictionary=True) as cursor:
                cursor.execute("""
                    SELECT id FROM direccion 
                    WHERE id = %s AND estado = 'Activo'
                """, (direccion_id,))
                if not cursor.fetchone():
                    return None, "La dirección no existe o no está activa"
        
        return direccion_id, None
        
    except ValueError:
        return None, "El ID de dirección debe ser un número entero válido"

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

def procesar_entrega(tipo_entrega, direccion_id=None, users_id=None):
    """Crea registro en entrega con users_id obligatorio"""
    try:
        if not users_id:
            raise ValueError("El users_id es obligatorio")
        
        with connectionBD() as conexion_MySQLdb:
            with conexion_MySQLdb.cursor(dictionary=True) as cursor:
                # Para domicilio, verificar que la dirección pertenece al usuario
                if tipo_entrega == 'Domicilio' and direccion_id:
                    cursor.execute("SELECT users_id FROM direccion WHERE id = %s", (direccion_id,))
                    dir_data = cursor.fetchone()
                    if dir_data and dir_data['users_id'] != int(users_id):
                        raise ValueError("La dirección no pertenece al usuario")
                
                # Insertar la entrega siempre con users_id, tanto para domicilio como presencial
                sql = """INSERT INTO entrega (
                    tipo, estado, costo_domicilio, direccion_id, users_id, fecha_hora
                ) VALUES (%s, %s, %s, %s, %s, NOW())"""
                
                valores = (
                    tipo_entrega,
                    'Pendiente',
                    float(0) if tipo_entrega == 'Domicilio' else None,
                    int(direccion_id) if tipo_entrega == 'Domicilio' else None,
                    int(users_id)  # Siempre se asigna el users_id
                )
                
                cursor.execute(sql, valores)
                entrega_id = cursor.lastrowid
                conexion_MySQLdb.commit()
                return entrega_id
                
    except Exception as e:
        print(f"Error en procesar_entrega: {str(e)}")
        if 'conexion_MySQLdb' in locals():
            conexion_MySQLdb.rollback()
        raisey

def crear_pedido(users_id, metodo_pago_id, entrega_id, total):
    """Crea un pedido y actualiza automáticamente la entrega"""
    try:
        with connectionBD() as conexion_MySQLdb:
            with conexion_MySQLdb.cursor(dictionary=True) as cursor:
                # 1. Crear el pedido
                sql_pedido = """
                    INSERT INTO pedido (
                        fecha, estado, total, entrega_id, users_id, metodo_pago_id
                    ) VALUES (NOW(), %s, %s, %s, %s, %s)
                """
                valores_pedido = (
                    'Pendiente',
                    float(total),
                    int(entrega_id),
                    int(users_id),
                    int(metodo_pago_id)
                )
                cursor.execute(sql_pedido, valores_pedido)
                pedido_id = cursor.lastrowid
                
                # 2. Actualizar automáticamente la entrega con el users_id
                sql_actualizar = """
                    UPDATE entrega 
                    SET users_id = %s 
                    WHERE id = %s AND (users_id IS NULL OR users_id = 0 OR users_id != %s)
                """
                # CORRECCIÓN: Paréntesis correctamente cerrados
                cursor.execute(sql_actualizar, (int(users_id), int(entrega_id), int(users_id)))
                
                conexion_MySQLdb.commit()
                return pedido_id
                
    except Exception as e:
        print(f"ERROR en crear_pedido: {str(e)}")
        if 'conexion_MySQLdb' in locals():
            conexion_MySQLdb.rollback()
        return f"Error al crear el pedido: {str(e)}"
    
def obtener_entregas():
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
                        e.users_id,
                        e.fecha_hora,
                        COALESCE(
                            u.nombre,  # Usuario directo de la entrega
                            (SELECT u2.nombre FROM users u2 WHERE u2.id = d.users_id),  # Usuario de la dirección
                            'Usuario no disponible'
                        ) AS nombre_usuario,
                        d.nombre_completo,
                        CASE
                            WHEN e.tipo = 'Domicilio' THEN 
                                CONCAT(d.domicilio, ', ', COALESCE(d.barrio, ''), ' - ', COALESCE(d.referencias, ''))
                            ELSE 'Establecimiento físico'
                        END AS direccion_completa,
                        d.telefono,
                        m.nombre AS municipio,
                        dp.nombre AS departamento
                    FROM 
                        entrega e
                    LEFT JOIN 
                        direccion d ON e.direccion_id = d.id
                    LEFT JOIN 
                        users u ON e.users_id = u.id
                    LEFT JOIN 
                        municipio m ON d.municipio_id = m.id
                    LEFT JOIN 
                        departamento dp ON d.departamento_id = dp.id
                    ORDER BY e.id DESC
                """
                cursor.execute(querySQL)
                return cursor.fetchall()
    except MySQLError as err:
        print(f"Error de MySQL al obtener las entregas: {err}")
        return []

def buscar_entrega_por_id(id):
    """Busca una entrega por su ID incluyendo todos los datos relacionados."""
    try:
        with connectionBD() as conexion_MySQLdb:
            with conexion_MySQLdb.cursor(dictionary=True) as cursor:
                querySQL = """
                    SELECT 
                        e.*, 
                        d.nombre_completo, 
                        d.domicilio,
                        d.telefono,
                        d.barrio,
                        d.referencias,
                        d.users_id AS direccion_users_id,
                        m.nombre AS municipio,
                        dp.nombre AS departamento,
                        u1.nombre AS nombre_usuario_direccion,
                        u2.nombre AS nombre_usuario_entrega
                    FROM 
                        entrega e
                    LEFT JOIN 
                        direccion d ON e.direccion_id = d.id
                    LEFT JOIN 
                        municipio m ON d.municipio_id = m.id
                    LEFT JOIN 
                        departamento dp ON d.departamento_id = dp.id
                    LEFT JOIN 
                        users u1 ON d.users_id = u1.id
                    LEFT JOIN 
                        users u2 ON e.users_id = u2.id
                    WHERE 
                        e.id = %s
                """
                cursor.execute(querySQL, (id,))
                entrega = cursor.fetchone()
                
                # Si se encuentra la entrega, agregar un campo combinado para el nombre del usuario
                if entrega:
                    entrega['nombre_usuario'] = entrega['nombre_usuario_entrega'] or entrega['nombre_usuario_direccion'] or 'Usuario no disponible'
                
                return entrega
    except MySQLError as err:
        print(f"Error de MySQL al buscar la entrega: {err}")
        return None

def actualizar_entrega(id, data_form):
    """Actualiza una entrega existente sin perder datos."""
    try:
        # Obtener la entrega actual primero
        entrega_actual = buscar_entrega_por_id(id)
        if not entrega_actual:
            return "La entrega no existe"

        # Campos obligatorios
        campos_requeridos = ['tipo', 'estado']
        error = validar_campos_obligatorios(data_form, campos_requeridos)
        if error:
            return error

        # Validar tipo y estado
        error = validar_tipo(data_form['tipo'])
        if error:
            return error

        error = validar_estado(data_form['estado'])
        if error:
            return error

        # Mantener los valores existentes si no se proporcionan nuevos
        costo_domicilio = data_form.get('costo_domicilio', entrega_actual.get('costo_domicilio'))
        direccion_id = data_form.get('direccion_id', entrega_actual.get('direccion_id'))

        # Validar costo_domicilio
        if costo_domicilio and str(costo_domicilio).strip():
            try:
                costo_domicilio = float(costo_domicilio)
            except ValueError:
                return "El campo 'costo_domicilio' debe ser un número válido"
        else:
            costo_domicilio = entrega_actual.get('costo_domicilio')

        # Validar direccion_id
        if direccion_id and str(direccion_id).strip():
            try:
                direccion_id = int(direccion_id)
                # Verificar que la dirección existe
                with connectionBD() as conexion_MySQLdb:
                    with conexion_MySQLdb.cursor() as cursor:
                        cursor.execute("SELECT id FROM direccion WHERE id = %s", (direccion_id,))
                        if not cursor.fetchone():
                            return "El ID de la dirección no es válido"
            except ValueError:
                return "El campo 'direccion_id' debe ser un número entero válido"
        else:
            direccion_id = entrega_actual.get('direccion_id')

        # Actualizar la entrega en la base de datos
        with connectionBD() as conexion_MySQLdb:
            with conexion_MySQLdb.cursor() as cursor:
                sql = """
                    UPDATE entrega
                    SET tipo = %s, 
                        estado = %s, 
                        costo_domicilio = %s, 
                        direccion_id = %s
                    WHERE id = %s
                """
                valores = (
                    data_form['tipo'],
                    data_form['estado'],
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
                        e.fecha_hora,
                        d.nombre_completo,
                        CONCAT(d.domicilio, ', ', COALESCE(d.barrio, ''), ' - ', COALESCE(d.referencias, '')) AS direccion_completa,
                        d.telefono,
                        m.nombre AS municipio,
                        dp.nombre AS departamento,
                        u.nombre AS nombre_usuario
                    FROM 
                        entrega e
                    LEFT JOIN 
                        direccion d ON e.direccion_id = d.id
                    LEFT JOIN 
                        users u ON d.users_id = u.id
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
                        dp.nombre LIKE %s OR
                        u.nombre LIKE %s
                    ORDER BY e.id DESC
                """
                search_pattern = f"%{search_query}%"
                cursor.execute(querySQL, (search_pattern, search_pattern, search_pattern, 
                                        search_pattern, search_pattern, search_pattern, 
                                        search_pattern, search_pattern))
                return cursor.fetchall()
    except MySQLError as err:
        print(f"Error en buscar_entregaBD: {err}")
        return []

def obtener_entregas_cliente(users_id):
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
                        e.users_id,
                        e.fecha_hora,
                        COALESCE(u.nombre, 'Usuario no disponible') AS nombre_usuario,
                        d.nombre_completo,
                        CASE
                            WHEN e.tipo = 'Domicilio' THEN 
                                CONCAT(d.domicilio, ', ', COALESCE(d.barrio, ''), ' - ', COALESCE(d.referencias, ''))
                            ELSE 'Establecimiento físico'
                        END AS direccion_completa,
                        d.telefono,
                        m.nombre AS municipio,
                        dp.nombre AS departamento
                    FROM 
                        entrega e
                    LEFT JOIN 
                        direccion d ON e.direccion_id = d.id
                    LEFT JOIN 
                        users u ON e.users_id = u.id
                    LEFT JOIN 
                        municipio m ON d.municipio_id = m.id
                    LEFT JOIN 
                        departamento dp ON d.departamento_id = dp.id
                    WHERE 
                        e.users_id = %s
                    ORDER BY e.id DESC
                """
                cursor.execute(querySQL, (users_id,))
                return cursor.fetchall()
    except MySQLError as err:
        print(f"Error de MySQL al obtener las entregas del cliente: {err}")
        return []
