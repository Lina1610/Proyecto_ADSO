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