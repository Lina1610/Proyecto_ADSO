import re
from conexion.conexionBD import connectionBD
import datetime

def procesar_pedido(dataForm):
    try:
        # Validación de campos
        if 'fecha' not in dataForm or 'fecha_entrega' not in dataForm or 'estado_pedido' not in dataForm or 'persona_id' not in dataForm or 'entrega_id' not in dataForm:
            return "Faltan campos en el formulario."

        # Convertir las fechas de acuerdo al formato del formulario
        fecha = datetime.datetime.strptime(dataForm['fecha'], "%Y-%m-%d").date()
        fecha_entrega = datetime.datetime.strptime(dataForm['fecha_entrega'], "%Y-%m-%dT%H:%M").replace(tzinfo=None)
        estado_pedido = dataForm['estado_pedido']
        persona_id = int(dataForm['persona_id'])  # Asume que el formulario trae el ID de la persona
        entrega_id = int(dataForm['entrega_id'])  # Asume que el formulario trae el ID de la entrega

        # Validación de estado del pedido
        estados_permitidos = ["Pendiente", "En Proceso", "En camino", "Entregado"]
        if estado_pedido not in estados_permitidos:
            return "Estado de pedido no válido."

        with connectionBD() as conexion_MySQLdb:
            with conexion_MySQLdb.cursor(dictionary=True) as cursor:
                # SQL para insertar el nuevo pedido
                sql = """
                    INSERT INTO pedido (fecha, fechaEntrega, horaEntrega, estado, persona_id, entrega_id)
                    VALUES (%s, %s, %s, %s, %s, %s)
                """

                # Convertir hora de entrega a solo hora
                hora_entrega = fecha_entrega.time()

                # Crear tupla con los valores
                valores = (
                    fecha, 
                    fecha_entrega.date(),  # Fecha de entrega
                    hora_entrega,          # Hora de entrega
                    estado_pedido, 
                    persona_id, 
                    entrega_id
                )

                cursor.execute(sql, valores)  # Ejecutar consulta
                conexion_MySQLdb.commit()  # Confirmar transacción

                resultado_insert = cursor.rowcount
                if resultado_insert > 0:
                    return "Pedido registrado con éxito."
                else:
                    return "Error al registrar el pedido."

    except Exception as e:
        return f"Se produjo un error en procesar_pedido: {str(e)}"
