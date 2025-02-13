import re
from conexion.conexionBD import connectionBD
import datetime
from mysql.connector.errors import Error

def procesar_pedido(dataForm):
    try:
        # Validación de campos obligatorios
        campos_requeridos = ['fecha', 'fecha_entrega', 'estado_pedido', 'persona_id', 'entrega_id']
        for campo in campos_requeridos:
            if campo not in dataForm or not dataForm[campo]:
                return f"El campo {campo} es obligatorio."

        # Convertir fechas y hora
        try:
            fecha = datetime.datetime.strptime(dataForm['fecha'], "%Y-%m-%d").date()
            fecha_entrega = datetime.datetime.strptime(dataForm['fecha_entrega'], "%Y-%m-%dT%H:%M")
            hora_entrega = fecha_entrega.time()
        except ValueError:
            return "Formato de fecha o hora no válido. Verifica los campos de fecha."

        # Validar estado del pedido
        estados_permitidos = ["Pendiente", "En Proceso", "En camino", "Entregado"]
        estado_pedido = dataForm['estado_pedido']
        if estado_pedido not in estados_permitidos:
            return f"Estado de pedido no válido. Estados permitidos: {', '.join(estados_permitidos)}"

        # Validar IDs
        try:
            persona_id = int(dataForm['persona_id'])
            entrega_id = int(dataForm['entrega_id'])
        except ValueError:
            return "Los campos persona_id y entrega_id deben ser números válidos."

        # Insertar en la base de datos
        with connectionBD() as conexion_MySQLdb:
            with conexion_MySQLdb.cursor(dictionary=True) as cursor:
                sql = """
                    INSERT INTO pedido (fecha, fechaEntrega, horaEntrega, estado, persona_id, entrega_id)
                    VALUES (%s, %s, %s, %s, %s, %s)
                """
                valores = (fecha, fecha_entrega.date(), hora_entrega, estado_pedido, persona_id, entrega_id)
                cursor.execute(sql, valores)
                conexion_MySQLdb.commit()

                if cursor.rowcount > 0:
                    return "Pedido registrado con éxito."
                else:
                    return "Error al registrar el pedido."

    except Error as db_error:
        return f"Error en la base de datos: {str(db_error)}"
    except Exception as e:
        return f"Se produjo un error inesperado: {str(e)}"
