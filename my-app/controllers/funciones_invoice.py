from werkzeug.utils import secure_filename
import uuid
from conexion.conexionBD import connectionBD
from flask import session
import re

def procesar_factura(dataForm):
    try:
        # Validación de campos requeridos
        campos_requeridos = ['estado', 'pedido_id']
        for campo in campos_requeridos:
            if campo not in dataForm or not dataForm[campo].strip():
                return f"El campo {campo.replace('_', ' ').title()} es requerido"

        # Validación del estado
        estado = dataForm['estado'].strip()
        if estado not in ['Pendiente', 'Facturado']:
            return "Estado de factura inválido. Debe ser 'Pendiente' o 'Facturado'"

        # Conversión de pedido_id a entero
        try:
            pedido_id = int(dataForm['pedido_id'])
        except ValueError:
            return "Datos numéricos inválidos. Asegúrate de que el ID del pedido sea un número válido"

        with connectionBD() as conexion_MySQLdb:
            with conexion_MySQLdb.cursor(dictionary=True) as cursor:
                # Verificar existencia del pedido
                cursor.execute("SELECT id FROM pedido WHERE id = %s", (pedido_id,))
                pedido = cursor.fetchone()
                if not pedido:
                    return "El pedido seleccionado no existe"

                # SQL para insertar la factura (sin users_id)
                sql = """
                    INSERT INTO factura (
                        estado,
                        pedido_id
                    ) VALUES (%s, %s)
                """
                # Creando una tupla con los valores del INSERT
                valores = (
                    estado,
                    pedido_id
                )

                cursor.execute(sql, valores)
                conexion_MySQLdb.commit()  # Confirmar la transacción
                resultado_insert = cursor.rowcount

                if resultado_insert > 0:
                    return resultado_insert  # Éxito
                else:
                    return "No se pudo insertar la factura en la base de datos"

    except Exception as e:
        print(f"Error en procesar_factura: {e}")  # Debug
        return f"Se produjo un error en procesar_factura: {str(e)}"
    
def obtener_facturas():
    try:
        with connectionBD() as conexion_MySQLdb:
            with conexion_MySQLdb.cursor(dictionary=True) as cursor:
                cursor.execute("SELECT * FROM factura")
                facturas = cursor.fetchall()
                return facturas
    except Exception as e:
        print(f"Error en obtener_facturas: {e}")
        return []

def buscarFacturaBD(search_query):
    try:
        with connectionBD() as conexion_MySQLdb:
            with conexion_MySQLdb.cursor(dictionary=True) as cursor:
                cursor.execute("""
                    SELECT * FROM factura
                    WHERE estado LIKE %s OR fecha LIKE %s OR pedido_id LIKE %s
                """, (f"%{search_query}%", f"%{search_query}%", f"%{search_query}%"))
                facturas = cursor.fetchall()
                return facturas
    except Exception as e:
        print(f"Error en buscarFacturaBD: {e}")
        return []

def eliminar_factura(id):
    try:
        with connectionBD() as conexion_MySQLdb:
            with conexion_MySQLdb.cursor() as cursor:
                cursor.execute("DELETE FROM factura WHERE id = %s", (id,))
                conexion_MySQLdb.commit()
                return cursor.rowcount
    except Exception as e:
        print(f"Error en eliminar_factura: {e}")
        return 0

def actualizar_factura(id, data_form):
    try:
        with connectionBD() as conexion_MySQLdb:
            with conexion_MySQLdb.cursor() as cursor:
                sql = """
                    UPDATE factura
                    SET estado = %s, fecha = %s, pedido_id = %s
                    WHERE id = %s
                """
                valores = (
                    data_form['estado'],
                    data_form['fecha'],
                    data_form['pedido_id'],
                    id
                )
                cursor.execute(sql, valores)
                conexion_MySQLdb.commit()
                return True
    except Exception as e:
        print(f"Error en actualizar_factura: {e}")
        return str(e)
    
