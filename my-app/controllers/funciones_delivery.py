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

def procesar_entrega(data_form):
    """Procesa el formulario de entrega y realiza las validaciones necesarias."""
    # Campos obligatorios
    campos_requeridos = ['tipo', 'estado', 'costo_domicilio', 'direccion_id']
    error = validar_campos_obligatorios(data_form, campos_requeridos)
    if error:
        return error

    # Validar tipo
    tipo = data_form.get('tipo')
    error = validar_tipo(tipo)
    if error:
        return error

    # Validar estado
    estado = data_form.get('estado')
    error = validar_estado(estado)
    if error:
        return error

    # Validar costo_domicilio
    costo_domicilio, error = validar_costo_domicilio(data_form.get('costo_domicilio'))
    if error:
        return error

    # Validar direccion_id
    direccion_id, error = validar_direccion_id(data_form.get('direccion_id'))
    if error:
        return error

    # Verificar que el direccion_id exista en la base de datos
    error = verificar_direccion_existe(direccion_id)
    if error:
        return error

    # Insertar la entrega en la base de datos
    id_entrega = insertar_entrega(tipo, estado, costo_domicilio, direccion_id)
    if isinstance(id_entrega, int) and id_entrega > 0:
        return id_entrega  # Éxito
    else:
        return id_entrega  # Devuelve el mensaje de error
