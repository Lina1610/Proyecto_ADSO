import re
from conexion.conexionBD import connectionBD
import datetime
from mysql.connector.errors import Error
from datetime import datetime

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
            
            # Extraer los valores del ENUM utilizando expresiones regulares para mayor precisión
            tipo_columna = resultado['Type']
            valores_enum = re.findall(r"'([^']*)'", tipo_columna)
            
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
        valores_enum = obtener_valores_enum(conexion, 'entrega', 'tipo')
        print("Valores ENUM de 'tipo':", valores_enum)
        return valores_enum
    except Error as err:
        print(f"Error al obtener valores ENUM: {err}")
        return []

def asegurar_registros_entrega(conexion, direccion_id=1):
    """
    Asegura que existan registros en la tabla entrega para cada tipo de entrega.
    """
    try:
        # Obtener los valores del ENUM
        tipos_entrega = obtener_valores_enum(conexion, 'entrega', 'tipo')
        
        with conexion.cursor(dictionary=True) as cursor:
            # Verificar registros existentes
            cursor.execute("SELECT id, tipo FROM entrega")
            registros_existentes = cursor.fetchall()  # Consumir todos los resultados
            
            tipos_existentes = [reg['tipo'] for reg in registros_existentes]
            print(f"Tipos existentes en BD: {tipos_existentes}")
            
            # Crear registros para tipos faltantes
            for tipo in tipos_entrega:
                if tipo not in tipos_existentes:
                    print(f"Creando registro para tipo de entrega: {tipo}")
                    # Establecer costo_domicilio basado en el tipo
                    costo = 5000 if tipo == 'Domicilio' else 0
                    
                    cursor.execute("""
                        INSERT INTO entrega (tipo, fecha_hora, estado, costo_domicilio, direccion_id) 
                        VALUES (%s, %s, %s, %s, %s)
                    """, (tipo, datetime.datetime.now(), 'Pendiente', costo, direccion_id))
            
            conexion.commit()
            
    except Error as err:
        print(f"Error al asegurar registros de entrega: {err}")

