from conexion.conexionBD import connectionBD
from datetime import date

def agregar_al_carrito(producto_id, cantidad, users_id):
    """
    Agrega un producto al carrito de compras o actualiza la cantidad si ya existe
    """
    try:
        conexion = connectionBD()
        cursor = conexion.cursor(dictionary=True)
        
        # Verificar si el producto ya está en el carrito del usuario
        sql_check = "SELECT * FROM carrito_compras WHERE producto_id = %s AND users_id = %s"
        cursor.execute(sql_check, (producto_id, users_id))
        item_existente = cursor.fetchone()
        
        if item_existente:
            # Actualizar la cantidad si el producto ya está en el carrito
            nueva_cantidad = item_existente['cantidad'] + cantidad
            sql_update = "UPDATE carrito_compras SET cantidad = %s WHERE id = %s"
            cursor.execute(sql_update, (nueva_cantidad, item_existente['id']))
            conexion.commit()
            resultado = {'status': 'success', 'mensaje': 'Cantidad actualizada en el carrito'}
        else:
            # Insertar nuevo producto en el carrito
            fecha_actual = date.today()
            sql_insert = "INSERT INTO carrito_compras (cantidad, fecha_creacion, producto_id, users_id) VALUES (%s, %s, %s, %s)"
            cursor.execute(sql_insert, (cantidad, fecha_actual, producto_id, users_id))
            conexion.commit()
            resultado = {'status': 'success', 'mensaje': 'Producto agregado al carrito'}
            
        return resultado
    except Exception as e:
        return {'status': 'error', 'mensaje': f'Error al agregar al carrito: {str(e)}'}
    finally:
        if conexion.is_connected():
            cursor.close()
            conexion.close()

def obtener_carrito(users_id):
    """
    Obtiene todos los productos en el carrito de un usuario con información detallada
    """
    try:
        conexion = connectionBD()
        cursor = conexion.cursor(dictionary=True)
        
        # Consulta JOIN para obtener información detallada de los productos en el carrito
        sql = """
        SELECT cc.id, cc.cantidad, cc.fecha_creacion, p.id as producto_id, p.nombre, p.precio, p.imagen 
        FROM carrito_compras cc
        JOIN producto p ON cc.producto_id = p.id
        WHERE cc.users_id = %s
        """
        cursor.execute(sql, (users_id,))
        items_carrito = cursor.fetchall()
        
        # Calcular total del carrito
        total = sum(item['precio'] * item['cantidad'] for item in items_carrito)
        
        return {'status': 'success', 'items': items_carrito, 'total': total}
    except Exception as e:
        return {'status': 'error', 'mensaje': f'Error al obtener carrito: {str(e)}'}
    finally:
        if conexion.is_connected():
            cursor.close()
            conexion.close()

def actualizar_cantidad_carrito(carrito_id, cantidad, users_id):
    """
    Actualiza la cantidad de un producto en el carrito
    """
    try:
        conexion = connectionBD()
        cursor = conexion.cursor()
        
        # Verificar que el item del carrito pertenezca al usuario
        sql_check = "SELECT * FROM carrito_compras WHERE id = %s AND users_id = %s"
        cursor.execute(sql_check, (carrito_id, users_id))
        if cursor.fetchone() is None:
            return {'status': 'error', 'mensaje': 'El producto no pertenece a este usuario'}
        
        if cantidad <= 0:
            # Si la cantidad es 0 o negativa, eliminar el producto del carrito
            sql_delete = "DELETE FROM carrito_compras WHERE id = %s"
            cursor.execute(sql_delete, (carrito_id,))
            mensaje = 'Producto eliminado del carrito'
        else:
            # Actualizar la cantidad
            sql_update = "UPDATE carrito_compras SET cantidad = %s WHERE id = %s"
            cursor.execute(sql_update, (cantidad, carrito_id))
            mensaje = 'Cantidad actualizada'
            
        conexion.commit()
        return {'status': 'success', 'mensaje': mensaje}
    except Exception as e:
        return {'status': 'error', 'mensaje': f'Error al actualizar cantidad: {str(e)}'}
    finally:
        if conexion.is_connected():
            cursor.close()
            conexion.close()

