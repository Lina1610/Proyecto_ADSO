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
                return f"El campo {campo.replace('_', ' ').title()} es requerido."

        # Obtener los valores del formulario
        estado = dataForm['estado'].strip()
        pedido_id_str = dataForm['pedido_id'].strip()

        # Validación del estado
        if estado not in ['Pendiente', 'Facturado']:
            return "El estado de la factura debe ser 'Pendiente' o 'Facturado'."
        
        # Validar longitud del estado (por seguridad, aunque es un ENUM)
        if len(estado) > 20:  # Límite arbitrario, ya que 'Facturado' tiene 9 caracteres
            return "El estado de la factura es demasiado largo."

        # Validar que el estado no contenga caracteres extraños (solo letras)
        if not re.match(r'^[A-Za-z]+$', estado):
            return "El estado de la factura solo puede contener letras."

        # Validación del pedido_id
        try:
            pedido_id = int(pedido_id_str)
            if pedido_id <= 0:
                return "El ID del pedido debe ser un número positivo mayor que 0."
        except ValueError:
            return "El ID del pedido debe ser un número entero válido."

        with connectionBD() as conexion_MySQLdb:
            with conexion_MySQLdb.cursor(dictionary=True) as cursor:
                # Verificar existencia del pedido
                cursor.execute("SELECT id, estado FROM pedido WHERE id = %s", (pedido_id,))
                pedido = cursor.fetchone()
                if not pedido:
                    return "El pedido seleccionado no existe."

                # Opcional: Validar el estado del pedido (por ejemplo, no permitir facturas para pedidos cancelados)
                # Esto depende de tu lógica de negocio. Supongamos que 'pedido' tiene un campo 'estado'
                # y que no quieres permitir facturas para pedidos cancelados.
                if 'estado' in pedido and pedido['estado'].lower() == 'cancelado':
                    return "No se puede crear una factura para un pedido cancelado."

                # SQL para insertar la factura (sin fecha, ya que es TIMESTAMP)
                sql = """
                    INSERT INTO factura (
                        estado,
                        pedido_id
                    ) VALUES (%s, %s)
                """
                valores = (
                    estado,
                    pedido_id
                )

                cursor.execute(sql, valores)
                conexion_MySQLdb.commit()
                resultado_insert = cursor.rowcount

                if resultado_insert > 0:
                    return resultado_insert  # Éxito
                else:
                    return "No se pudo insertar la factura en la base de datos."

    except Exception as e:
        print(f"Error en procesar_factura: {e}")
        return f"Se produjo un error al procesar la factura: {str(e)}"
    
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
                querySQL = """
                    SELECT * FROM factura
                    WHERE estado LIKE %s OR fecha LIKE %s OR pedido_id LIKE %s
                    ORDER BY id DESC
                """
                search_pattern = f"%{search_query}%"
                cursor.execute(querySQL, (search_pattern, search_pattern, search_pattern))
                facturas = cursor.fetchall()
                return facturas
    except Exception as e:
        print(f"Error en buscarFacturaBD: {e}")
        return []

def eliminar_factura(id):
    """Elimina una factura por su ID."""
    try:
        with connectionBD() as conexion_MySQLdb:
            with conexion_MySQLdb.cursor() as cursor:
                # Verificar si la factura existe antes de eliminar
                cursor.execute("SELECT id FROM factura WHERE id = %s", (id,))
                existe_antes = cursor.fetchone() is not None

                if not existe_antes:
                    return False  # La factura no existía para empezar

                # Intentar eliminar
                cursor.execute("DELETE FROM factura WHERE id = %s", (id,))
                conexion_MySQLdb.commit()

                # Verificar si la factura ya no existe
                cursor.execute("SELECT id FROM factura WHERE id = %s", (id,))
                existe_despues = cursor.fetchone() is not None

                # Si ya no existe, la eliminación fue exitosa
                return existe_antes and not existe_despues
    except Exception as e:
        print(f"Error en eliminar_factura: {e}")
        return False

def actualizar_factura(id, data_form):
    try:
        with connectionBD() as conexion_MySQLdb:
            with conexion_MySQLdb.cursor() as cursor:
                # Validación de campos requeridos
                campos_requeridos = ['estado', 'pedido_id']
                for campo in campos_requeridos:
                    if campo not in data_form or not data_form[campo].strip():
                        return f"El campo {campo.replace('_', ' ').title()} es requerido."

                estado = data_form['estado'].strip()
                pedido_id_str = data_form['pedido_id'].strip()

                # Validación del estado
                if estado not in ['Pendiente', 'Facturado']:
                    return "El estado de la factura debe ser 'Pendiente' o 'Facturado'."

                if len(estado) > 20:
                    return "El estado de la factura es demasiado largo."

                if not re.match(r'^[A-Za-z]+$', estado):
                    return "El estado de la factura solo puede contener letras."

                # Validación del pedido_id
                try:
                    pedido_id = int(pedido_id_str)
                    if pedido_id <= 0:
                        return "El ID del pedido debe ser un número positivo mayor que 0."
                except ValueError:
                    return "El ID del pedido debe ser un número entero válido."

                # Verificar existencia del pedido
                cursor.execute("SELECT id, estado FROM pedido WHERE id = %s", (pedido_id,))
                pedido = cursor.fetchone()
                if not pedido:
                    return "El pedido seleccionado no existe."

                if 'estado' in pedido and pedido['estado'].lower() == 'cancelado':
                    return "No se puede actualizar una factura para un pedido cancelado."

                # Actualizar la factura
                sql = """
                    UPDATE factura
                    SET estado = %s, pedido_id = %s
                    WHERE id = %s
                """
                valores = (
                    estado,
                    pedido_id,
                    id
                )
                cursor.execute(sql, valores)
                conexion_MySQLdb.commit()
                return True
    except Exception as e:
        print(f"Error en actualizar_factura: {e}")
        return str(e)