from datetime import datetime

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

        # Obtener el tipo de entrega
        tipo_entrega = dataForm['tipo_entrega'].strip()
        
        # Mostrar información de depuración
        print(f"Tipo de entrega recibido del formulario: '{tipo_entrega}'")

        # Obtener el método de pago
        metodo_pago_id = int(dataForm['metodo_pago'])
        print(f"Valor de metodo_pago_id: {metodo_pago_id}")  # Depuración

        # Paso 1: Obtener el ID de la entrega basado en el tipo de entrega
        with connectionBD() as conexion_MySQLdb:
            with conexion_MySQLdb.cursor(dictionary=True, buffered=True) as cursor:
                # Verificar que el método de pago exista
                cursor.execute("SELECT id FROM metodo_pago WHERE id = %s", (metodo_pago_id,))
                metodo_pago = cursor.fetchone()

                if not metodo_pago:
                    return f"El método de pago con ID {metodo_pago_id} no existe."

                # Obtener el ID de la entrega
                cursor.execute("SELECT id FROM entrega WHERE tipo = %s", (tipo_entrega,))
                entrega = cursor.fetchone()  # Consumir el resultado
                
                if not entrega:
                    # Si no se encuentra, intentar una búsqueda más flexible
                    cursor.execute("SELECT id, tipo FROM entrega")
                    todas_entregas = cursor.fetchall()  # Consumir TODOS los resultados
                    
                    # Buscar coincidencia ignorando mayúsculas/minúsculas
                    for e in todas_entregas:
                        if e['tipo'].lower() == tipo_entrega.lower():
                            entrega = {'id': e['id']}
                            print(f"Coincidencia encontrada: ID {e['id']} - '{e['tipo']}'")
                            break
                    
                    if not entrega:
                        return f"Tipo de entrega no válido: {tipo_entrega}. Valores disponibles: {[e['tipo'] for e in todas_entregas]}"
                
                entrega_id = entrega['id']
                print(f"ID de entrega seleccionado: {entrega_id}")

            # Paso 2: Insertar en la tabla pedido
            with conexion_MySQLdb.cursor() as cursor:
                sql = """
                    INSERT INTO pedido (
                        fecha, fechaEntrega, horaEntrega, estado, 
                        users_id, producto_id, metodo_pago_id, entrega_id
                    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                """
                valores = (
                    datetime.now().strftime('%Y-%m-%d'),  # Solo la fecha (formato DATE)
                    dataForm['fechaEntrega'],            # Fecha de entrega
                    dataForm['horaEntrega'],             # Hora de entrega
                    dataForm['estado'],                  # Estado del pedido
                    int(dataForm['users_id']),           # ID del usuario
                    int(dataForm['producto_id']),        # ID del producto
                    metodo_pago_id,                     # ID del método de pago
                    entrega_id                          # ID de la entrega
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

def obtener_pedidos(user_id=None):
    try:
        with connectionBD() as conexion_MySQLdb:
            with conexion_MySQLdb.cursor(dictionary=True) as cursor:
                querySQL = """
                    SELECT p.id, p.fecha, p.fechaEntrega, p.horaEntrega, p.estado,
                           u.nombre AS usuario_nombre, pr.nombre AS producto_nombre,
                           mp.metodo AS metodo_pago, e.tipo AS tipo_entrega,
                           COALESCE((SELECT SUM(dp.total) FROM detalle_pedido dp WHERE dp.pedido_id = p.id), 0) AS total
                    FROM pedido p
                    JOIN users u ON p.users_id = u.id
                    JOIN producto pr ON p.producto_id = pr.id
                    JOIN metodo_pago mp ON p.metodo_pago_id = mp.id
                    JOIN entrega e ON p.entrega_id = e.id
                """
                # Si se proporciona un user_id, filtrar por ese cliente
                if user_id:
                    querySQL += " WHERE p.users_id = %s"
                    querySQL += " ORDER BY p.id DESC"
                    cursor.execute(querySQL, (user_id,))
                else:
                    querySQL += " ORDER BY p.id DESC"
                    cursor.execute(querySQL)

                pedidos = cursor.fetchall()
                return pedidos
    except Exception as e:
        print(f"Error en obtener_pedidos: {e}")
        return []

def buscarPedidoBD(search):
    try:
        with connectionBD() as conexion_MySQLdb:
            with conexion_MySQLdb.cursor(dictionary=True) as cursor:
                querySQL = """
                    SELECT p.id, p.fecha, p.fechaEntrega, p.horaEntrega, p.estado,
                           u.nombre AS usuario_nombre, pr.nombre AS producto_nombre,
                           mp.metodo AS metodo_pago, e.tipo AS tipo_entrega
                    FROM pedido p
                    JOIN users u ON p.users_id = u.id
                    JOIN producto pr ON p.producto_id = pr.id
                    JOIN metodo_pago mp ON p.metodo_pago_id = mp.id
                    JOIN entrega e ON p.entrega_id = e.id
                    WHERE u.nombre LIKE %s OR pr.nombre LIKE %s OR mp.metodo LIKE %s OR e.tipo LIKE %s
                    ORDER BY p.id DESC
                """
                search_pattern = f"%{search}%"
                cursor.execute(querySQL, (search_pattern, search_pattern, search_pattern, search_pattern))
                resultado_busqueda = cursor.fetchall()
                return resultado_busqueda
    except Exception as e:
        print(f"Error en buscarPedidoBD: {e}")
        return []


def eliminar_pedido(id):
    try:
        with connectionBD() as conexion_MySQLdb:
            with conexion_MySQLdb.cursor(dictionary=True) as cursor:
                querySQL = "DELETE FROM pedido WHERE id = %s"
                cursor.execute(querySQL, (id,))
                conexion_MySQLdb.commit()
                return cursor.rowcount
    except Exception as e:
        print(f"Error en eliminar_pedido: {e}")
        return None
    
def procesar_pedido(dataForm):
    """
    Procesa y guarda un pedido en la base de datos con validaciones.
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

        # Convertir fechaEntrega y horaEntrega a objetos válidos
        fecha_entrega_str = dataForm['fechaEntrega']
        hora_entrega_str = dataForm['horaEntrega']
        
        try:
            fecha_entrega = datetime.strptime(fecha_entrega_str, '%Y-%m-%d').date()
            hora_entrega = datetime.strptime(hora_entrega_str, '%H:%M').time()
        except ValueError:
            return "Formato de fecha u hora inválido. Usa YYYY-MM-DD para fecha y HH:MM para hora."

        # Validar que la fecha no sea anterior a hoy
        hoy = date.today()
        if fecha_entrega < hoy:
            return "La fecha de entrega no puede ser anterior a hoy."

        # Validar que la hora no sea anterior si la fecha es hoy
        ahora = datetime.now().time()
        if fecha_entrega == hoy and hora_entrega < ahora:
            return "La hora de entrega no puede ser anterior a la hora actual si es para hoy."

        # Obtener el tipo de entrega
        tipo_entrega = dataForm['tipo_entrega'].strip()
        print(f"Tipo de entrega recibido del formulario: '{tipo_entrega}'")

        # Obtener el método de pago
        metodo_pago_id = int(dataForm['metodo_pago'])
        print(f"Valor de metodo_pago_id: {metodo_pago_id}")

        # Paso 1: Obtener el ID de la entrega basado en el tipo de entrega
        with connectionBD() as conexion_MySQLdb:
            with conexion_MySQLdb.cursor(dictionary=True, buffered=True) as cursor:
                # Verificar que el método de pago exista
                cursor.execute("SELECT id FROM metodo_pago WHERE id = %s", (metodo_pago_id,))
                metodo_pago = cursor.fetchone()
                if not metodo_pago:
                    return f"El método de pago con ID {metodo_pago_id} no existe."

                # Obtener el ID de la entrega
                cursor.execute("SELECT id FROM entrega WHERE tipo = %s", (tipo_entrega,))
                entrega = cursor.fetchone()
                if not entrega:
                    cursor.execute("SELECT id, tipo FROM entrega")
                    todas_entregas = cursor.fetchall()
                    for e in todas_entregas:
                        if e['tipo'].lower() == tipo_entrega.lower():
                            entrega = {'id': e['id']}
                            break
                    if not entrega:
                        return f"Tipo de entrega no válido: {tipo_entrega}. Valores disponibles: {[e['tipo'] for e in todas_entregas]}"
                
                entrega_id = entrega['id']
                print(f"ID de entrega seleccionado: {entrega_id}")

            # Paso 2: Insertar en la tabla pedido
            with conexion_MySQLdb.cursor() as cursor:
                sql = """
                    INSERT INTO pedido (
                        fecha, fechaEntrega, horaEntrega, estado, 
                        users_id, producto_id, metodo_pago_id, entrega_id
                    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                """
                valores = (
                    datetime.now().strftime('%Y-%m-%d'),
                    fecha_entrega_str,
                    hora_entrega_str,
                    dataForm['estado'],
                    int(dataForm['users_id']),
                    int(dataForm['producto_id']),
                    metodo_pago_id,
                    entrega_id
                )
                cursor.execute(sql, valores)
                conexion_MySQLdb.commit()
                resultado_insert = cursor.rowcount

            if resultado_insert > 0:
                return resultado_insert  # Éxito
            else:
                return "No se pudo insertar el pedido en la base de datos."

    except Exception as e:
        print(f"Error en procesar_pedido: {e}")
        return f"Se produjo un error al procesar el pedido: {str(e)}"

import datetime
from conexion.conexionBD import connectionBD

def actualizar_pedido(id, dataForm):
    try:
        # Validar que los campos no estén vacíos
        campos_requeridos = [
            'fechaEntrega', 'horaEntrega', 'estado', 'users_id', 
            'producto_id', 'metodo_pago', 'tipo_entrega'
        ]
        for campo in campos_requeridos:
            if campo not in dataForm or not dataForm[campo].strip():
                return f"El campo {campo} es obligatorio."

        # Convertir fechaEntrega y horaEntrega
        fecha_entrega_str = dataForm['fechaEntrega'].strip()
        hora_entrega_str = dataForm['horaEntrega'].strip()
        print(f"Fecha recibida: '{fecha_entrega_str}' (tipo: {type(fecha_entrega_str)})")
        print(f"Hora recibida: '{hora_entrega_str}' (tipo: {type(hora_entrega_str)})")

        # Verificar si los valores están vacíos
        if not fecha_entrega_str or not hora_entrega_str:
            return "Los campos fechaEntrega y horaEntrega no pueden estar vacíos."

        # Intentar parsear con manejo de formatos adicionales
        try:
            fecha_entrega = datetime.datetime.strptime(fecha_entrega_str, '%Y-%m-%d').date()
        except ValueError:
            try:
                # Manejar formatos alternativos como DD/MM/YYYY si es necesario
                fecha_entrega = datetime.datetime.strptime(fecha_entrega_str, '%d/%m/%Y').date()
                fecha_entrega_str = fecha_entrega.strftime('%Y-%m-%d')  # Convertir al formato esperado
            except ValueError:
                print(f"Error al parsear fecha: Fecha: '{fecha_entrega_str}'")
                return "Formato de fecha inválido. Usa YYYY-MM-DD."

        try:
            hora_entrega = datetime.datetime.strptime(hora_entrega_str, '%H:%M').time()
        except ValueError:
            try:
                # Manejar HH:MM:SS si viene con segundos
                hora_entrega = datetime.datetime.strptime(hora_entrega_str, '%H:%M:%S').time()
                hora_entrega_str = hora_entrega.strftime('%H:%M')  # Convertir al formato esperado
            except ValueError:
                print(f"Error al parsear hora: Hora: '{hora_entrega_str}'")
                return "Formato de hora inválido. Usa HH:MM."

        # Validar que la fecha no sea anterior a hoy
        hoy = datetime.date.today()
        if fecha_entrega < hoy:
            return "La fecha de entrega no puede ser anterior a hoy."

        # Validar que la hora no sea anterior si la fecha es hoy
        ahora = datetime.datetime.now().time()
        if fecha_entrega == hoy and hora_entrega < ahora:
            return "La hora de entrega no puede ser anterior a la hora actual si es para hoy."

        # Obtener el tipo de entrega
        tipo_entrega = dataForm['tipo_entrega'].strip()
        print(f"Tipo de entrega recibido del formulario: '{tipo_entrega}'")

        # Obtener el método de pago
        metodo_pago_id = int(dataForm['metodo_pago'])
        print(f"Valor de metodo_pago_id: {metodo_pago_id}")

        # Actualizar el pedido en la base de datos
        with connectionBD() as conexion_MySQLdb:
            with conexion_MySQLdb.cursor(dictionary=True, buffered=True) as cursor:
                # Verificar que el método de pago exista
                cursor.execute("SELECT id FROM metodo_pago WHERE id = %s", (metodo_pago_id,))
                metodo_pago = cursor.fetchone()
                if not metodo_pago:
                    return f"El método de pago con ID {metodo_pago_id} no existe."

                # Obtener el ID de la entrega
                cursor.execute("SELECT id FROM entrega WHERE tipo = %s", (tipo_entrega,))
                entrega = cursor.fetchone()
                if not entrega:
                    cursor.execute("SELECT id, tipo FROM entrega")
                    todas_entregas = cursor.fetchall()
                    for e in todas_entregas:
                        if e['tipo'].lower() == tipo_entrega.lower():
                            entrega = {'id': e['id']}
                            break
                    if not entrega:
                        return f"Tipo de entrega no válido: {tipo_entrega}. Valores disponibles: {[e['tipo'] for e in todas_entregas]}"
                
                entrega_id = entrega['id']
                print(f"ID de entrega seleccionado: {entrega_id}")

                # Actualizar el pedido
                sql = """
                    UPDATE pedido 
                    SET fechaEntrega = %s, horaEntrega = %s, estado = %s, 
                        users_id = %s, producto_id = %s, metodo_pago_id = %s, entrega_id = %s
                    WHERE id = %s
                """
                valores = (
                    fecha_entrega_str,
                    hora_entrega_str,
                    dataForm['estado'],
                    int(dataForm['users_id']),
                    int(dataForm['producto_id']),
                    metodo_pago_id,
                    entrega_id,
                    id
                )
                cursor.execute(sql, valores)
                conexion_MySQLdb.commit()
                return cursor.rowcount > 0

    except Exception as e:
        print(f"Error en actualizar_pedido: {e}")
        return f"Se produjo un error al actualizar el pedido: {str(e)}"