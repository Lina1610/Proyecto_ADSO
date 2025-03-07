from app import app
from flask import render_template, request, flash, redirect, url_for, session,  jsonify
from mysql.connector.errors import Error


from mysql.connector import Error
from conexion.conexionBD import connectionBD
# Importando cenexión a BD
from controllers.funciones_order import *

PATH_URL = "public/pedido"
from app import app
from flask import render_template, request, flash, redirect, url_for, session
from mysql.connector import Error
from conexion.conexionBD import connectionBD
from controllers.funciones_order import *




# Ruta para el formulario de registro de pedidos
@app.route('/registrar-pedido', methods=['GET', 'POST'])
def viewFormPedido():
    if 'conectado' in session:
        if request.method == 'POST':
            data_form = request.form
            resultado = procesar_pedido(data_form)

            if isinstance(resultado, int) and resultado > 0:
                flash('Pedido registrado con éxito', 'success')
                return redirect(url_for('viewFormPedido'))
            else:
                flash(f'Error al registrar pedido: {resultado}', 'error')
                return redirect(url_for('viewFormPedido'))

        with connectionBD() as conexion_MySQLdb:
            with conexion_MySQLdb.cursor(dictionary=True) as cursor:
                # Obtener usuarios
                cursor.execute("SELECT id, nombre FROM users")
                usuarios = cursor.fetchall()

                # Obtener productos
                cursor.execute("SELECT id, nombre FROM producto")
                productos = cursor.fetchall()

                # Obtener métodos de pago
                metodos_pago = obtener_metodos_pago(conexion_MySQLdb)

                # Obtener tipos de entrega
                tipos_entrega = obtener_tipos_entrega(conexion_MySQLdb)
                print("Tipos de entrega obtenidos:", tipos_entrega)  # Depuración

        return render_template(
            'public/pedido/registro_pedido.html',  # Asegúrate de que la ruta sea correcta
            usuarios=usuarios,
            productos=productos,
            metodos_pago=metodos_pago,
            tipos_entrega=tipos_entrega  # Pasar los tipos de entrega a la plantilla
        )
    else:
        flash('Primero debes iniciar sesión.', 'error')
        return redirect(url_for('inicio'))
    

from controllers.funciones_order import obtener_pedidos

@app.route('/lista-de-pedidos')
def lista_pedidos():
    if 'conectado' in session:
        pedidos = obtener_pedidos()  # Asegúrate de que esta función devuelva el campo 'total'
        print("Pedidos enviados a la plantilla:", pedidos)  # Depuración
        return render_template('public/pedido/lista_pedidos.html', pedidos=pedidos)
    else:
        flash('Primero debes iniciar sesión.', 'error')
        return redirect(url_for('inicio'))

# Ruta para buscar pedidos
@app.route("/buscando-pedido", methods=['POST'])
def viewBuscarPedidoBD():
    try:
        search_query = request.json.get('busqueda')
        if not search_query:
            return jsonify({'error': 'No search query provided'}), 400

        resultadoBusqueda = buscarPedidoBD(search_query)

        if resultadoBusqueda:
            html_resultados = ""
            for pedido in resultadoBusqueda:
                html_resultados += f"""
                <tr id="pedido_{pedido['id']}">
                    <td>{pedido['id']}</td>
                    <td>{pedido['fecha']}</td>
                    <td>{pedido['fechaEntrega']}</td>
                    <td>{pedido['horaEntrega']}</td>
                    <td>{pedido['estado']}</td>
                    <td>{pedido['usuario_nombre']}</td>
                    <td>{pedido['producto_nombre']}</td>
                    <td>{pedido['metodo_pago']}</td>
                    <td>{pedido['tipo_entrega']}</td>
                    <td width="10px">
                        <a href="#" class="btn btn-info btn-sm" title="Ver detalles">
                            <i class="bi bi-eye"></i> Ver detalles
                        </a>
                        <a href="#" class="btn btn-success btn-sm" title="Actualizar">
                            <i class="bi bi-arrow-clockwise"></i> Actualizar
                        </a>
                        <a href="#" onclick="eliminarPedido('{pedido['id']}');" class="btn btn-danger btn-sm" title="Eliminar">
                            <i class="bi bi-trash3"></i> Eliminar
                        </a>
                    </td>
                </tr>
                """
            return jsonify({'success': True, 'html': html_resultados})
        else:
            mensaje_html = f"""
            <tr>
                <td colspan="10" style="text-align:center;color: red;font-weight: bold;">
                    No resultados para la búsqueda: <strong style="color: #222;">{search_query}</strong>
                </td>
            </tr>
            """
            return jsonify({'success': False, 'html': mensaje_html})
    except Exception as e:
        print(f"Error en viewBuscarPedidoBD: {e}")
        return jsonify({'error': str(e)}), 500


