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
        pedido_id = int(dataForm['pedido_id'])

        with connectionBD() as conexion_MySQLdb:
            with conexion_MySQLdb.cursor(dictionary=True) as cursor:
                # Verificar existencia del pedido
                cursor.execute("SELECT id, users_id FROM pedido WHERE id = %s", (pedido_id,))
                pedido = cursor.fetchone()
                if not pedido:
                    return "El pedido seleccionado no existe"

                # Obtener el users_id del pedido
                users_id = pedido['users_id']

                # SQL para insertar la factura
                sql = """
                    INSERT INTO factura (
                        estado,
                        pedido_id,
                        users_id
                    ) VALUES (%s, %s, %s)
                """
                # Creando una tupla con los valores del INSERT
                valores = (
                    estado,
                    pedido_id,
                    users_id
                )

                cursor.execute(sql, valores)
                conexion_MySQLdb.commit()  # Confirmar la transacción
                resultado_insert = cursor.rowcount

                if resultado_insert > 0:
                    return resultado_insert  # Éxito
                else:
                    return "No se pudo insertar la factura en la base de datos"

    except ValueError:
        return "Datos numéricos inválidos. Asegúrate de que el ID del pedido sea un número válido"
    except Exception as e:
        print(f"Error en procesar_factura: {e}")  # Debug
        return f"Se produjo un error en procesar_factura: {str(e)}"