def vaciar_carrito(users_id):
    """
    Elimina todos los productos del carrito de un usuario
    """
    try:
        conexion = connectionBD()
        cursor = conexion.cursor()
        
        sql = "DELETE FROM carrito_compras WHERE users_id = %s"
        cursor.execute(sql, (users_id,))
        conexion.commit()
        
        return {'status': 'success', 'mensaje': 'Carrito vaciado con éxito'}
    except Exception as e:
        return {'status': 'error', 'mensaje': f'Error al vaciar el carrito: {str(e)}'}
    finally:
        if conexion.is_connected():
            cursor.close()
            conexion.close()

def eliminar_del_carrito(carrito_id, users_id):
    try:
        conexion = connectionBD()
        cursor = conexion.cursor()
        
        # Verificar que el item del carrito pertenezca al usuario
        sql_check = "SELECT * FROM carrito_compras WHERE id = %s AND users_id = %s"
        cursor.execute(sql_check, (carrito_id, users_id))
        item = cursor.fetchone()
        
        if item is None:
            print(f"El producto con ID {carrito_id} no pertenece al usuario {users_id}")
            return {'status': 'error', 'mensaje': 'El producto no pertenece a este usuario'}
        
        # Eliminar el producto del carrito
        sql_delete = "DELETE FROM carrito_compras WHERE id = %s"
        cursor.execute(sql_delete, (carrito_id,))
        conexion.commit()
        
        print(f"Producto con ID {carrito_id} eliminado del carrito del usuario {users_id}")
        return {'status': 'success', 'mensaje': 'Producto eliminado del carrito'}
    except Exception as e:
        print(f"Error al eliminar del carrito: {str(e)}")
        return {'status': 'error', 'mensaje': f'Error al eliminar del carrito: {str(e)}'}
    finally:
        if conexion.is_connected():
            cursor.close()
            conexion.close()

def obtener_direcciones_usuario(users_id):
    try:
        conexion = connectionBD()
        cursor = conexion.cursor(dictionary=True)
        
        # Modificar la consulta para incluir nombres de municipio y departamento
        sql = """
        SELECT d.*, m.nombre AS nombre_municipio, dep.nombre AS nombre_departamento 
        FROM direccion d
        LEFT JOIN municipio m ON d.municipio_id = m.id
        LEFT JOIN departamento dep ON d.departamento_id = dep.id
        WHERE d.users_id = %s
        """
        print(f"Ejecutando consulta con JOIN: {sql} con users_id={users_id}")
        cursor.execute(sql, (users_id,))
        direcciones = cursor.fetchall()
        print(f"Direcciones completas obtenidas de la BD: {direcciones}")
        
        return direcciones
    except Exception as e:
        print(f"Error al obtener direcciones: {e}")
        return []
    finally:
        if conexion.is_connected():
            cursor.close()
            conexion.close()

def crear_entrega_automatica(tipo_entrega, users_id, direccion_id=None):
    """
    Crea una entrega automáticamente asignando todos los valores requeridos
    """
    try:
        with connectionBD() as conexion:
            with conexion.cursor() as cursor:
                # Validar dirección si es domicilio
                if tipo_entrega == 'Domicilio' and direccion_id:
                    cursor.execute("SELECT users_id FROM direccion WHERE id = %s", (direccion_id,))
                    if cursor.fetchone()[0] != users_id:
                        raise ValueError("La dirección no pertenece al usuario")

                # Insertar entrega con todos los campos requeridos
                sql = """
                INSERT INTO entrega (
                    tipo, estado, costo_domicilio, direccion_id, users_id, fecha_hora
                ) VALUES (%s, %s, %s, %s, %s, NOW())
                """
                valores = (
                    tipo_entrega,
                    'Pendiente',
                    0,  # Valor por defecto
                    direccion_id if tipo_entrega == 'Domicilio' else None,
                    users_id
                )
                cursor.execute(sql, valores)
                entrega_id = cursor.lastrowid
                conexion.commit()
                return entrega_id
                
    except Exception as e:
        print(f"Error en crear_entrega_automatica: {str(e)}")
        raise
