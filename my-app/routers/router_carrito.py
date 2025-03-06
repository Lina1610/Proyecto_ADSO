from flask import Blueprint, request, jsonify, session, render_template, redirect, url_for
from controllers.funciones_carrito import obtener_direcciones_usuario, agregar_al_carrito, obtener_carrito, actualizar_cantidad_carrito, vaciar_carrito, eliminar_del_carrito
from conexion.conexionBD import connectionBD
carrito_bp = Blueprint('carrito', __name__)

@carrito_bp.route('/agregar', methods=['POST'])
def agregar_producto_carrito():
    """Ruta para agregar un producto al carrito"""
    if 'conectado' not in session or not session['conectado']:
        return jsonify({'status': 'error', 'mensaje': 'Debe iniciar sesión para agregar productos al carrito'})
    
    datos = request.json
    producto_id = datos.get('producto_id')
    cantidad = datos.get('cantidad', 1)
    users_id = session.get('id')
    
    if not producto_id:
        return jsonify({'status': 'error', 'mensaje': 'ID de producto no proporcionado'})
    
    resultado = agregar_al_carrito(producto_id, cantidad, users_id)
    return jsonify(resultado)

@carrito_bp.route('/obtener', methods=['GET'])
def obtener_carrito_usuario():
    """Ruta para obtener el carrito del usuario actual"""
    if 'conectado' not in session or not session['conectado']:
        return jsonify({'status': 'error', 'mensaje': 'Debe iniciar sesión para ver el carrito'})
    
    users_id = session.get('id')
    resultado = obtener_carrito(users_id)
    return jsonify(resultado)

@carrito_bp.route('/actualizar', methods=['POST'])
def actualizar_carrito():
    """Ruta para actualizar la cantidad de un producto en el carrito"""
    if 'conectado' not in session or not session['conectado']:
        return jsonify({'status': 'error', 'mensaje': 'Debe iniciar sesión para actualizar el carrito'})
    
    datos = request.json
    carrito_id = datos.get('carrito_id')
    cantidad = datos.get('cantidad')
    users_id = session.get('id')
    
    if not carrito_id or cantidad is None:
        return jsonify({'status': 'error', 'mensaje': 'Datos incompletos'})
    
    resultado = actualizar_cantidad_carrito(carrito_id, cantidad, users_id)
    return jsonify(resultado)

@carrito_bp.route('/vaciar', methods=['POST'])
def vaciar_carrito_usuario():
    """Ruta para vaciar el carrito del usuario"""
    if 'conectado' not in session or not session['conectado']:
        return jsonify({'status': 'error', 'mensaje': 'Debe iniciar sesión para vaciar el carrito'})
    
    users_id = session.get('id')
    resultado = vaciar_carrito(users_id)
    return jsonify(resultado)

@carrito_bp.route('/finalizar-compra', methods=['POST'])
def finalizar_compra():
    if 'conectado' not in session:
        return jsonify({'status': 'error', 'mensaje': 'Debe iniciar sesión para finalizar la compra'})
    
    users_id = session.get('id')
    datos = request.json
    direccion_id = datos.get('direccion_id')
    
    if not direccion_id:
        return jsonify({'status': 'error', 'mensaje': 'Debes seleccionar una dirección de envío'})
    
    # Obtener los productos del carrito
    carrito = obtener_carrito(users_id)
    if carrito['status'] != 'success':
        return jsonify({'status': 'error', 'mensaje': 'Error al obtener el carrito'})
    
    # Crear el pedido en la base de datos
    try:
        conexion = connectionBD()
        cursor = conexion.cursor()
        
        # Insertar el pedido en la tabla "pedidos"
        sql_pedido = """
            INSERT INTO pedidos (users_id, direccion_id, estado, fecha_creacion)
            VALUES (%s, %s, 'pendiente', NOW())
        """
        cursor.execute(sql_pedido, (users_id, direccion_id))
        pedido_id = cursor.lastrowid  # Obtener el ID del pedido recién creado
        
        # Insertar los productos del carrito en la tabla "detalles_pedido"
        for item in carrito['items']:
            sql_detalle = """
                INSERT INTO detalles_pedido (pedido_id, producto_id, cantidad, precio_unitario)
                VALUES (%s, %s, %s, %s)
            """
            cursor.execute(sql_detalle, (pedido_id, item['producto_id'], item['cantidad'], item['precio']))
        
        # Vaciar el carrito después de crear el pedido
        vaciar_carrito(users_id)
        
        conexion.commit()
        return jsonify({'status': 'success', 'mensaje': 'Pedido creado con éxito', 'pedido_id': pedido_id})
    except Exception as e:
        print(f"Error al finalizar la compra: {e}")
        return jsonify({'status': 'error', 'mensaje': 'Error al finalizar la compra'})
    finally:
        if conexion.is_connected():
            cursor.close()
            conexion.close()

@carrito_bp.route('/eliminar', methods=['POST'])
def eliminar_producto_carrito():
    """Ruta para eliminar un producto del carrito"""
    if 'conectado' not in session or not session['conectado']:
        return jsonify({'status': 'error', 'mensaje': 'Debe iniciar sesión para eliminar productos del carrito'})
    
    datos = request.json
    carrito_id = datos.get('carrito_id')
    users_id = session.get('id')
    
    if not carrito_id:
        return jsonify({'status': 'error', 'mensaje': 'ID de carrito no proporcionado'})
    
    # Llamar a la función para eliminar el producto del carrito
    resultado = eliminar_del_carrito(carrito_id, users_id)
    return jsonify(resultado)

@carrito_bp.route('/obtener-direcciones', methods=['GET'])
def obtener_direcciones():
    """Ruta para obtener las direcciones del usuario actual"""
    if 'conectado' not in session or not session['conectado']:
        return jsonify({'status': 'error', 'mensaje': 'Debe iniciar sesión para ver sus direcciones'})
    
    users_id = session.get('id')
    direcciones = obtener_direcciones_usuario(users_id)
    return jsonify({'status': 'success', 'direcciones': direcciones})