from datetime import datetime
from mysql.connector import Error as MySQLError
from conexion.conexionBD import connectionBD



def validar_campos_obligatorios(data_form, campos_requeridos):
    """Valida que los campos obligatorios no estén vacíos."""
    for campo in campos_requeridos:
        if campo not in data_form or not data_form[campo].strip():
            return f"El campo {campo} es obligatorio."
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