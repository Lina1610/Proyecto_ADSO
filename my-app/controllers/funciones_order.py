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

        # Paso 1: Obtener el ID de la entrega basado en el tipo de entrega
        with connectionBD() as conexion_MySQLdb:
            with conexion_MySQLdb.cursor(dictionary=True) as cursor:
                # Consulta para obtener el ID de la entrega
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
                    datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),  # Fecha automática
                    dataForm['fechaEntrega'],                              # Fecha de entrega
                    dataForm['horaEntrega'],                               # Hora de entrega
                    dataForm['estado'],                                    # Estado del pedido
                    int(dataForm['users_id']),                             # ID del usuario
                    int(dataForm['producto_id']),                          # ID del producto
                    int(dataForm['metodo_pago']),                          # ID del método de pago
                    entrega_id                                             # ID de la entrega
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