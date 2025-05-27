from werkzeug.utils import secure_filename
import uuid
from conexion.conexionBD import connectionBD
from flask import session
import re

# Constantes para límites
MAX_MONTO = 9999999999  # Límite de DECIMAL(10,0)

def validar_monto(monto):
    """
    Valida que el monto sea un número entero positivo y no exceda el límite.
    """
    try:
        monto = float(monto)
        if monto <= 0:
            return False, "El monto debe ser un valor positivo"
        if monto > MAX_MONTO:
            return False, "El monto no puede exceder 9999999999"
        if not monto.is_integer():
            return False, "El monto debe ser un número entero (sin decimales)"
        return True, None
    except (ValueError, TypeError):
        return False, "El monto debe ser un número válido"

def validar_id(id_value, nombre_campo):
    """
    Valida que un ID sea un número entero positivo.
    """
    try:
        id_value = int(id_value)
        if id_value <= 0:
            return False, f"El {nombre_campo} debe ser un número positivo"
        return True, None
    except (ValueError, TypeError):
        return False, f"El {nombre_campo} debe ser un número entero"

def validar_abono_final(abono_final):
    """
    Valida el campo abono_final (opcional, DECIMAL(10,0)).
    """
    if not abono_final or abono_final.strip() == '':
        return True, None  # Permitir valores nulos o vacíos
    try:
        abono_final = float(abono_final)
        if abono_final < 0:
            return False, "El abono final no puede ser negativo"
        if abono_final > MAX_MONTO:
            return False, "El abono final no puede exceder 9999999999"
        if not abono_final.is_integer():
            return False, "El abono final debe ser un número entero (sin decimales)"
        return True, None
    except (ValueError, TypeError):
        return False, "El abono final debe ser un número válido"

def pedido_existe(pedido_id):
    """
    Verifica si un pedido existe en la base de datos.
    """
    try:
        with connectionBD() as conexion:
            with conexion.cursor(dictionary=True) as cursor:
                cursor.execute("SELECT id FROM pedido WHERE id = %s", (pedido_id,))
                return cursor.fetchone() is not None
    except Exception as e:
        print(f"Error al verificar pedido: {e}")
        return False

def abono_duplicado(pedido_id, numero_abonos, abono_id=None):
    """
    Verifica si ya existe un abono con el mismo pedido_id y numero_abonos.
    Si abono_id se proporciona, excluye ese abono (para actualizaciones).
    """
    try:
        with connectionBD() as conexion:
            with conexion.cursor(dictionary=True) as cursor:
                if abono_id:
                    sql = "SELECT id FROM abono WHERE pedido_id = %s AND numero_abonos = %s AND id != %s"
                    cursor.execute(sql, (pedido_id, numero_abonos, abono_id))
                else:
                    sql = "SELECT id FROM abono WHERE pedido_id = %s AND numero_abonos = %s"
                    cursor.execute(sql, (pedido_id, numero_abonos))
                return cursor.fetchone() is not None
    except Exception as e:
        print(f"Error al verificar duplicados: {e}")
        return False

def procesar_abono(dataForm):
    """
    Procesa la inserción de un nuevo abono con validaciones.
    """
    try:
        # Validar campos requeridos
        campos_requeridos = ['numero_abonos', 'estado', 'monto', 'pedido_id']
        for campo in campos_requeridos:
            if campo not in dataForm or not dataForm[campo].strip():
                return f"El campo {campo.replace('_', ' ').title()} es obligatorio"

        numero_abonos = dataForm['numero_abonos'].strip()
        if numero_abonos not in ['Pago inicial', 'Pago final']:
            return "El número de abono debe ser 'Pago inicial' o 'Pago final'"

        estado = dataForm['estado'].strip()
        if estado not in ['Abono Pendiente', 'Abono confirmado']:
            return "El estado debe ser 'Abono Pendiente' o 'Abono confirmado'"

        # Validar monto
        es_valido, mensaje = validar_monto(dataForm['monto'])
        if not es_valido:
            return mensaje
        monto = float(dataForm['monto'])

        # Validar pedido_id
        es_valido, mensaje = validar_id(dataForm['pedido_id'], "ID del pedido")
        if not es_valido:
            return mensaje
        pedido_id = int(dataForm['pedido_id'])

        # Validar abono_final
        abono_final = dataForm.get('abono_final', '').strip()
        es_valido, mensaje = validar_abono_final(abono_final)
        if not es_valido:
            return mensaje
        abono_final_value = float(abono_final) if abono_final else None

        # Verificar si el pedido existe
        if not pedido_existe(pedido_id):
            return "El pedido seleccionado no existe"

        # Verificar duplicados
        if abono_duplicado(pedido_id, numero_abonos):
            return "Ya existe un abono de tipo '{}' para este pedido".format(numero_abonos)

        with connectionBD() as conexion_MySQLdb:
            with conexion_MySQLdb.cursor(dictionary=True) as cursor:
                sql = """
                    INSERT INTO abono (
                        numero_abonos,
                        estado,
                        monto,
                        pedido_id,
                        abono_final
                    ) VALUES (%s, %s, %s, %s, %s)
                """
                valores = (
                    numero_abonos,
                    estado,
                    monto,
                    pedido_id,
                    abono_final_value
                )

                cursor.execute(sql, valores)
                conexion_MySQLdb.commit()
                resultado_insert = cursor.rowcount

                if resultado_insert > 0:
                    return resultado_insert
                else:
                    return "No se pudo registrar el abono en la base de datos"

    except Exception as e:
        print(f"Error al procesar el abono: {e}")
        return f"Se produjo un error al registrar el abono: {str(e)}"

