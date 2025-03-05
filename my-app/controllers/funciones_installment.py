from werkzeug.utils import secure_filename
import uuid
from conexion.conexionBD import connectionBD
from flask import session
import re

def procesar_abono(dataForm):
    try:
        campos_requeridos = ['numero_abonos', 'estado', 'monto', 'pedido_id']
        for campo in campos_requeridos:
            if campo not in dataForm or not dataForm[campo].strip():
                return f"El campo {campo.replace('_', ' ').title()} es requerido"

        numero_abonos = dataForm['numero_abonos'].strip()
        if numero_abonos not in ['Pago inicial', 'Pago final']:
            return "Número de abono inválido. Debe ser 'Pago inicial' o 'Pago final'"

        estado = dataForm['estado'].strip()
        if estado not in ['Abono Pendiente', 'Abono confirmado']:
            return "Estado de abono inválido. Debe ser 'Abono Pendiente' o 'Abono confirmado'"

        try:
            monto = float(dataForm['monto'])
            if monto <= 0:
                return "El monto debe ser un valor positivo"
        except ValueError:
            return "El monto debe ser un número válido"

        try:
            pedido_id = int(dataForm['pedido_id'])
        except ValueError:
            return "Datos numéricos inválidos. Asegúrate de que el ID del pedido sea un número válido"

        with connectionBD() as conexion_MySQLdb:
            with conexion_MySQLdb.cursor(dictionary=True) as cursor:
                cursor.execute("SELECT id FROM pedido WHERE id = %s", (pedido_id,))
                pedido = cursor.fetchone()
                if not pedido:
                    return "El pedido seleccionado no existe"

                sql = """
                    INSERT INTO abono (
                        numero_abonos,
                        estado,
                        monto,
                        pedido_id
                    ) VALUES (%s, %s, %s, %s)
                """
                valores = (
                    numero_abonos,
                    estado,
                    monto,
                    pedido_id
                )

                cursor.execute(sql, valores)
                conexion_MySQLdb.commit()
                resultado_insert = cursor.rowcount

                if resultado_insert > 0:
                    return resultado_insert
                else:
                    return "No se pudo insertar el abono en la base de datos"

    except Exception as e:
        print(f"Error en procesar_abono: {e}")
        return f"Se produjo un error en procesar_abono: {str(e)}"
    
def obtener_abonos():
    try:
        with connectionBD() as conexion_MySQLdb:
            with conexion_MySQLdb.cursor(dictionary=True) as cursor:
                cursor.execute("""
                    SELECT id, numero_abonos, estado, monto, pedido_id
                    FROM abono
                """)
                abonos = cursor.fetchall()
                print("Abonos encontrados:", abonos)  # Depuración
                return abonos
    except Exception as e:
        print(f"Error al obtener abonos: {e}")
        return []
    
def actualizar_abono(id, data_form):
    try:
        print("Datos recibidos:", data_form)  # Depuración
        campos_requeridos = ['numero_abonos', 'estado', 'monto', 'pedido_id']
        for campo in campos_requeridos:
            if campo not in data_form or not data_form[campo].strip():
                return f"El campo {campo.replace('_', ' ').title()} es requerido"

        numero_abonos = data_form['numero_abonos'].strip()
        if numero_abonos not in ['Pago inicial', 'Pago final']:
            return "Número de abono inválido. Debe ser 'Pago inicial' o 'Pago final'"

        estado = data_form['estado'].strip()
        if estado not in ['Abono Pendiente', 'Abono confirmado']:
            return "Estado de abono inválido. Debe ser 'Abono Pendiente' o 'Abono confirmado'"

        try:
            monto = float(data_form['monto'])
            if monto <= 0:
                return "El monto debe ser un valor positivo"
        except ValueError:
            return "El monto debe ser un número válido"

        try:
            pedido_id = int(data_form['pedido_id'])
        except ValueError:
            return "Datos numéricos inválidos. Asegúrate de que el ID del pedido sea un número válido"

        with connectionBD() as conexion_MySQLdb:
            with conexion_MySQLdb.cursor() as cursor:
                sql = """
                    UPDATE abono
                    SET numero_abonos = %s,
                        estado = %s,
                        monto = %s,
                        pedido_id = %s
                    WHERE id = %s
                """
                valores = (
                    numero_abonos,
                    estado,
                    monto,
                    pedido_id,
                    id
                )

                cursor.execute(sql, valores)
                conexion_MySQLdb.commit()
                resultado_update = cursor.rowcount

                if resultado_update > 0:
                    return True  # Éxito
                else:
                    return "No se pudo actualizar el abono en la base de datos"

    except Exception as e:
        print(f"Error en actualizar_abono: {e}")
        return f"Se produjo un error en actualizar_abono: {str(e)}"
    

def buscarAbonoBD(search_query):
    try:
        with connectionBD() as conexion_MySQLdb:
            with conexion_MySQLdb.cursor(dictionary=True) as cursor:
                querySQL = """
                    SELECT 
                        abono.id,
                        abono.numero_abonos,
                        abono.estado,
                        abono.monto,
                        abono.pedido_id,
                        pedido.fecha AS fecha_pedido,
                        users.nombre AS nombre_usuario
                    FROM 
                        abono
                    JOIN 
                        pedido ON abono.pedido_id = pedido.id
                    JOIN 
                        users ON pedido.users_id = u.id
                    WHERE 
                        abono.numero_abonos LIKE %s OR
                        abono.estado LIKE %s OR
                        abono.monto LIKE %s OR
                        pedido.fecha LIKE %s OR
                        users.nombre LIKE %s
                """
                search_pattern = f"%{search_query}%"
                cursor.execute(querySQL, (search_pattern, search_pattern, search_pattern, search_pattern, search_pattern))
                return cursor.fetchall()
    except Exception as e:
        print(f"Error en buscarAbonoBD: {e}")
        return None
    
def eliminar_abono(id):
    try:
        with connectionBD() as conexion_MySQLdb:
            with conexion_MySQLdb.cursor() as cursor:
                querySQL = "DELETE FROM abono WHERE id = %s"
                cursor.execute(querySQL, (id,))
                conexion_MySQLdb.commit()
                return cursor.rowcount  # Retorna el número de filas afectadas
    except Exception as e:
        print(f"Error en eliminar_abono: {e}")
        return None
    


