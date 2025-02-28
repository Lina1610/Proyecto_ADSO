import re
from conexion.conexionBD import connectionBD
import datetime
from mysql.connector.errors import Error

from datetime import datetime
from mysql.connector import Error
from flask import request, flash, redirect, url_for
from datetime import datetime
from mysql.connector import Error

from datetime import datetime
from mysql.connector import Error
from conexion.conexionBD import connectionBD


def obtener_valores_enum(conexion, tabla, campo):
    """
    Obtiene los valores de un campo ENUM en una tabla.
    """
    try:
        with conexion.cursor(dictionary=True) as cursor:
            # Consulta para obtener los valores del ENUM
            cursor.execute(f"SHOW COLUMNS FROM {tabla} WHERE Field = '{campo}'")
            resultado = cursor.fetchone()
            
            # Extraer los valores del ENUM
            tipo_columna = resultado['Type']
            valores_enum = tipo_columna.replace("enum(", "").replace(")", "").replace("'", "").split(",")
            
            return valores_enum
    except Error as err:
        print(f"Error al obtener valores ENUM: {err}")
        return []

def obtener_metodos_pago(conexion):
    """
    Obtiene los métodos de pago (valores del ENUM) y los formatea para la plantilla.
    """
    try:
        # Obtener los valores del ENUM
        valores_enum = obtener_valores_enum(conexion, 'metodo_pago', 'metodo')
        
        # Formatear los valores para que coincidan con el formato esperado en la plantilla
        metodos_pago = [{"id": idx + 1, "metodo": valor} for idx, valor in enumerate(valores_enum)]
        
        return metodos_pago
    except Error as err:
        print(f"Error al obtener métodos de pago: {err}")
        return []

def obtener_tipos_entrega(conexion):
    """
    Obtiene los valores del ENUM 'tipo' de la tabla 'entrega'.
    """
    try:
        with conexion.cursor(dictionary=True) as cursor:
            # Consulta para obtener los valores del ENUM
            cursor.execute("SHOW COLUMNS FROM entrega WHERE Field = 'tipo'")
            resultado = cursor.fetchone()
            
            # Extraer los valores del ENUM
            tipo_columna = resultado['Type']
            valores_enum = tipo_columna.replace("enum(", "").replace(")", "").replace("'", "").split(",")
            
            print("Valores ENUM de 'tipo':", valores_enum)  # Depuración
            return valores_enum
    except Error as err:
        print(f"Error al obtener valores ENUM: {err}")
        return []

def procesar_pedido(dataForm):
    """
    Procesa y guarda un pedido en la base de datos.
    """
    try:
        # Validar que los campos no estén vacíos
        campos_requeridos = [
            'fechaEntrega', 'horaEntrega', 'estado', 'users_id', 
            'producto_id', 'metodo_pago', 'tipo_entrega'
        ]
        for campo in campos_requeridos:
            if campo not in dataForm or not dataForm[campo].strip():
                return f"El campo {campo} es obligatorio."

        # Generar fecha automáticamente
        fecha_pedido = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        # Convertir y validar fecha de entrega y hora
        try:
            fecha_entrega = datetime.strptime(dataForm['fechaEntrega'], "%Y-%m-%d").date()
            hora_entrega = datetime.strptime(dataForm['horaEntrega'], "%H:%M").time()
        except ValueError:
            return "Formato de fecha o hora no válido."

        # Validar estado del pedido
        estados_permitidos = ["Pendiente", "En Proceso", "En camino", "Entregado"]
        estado_pedido = dataForm['estado']
        if estado_pedido not in estados_permitidos:
            return f"Estado de pedido no válido. Estados permitidos: {', '.join(estados_permitidos)}"

        # Validar IDs
        try:
            users_id = int(dataForm['users_id'])
            producto_id = int(dataForm['producto_id'])
            metodo_pago_id = int(dataForm['metodo_pago'])
        except ValueError:
            return "Los campos users_id, producto_id y metodo_pago deben ser números válidos."

        # Obtener el tipo de entrega
        tipo_entrega = dataForm['tipo_entrega']

        # Obtener el ID de la entrega basado en el tipo de entrega
        with connectionBD() as conexion_MySQLdb:
            with conexion_MySQLdb.cursor(dictionary=True) as cursor:
                cursor.execute("SELECT id FROM entrega WHERE tipo = %s", (tipo_entrega,))
                entrega = cursor.fetchone()
                if not entrega:
                    return f"Tipo de entrega no válido: {tipo_entrega}"
                entrega_id = entrega['id']

        # Insertar en la tabla pedido
        with connectionBD() as conexion_MySQLdb:
            with conexion_MySQLdb.cursor() as cursor:
                sql = """
                    INSERT INTO pedido (
                        fecha, fechaEntrega, horaEntrega, estado, 
                        users_id, producto_id, metodo_pago_id, entrega_id
                    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                """
                valores = (
                    fecha_pedido,  # Fecha automática
                    fecha_entrega,  # Fecha de entrega
                    hora_entrega,   # Hora de entrega
                    estado_pedido,  # Estado del pedido
                    users_id,       # ID del usuario
                    producto_id,    # ID del producto
                    metodo_pago_id, # ID del método de pago
                    entrega_id      # ID de la entrega
                )
                cursor.execute(sql, valores)
                conexion_MySQLdb.commit()
                resultado_insert = cursor.rowcount

                if resultado_insert > 0:
                    return resultado_insert  # Éxito
                else:
                    return "No se pudo insertar el pedido en la base de datos."

    except Exception as e:
        print(f"Error en procesar_pedido: {e}")  # Debug
        return f"Se produjo un error en procesar_pedido: {str(e)}"