# Ruta para eliminar un pedido
@app.route('/eliminar-pedido/<int:id>', methods=['DELETE'])
def eliminar_pedido_route(id):
    if 'conectado' in session:
        resultado = eliminar_pedido(id)
        if resultado and resultado > 0:
            return {'success': True, 'message': 'Pedido eliminado correctamente'}
        return {'success': False, 'message': 'Error al eliminar pedido'}
    return {'success': False, 'message': 'Usuario no autenticado'}, 401



@app.route('/editar-pedido/<int:id>', methods=['GET', 'POST'])
def viewEditarPedido(id):
    if 'conectado' in session:
        if request.method == 'GET':
            # Obtener los datos del pedido por su ID
            with connectionBD() as conexion_MySQLdb:
                # Usar un cursor con buffered=True
                with conexion_MySQLdb.cursor(dictionary=True, buffered=True) as cursor:
                    cursor.execute("""
                        SELECT p.id, p.fecha, p.fechaEntrega, p.horaEntrega, p.estado,
                               p.users_id, p.producto_id, p.metodo_pago_id, p.entrega_id,
                               u.nombre AS usuario_nombre, pr.nombre AS producto_nombre,
                               mp.metodo AS metodo_pago, e.tipo AS tipo_entrega
                        FROM pedido p
                        JOIN users u ON p.users_id = u.id
                        JOIN producto pr ON p.producto_id = pr.id
                        JOIN metodo_pago mp ON p.metodo_pago_id = mp.id
                        JOIN entrega e ON p.entrega_id = e.id
                        WHERE p.id = %s
                    """, (id,))
                    pedido = cursor.fetchone()  # Consumir el resultado

                    if not pedido:
                        flash('Pedido no encontrado', 'error')
                        return redirect(url_for('lista_pedidos'))

                    # Obtener usuarios, productos, métodos de pago y tipos de entrega
                    cursor.execute("SELECT id, nombre FROM users")
                    usuarios = cursor.fetchall()  # Consumir todos los resultados

                    cursor.execute("SELECT id, nombre FROM producto")
                    productos = cursor.fetchall()  # Consumir todos los resultados

                    metodos_pago = obtener_metodos_pago(conexion_MySQLdb)
                    tipos_entrega = obtener_tipos_entrega(conexion_MySQLdb)

            return render_template(
                'public/pedido/editar_pedido.html',
                pedido=pedido,
                usuarios=usuarios,
                productos=productos,
                metodos_pago=metodos_pago,
                tipos_entrega=tipos_entrega
            )

        elif request.method == 'POST':
            # Procesar la actualización del pedido
            data_form = request.form
            resultado = actualizar_pedido(id, data_form)

            if resultado is True:
                flash('Pedido actualizado correctamente', 'success')
            else:
                flash(f'Error al actualizar el pedido: {resultado}', 'error')

            return redirect(url_for('lista_pedidos'))
    else:
        flash('Primero debes iniciar sesión.', 'error')
        return redirect(url_for('inicio'))
    
@app.route('/detalles-pedido/<int:id>')
def detalles_pedido(id):
    if 'conectado' in session:
        with connectionBD() as conexion_MySQLdb:
            with conexion_MySQLdb.cursor(dictionary=True) as cursor:
                # Obtener información del pedido
                cursor.execute("""
                    SELECT p.id, p.fecha, p.fechaEntrega, p.horaEntrega, p.estado,
                           u.nombre AS usuario_nombre, pr.nombre AS producto_nombre,
                           mp.metodo AS metodo_pago, e.tipo AS tipo_entrega,
                           (SELECT SUM(dp.total) FROM detalle_pedido dp WHERE dp.pedido_id = p.id) AS total_pedido
                    FROM pedido p
                    JOIN users u ON p.users_id = u.id
                    JOIN producto pr ON p.producto_id = pr.id
                    JOIN metodo_pago mp ON p.metodo_pago_id = mp.id
                    JOIN entrega e ON p.entrega_id = e.id
                    WHERE p.id = %s
                """, (id,))
                pedido = cursor.fetchone()

                # Asegurarse de que total_pedido no sea None
                if pedido['total_pedido'] is None:
                    pedido['total_pedido'] = 0.0

                # Obtener los detalles del pedido
                cursor.execute("""
                    SELECT dp.id, dp.precio_unitario, dp.total, dp.cantidad,
                           pr.nombre AS producto_nombre
                    FROM detalle_pedido dp
                    JOIN producto pr ON dp.producto_id = pr.id
                    WHERE dp.pedido_id = %s
                """, (id,))
                detalles_pedido = cursor.fetchall()

        return render_template('public/pedido/detalles_pedido.html', 
                             pedido=pedido, 
                             detalles_pedido=detalles_pedido)
    else:
        flash('Primero debes iniciar sesión.', 'error')
        return redirect(url_for('inicio'))