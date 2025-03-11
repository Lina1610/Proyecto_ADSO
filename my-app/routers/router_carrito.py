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
    tipo_entrega = datos.get('tipo_entrega')  # 'Domicilio' o 'Presencial'
    metodo_pago_id = datos.get('metodo_pago_id')  # ID del método de pago seleccionado
    
    # Validar que se hayan enviado los datos necesarios
    if not tipo_entrega or not metodo_pago_id:
        return jsonify({'status': 'error', 'mensaje': 'Faltan datos obligatorios (tipo de entrega o método de pago)'})
    
    if tipo_entrega == 'Domicilio' and not direccion_id:
        return jsonify({'status': 'error', 'mensaje': 'Debes seleccionar una dirección de envío para entrega a domicilio'})
    
    # Obtener los productos del carrito
    carrito = obtener_carrito(users_id)
    if carrito['status'] != 'success':
        return jsonify({'status': 'error', 'mensaje': 'Error al obtener el carrito'})
    
    # Calcular el total del carrito
    total = sum(item['precio'] * item['cantidad'] for item in carrito['items'])
    print(f"Total calculado: {total}")  # Depuración
    
    # Crear el pedido en la base de datos
    try:
        conexion = connectionBD()
        cursor = conexion.cursor()
        
        # Insertar la entrega en la tabla "entrega"
        sql_entrega = """
            INSERT INTO entrega (tipo, estado, costo_domicilio, direccion_id, fecha_hora)
            VALUES (%s, %s, %s, %s, NOW())
        """
        valores_entrega = (
            tipo_entrega,
            'Pendiente',  # Estado por defecto
            0,  # Siempre establecer costo_domicilio en 0
            direccion_id if tipo_entrega == 'Domicilio' else None
        )
        cursor.execute(sql_entrega, valores_entrega)
        entrega_id = cursor.lastrowid  # Obtener el ID de la entrega recién creada
        
        # Insertar el pedido en la tabla "pedido"
        sql_pedido = """
            INSERT INTO pedido (
                fecha, estado, total, entrega_id, users_id, metodo_pago_id, producto_id
            ) VALUES (NOW(), %s, %s, %s, %s, %s, %s)
        """
        valores_pedido = (
            'Pendiente',  # Estado por defecto
            total,  # Total del carrito
            entrega_id,
            users_id,
            metodo_pago_id,
            carrito['items'][0]['producto_id']  # Usar el ID del primer producto en el carrito
        )
        cursor.execute(sql_pedido, valores_pedido)
        pedido_id = cursor.lastrowid  # Obtener el ID del pedido recién creado
        
        # Insertar los productos del carrito en la tabla "detalle_pedido"
        for item in carrito['items']:
            total_item = item['precio'] * item['cantidad']  # Calcular el total para este producto
            sql_detalle = """
                INSERT INTO detalle_pedido (
                    pedido_id, producto_id, cantidad, precio_unitario, total
                ) VALUES (%s, %s, %s, %s, %s)
            """
            cursor.execute(sql_detalle, (
                pedido_id,
                item['producto_id'],
                item['cantidad'],
                item['precio'],
                total_item  # Total para este producto
            ))
        
        # Vaciar el carrito después de crear el pedido
        vaciar_carrito(users_id)
        
        conexion.commit()
        return jsonify({'status': 'success', 'mensaje': 'Pedido creado con éxito', 'pedido_id': pedido_id})
    except Exception as e:
        print(f"Error al finalizar la compra: {e}")
        return jsonify({'status': 'error', 'mensaje': str(e)})  # Mostrar el error específico
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