def obtener_abonos():
    """
    Obtiene todos los abonos de la base de datos.
    """
    try:
        with connectionBD() as conexion_MySQLdb:
            with conexion_MySQLdb.cursor(dictionary=True) as cursor:
                cursor.execute("""
                    SELECT id, numero_abonos, estado, monto, pedido_id, abono_final
                    FROM abono
                """)
                abonos = cursor.fetchall()
                print("Abonos encontrados:", abonos)
                return abonos
    except Exception as e:
        print(f"Error al obtener abonos: {e}")
        return []

def actualizar_abono(id, data_form):
    """
    Actualiza un abono existente con validaciones.
    """
    try:
        # Validar ID del abono
        es_valido, mensaje = validar_id(id, "ID del abono")
        if not es_valido:
            return mensaje

        # Validar campos requeridos
        campos_requeridos = ['numero_abonos', 'estado', 'monto', 'pedido_id']
        for campo in campos_requeridos:
            if campo not in data_form or not data_form[campo].strip():
                return f"El campo {campo.replace('_', ' ').title()} es obligatorio"

        numero_abonos = data_form['numero_abonos'].strip()
        if numero_abonos not in ['Pago inicial', 'Pago final']:
            return "El número de abono debe ser 'Pago inicial' o 'Pago final'"

        estado = data_form['estado'].strip()
        if estado not in ['Abono Pendiente', 'Abono confirmado']:
            return "El estado debe ser 'Abono Pendiente' o 'Abono confirmado'"

        # Validar monto
        es_valido, mensaje = validar_monto(data_form['monto'])
        if not es_valido:
            return mensaje
        monto = float(data_form['monto'])

        # Validar pedido_id
        es_valido, mensaje = validar_id(data_form['pedido_id'], "ID del pedido")
        if not es_valido:
            return mensaje
        pedido_id = int(data_form['pedido_id'])

        # Validar abono_final
        abono_final = data_form.get('abono_final', '').strip()
        es_valido, mensaje = validar_abono_final(abono_final)
        if not es_valido:
            return mensaje
        abono_final_value = float(abono_final) if abono_final else None

        # Verificar si el pedido existe
        if not pedido_existe(pedido_id):
            return "El pedido seleccionado no existe"

        # Verificar duplicados (excluyendo el abono actual)
        if abono_duplicado(pedido_id, numero_abonos, id):
            return "Ya existe un abono de tipo '{}' para este pedido".format(numero_abonos)

        with connectionBD() as conexion_MySQLdb:
            with conexion_MySQLdb.cursor() as cursor:
                sql = """
                    UPDATE abono
                    SET numero_abonos = %s,
                        estado = %s,
                        monto = %s,
                        pedido_id = %s,
                        abono_final = %s
                    WHERE id = %s
                """
                valores = (
                    numero_abonos,
                    estado,
                    monto,
                    pedido_id,
                    abono_final_value,
                    id
                )

                cursor.execute(sql, valores)
                conexion_MySQLdb.commit()
                resultado_update = cursor.rowcount

                if resultado_update > 0:
                    return True
                else:
                    return "No se pudo actualizar el abono en la base de datos"

    except Exception as e:
        print(f"Error al actualizar el abono: {e}")
        return f"Se produjo un error al actualizar el abono: {str(e)}"

def buscarAbonoBD(search_query):
    """
    Busca abonos en la base de datos según un término de búsqueda.
    """
    try:
        # Sanitizar el término de búsqueda
        search_query = search_query.strip()
        if not search_query:
            return None

        with connectionBD() as conexion_MySQLdb:
            with conexion_MySQLdb.cursor(dictionary=True) as cursor:
                querySQL = """
                    SELECT 
                        abono.id,
                        abono.numero_abonos,
                        abono.estado,
                        abono.monto,
                        abono.pedido_id,
                        abono.abono_final,
                        pedido.fecha AS fecha_pedido,
                        users.nombre AS nombre_usuario
                    FROM 
                        abono
                    JOIN 
                        pedido ON abono.pedido_id = pedido.id
                    JOIN 
                        users ON pedido.users_id = users.id
                    WHERE 
                        abono.numero_abonos LIKE %s OR
                        abono.estado LIKE %s OR
                        abono.monto LIKE %s OR
                        abono.abono_final LIKE %s OR
                        pedido.fecha LIKE %s OR
                        users.nombre LIKE %s
                """
                search_pattern = f"%{search_query}%"
                cursor.execute(querySQL, (search_pattern, search_pattern, search_pattern, search_pattern, search_pattern, search_pattern))
                return cursor.fetchall()
    except Exception as e:
        print(f"Error al buscar abonos: {e}")
        return None

def eliminar_abono(id):
    """
    Elimina un abono por su ID.
    """
    try:
        # Validar ID del abono
        es_valido, mensaje = validar_id(id, "ID del abono")
        if not es_valido:
            return mensaje

        with connectionBD() as conexion_MySQLdb:
            with conexion_MySQLdb.cursor() as cursor:
                # Verificar si el abono existe antes de eliminar
                cursor.execute("SELECT id FROM abono WHERE id = %s", (id,))
                existe_antes = cursor.fetchone() is not None

                if not existe_antes:
                    return False

                # Intentar eliminar
                cursor.execute("DELETE FROM abono WHERE id = %s", (id,))
                conexion_MySQLdb.commit()

                # Verificar si el abono ya no existe
                cursor.execute("SELECT id FROM abono WHERE id = %s", (id,))
                existe_despues = cursor.fetchone() is not None

                return existe_antes and not existe_despues
    except Exception as e:
        print(f"Error al eliminar el abono: {e}")
        return False
