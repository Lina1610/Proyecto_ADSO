from flask import Blueprint, request, jsonify, session, render_template, redirect, url_for
from controllers.funciones_carrito import obtener_direcciones_usuario, crear_entrega_automatica ,agregar_al_carrito, obtener_carrito, actualizar_cantidad_carrito, vaciar_carrito, eliminar_del_carrito
from conexion.conexionBD import connectionBD
from datetime import datetime  # Añade esto al inicio
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
        return jsonify({'status': 'error', 'mensaje': 'Debe iniciar sesión'})
    
    users_id = session.get('id')
    datos = request.json
    
    try:
        # Validaciones mejoradas
        tipo_entrega = datos.get('tipo_entrega')
        metodo_pago_id = datos.get('metodo_pago_id')
        direccion_id = datos.get('direccion_id')
        
        if not all([tipo_entrega, metodo_pago_id]):
            return jsonify({'status': 'error', 'mensaje': 'Faltan datos obligatorios'})
        
        if tipo_entrega not in ['Domicilio', 'Presencial']:
            return jsonify({'status': 'error', 'mensaje': 'Tipo de entrega no válido'})
        
        if tipo_entrega == 'Domicilio' and not direccion_id:
            return jsonify({'status': 'error', 'mensaje': 'Dirección requerida para domicilio'})

        # Verificar dirección si es domicilio
        if tipo_entrega == 'Domicilio':
            with connectionBD() as conexion:
                with conexion.cursor() as cursor:
                    cursor.execute("SELECT users_id FROM direccion WHERE id = %s", (direccion_id,))
                    if cursor.fetchone()[0] != users_id:
                        return jsonify({'status': 'error', 'mensaje': 'Dirección no válida'})

        # Procesar carrito
        carrito = obtener_carrito(users_id)
        if not carrito.get('items'):
            return jsonify({'status': 'error', 'mensaje': 'Carrito vacío'})

        with connectionBD() as conexion:
            with conexion.cursor() as cursor:
                # 1. Crear entrega (con users_id)
                sql_entrega = """
                    INSERT INTO entrega (
                        tipo, estado, costo_domicilio, direccion_id, users_id, fecha_hora
                    ) VALUES (%s, %s, %s, %s, %s, NOW())
                """
                cursor.execute(sql_entrega, (
                    tipo_entrega,
                    'Pendiente',
                    0,  # Valor fijo para simplificar
                    direccion_id if tipo_entrega == 'Domicilio' else None,
                    users_id  # Aseguramos users_id
                ))
                entrega_id = cursor.lastrowid

                # 2. Crear pedido (con producto_id del primer item)
                total = sum(item['precio'] * item['cantidad'] for item in carrito['items'])
                producto_id = carrito['items'][0]['producto_id']
                
                sql_pedido = """
                    INSERT INTO pedido (
                        fecha, estado, total, entrega_id, users_id, metodo_pago_id, producto_id
                    ) VALUES (NOW(), %s, %s, %s, %s, %s, %s)
                """
                cursor.execute(sql_pedido, (
                    'Pendiente',
                    total,
                    entrega_id,
                    users_id,
                    metodo_pago_id,
                    producto_id
                ))
                pedido_id = cursor.lastrowid

                # 3. Detalles del pedido
                for item in carrito['items']:
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
                        item['precio'] * item['cantidad']
                    ))

                # 4. Vaciar carrito
                cursor.execute("DELETE FROM carrito_compras WHERE users_id = %s", (users_id,))
                
                conexion.commit()
                
                # Usamos datetime.now() para la fecha de respuesta
                return jsonify({
                    'status': 'success',
                    'mensaje': 'Pedido creado con éxito',
                    'pedido_id': pedido_id,
                    'total': total,
                    'fecha': datetime.now().strftime('%d/%m/%Y %H:%M')
                })

    except Exception as e:
        print(f"Error en finalizar_compra: {str(e)}")
        return jsonify({'status': 'error', 'mensaje': str(e)})

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
