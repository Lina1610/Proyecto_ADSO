from flask import Blueprint, request, jsonify, session, render_template
from controllers.funciones_carrito import agregar_al_carrito, obtener_carrito, actualizar_cantidad_carrito, vaciar_carrito

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
    """Ruta para finalizar la compra (aquí podrías crear un pedido y vaciar el carrito)"""
    if 'conectado' not in session or not session['conectado']:
        return jsonify({'status': 'error', 'mensaje': 'Debe iniciar sesión para finalizar la compra'})
    
    users_id = session.get('id')
    
    # Aquí podrías implementar la lógica para crear un pedido con los productos del carrito
    # ...
    
    # Vaciar el carrito después de crear el pedido
    resultado = vaciar_carrito(users_id)
    if resultado['status'] == 'success':
        return jsonify({'status': 'success', 'mensaje': 'Compra finalizada con éxito'})
    else:
        return jsonify({'status': 'error', 'mensaje': 'Error al finalizar la compra'})