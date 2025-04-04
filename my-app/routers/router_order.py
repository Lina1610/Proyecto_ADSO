from app import app
from flask import render_template, request, flash, redirect, url_for, session,  jsonify
from mysql.connector.errors import Error
from controllers.funciones_order import *
import datetime  # Importación corregida


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

@app.route('/obtener-metodos-pago-tipos-entrega', methods=['GET'])
def obtener_metodos_pago_tipos_entrega():
    
    if 'conectado' not in session:
        return jsonify({'status': 'error', 'mensaje': 'Debe iniciar sesión para procesar el pedido'})
    
    with connectionBD() as conexion_MySQLdb:
        metodos_pago = obtener_metodos_pago(conexion_MySQLdb)
        tipos_entrega = obtener_tipos_entrega(conexion_MySQLdb)
        
        return jsonify({
            'status': 'success',
            'metodos_pago': metodos_pago,
            'tipos_entrega': tipos_entrega
        })

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


@app.route('/eliminar-pedido/<int:id>', methods=['GET'])
def eliminar_pedido_route(id):
    if 'conectado' in session:
        resultado = eliminar_pedido(id)
        print(f"Resultado de eliminar_pedido: {resultado}, tipo: {type(resultado)}")  # Mejor depuración
        
        if resultado == True:  # Comprobación explícita
            flash('Pedido eliminado correctamente.', 'success')
        else:
            flash('Error al eliminar el pedido', 'error')
        
        # Redireccionar a la lista de pedidos
        return redirect(url_for('lista_pedidos'))  # Asegúrate de que 'lista_pedidos' es la ruta correcta
    else:
        flash('Usuario no autenticado', 'error')
        return redirect(url_for('inicio'))  # Redirigir al inicio si no está autenticado



@app.route('/editar-pedido/<int:id>', methods=['GET', 'POST'])
def viewEditarPedido(id):
    if 'conectado' not in session:
        flash('Primero debes iniciar sesión.', 'error')
        return redirect(url_for('inicio'))

    with connectionBD() as conexion_MySQLdb:
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
            pedido = cursor.fetchone()

            if not pedido:
                flash('Pedido no encontrado', 'error')
                return redirect(url_for('lista_pedidos'))

            # Formatear fechaEntrega y horaEntrega para el formulario
            if isinstance(pedido['fechaEntrega'], (datetime.date, datetime.datetime)):
                pedido['fechaEntrega'] = pedido['fechaEntrega'].strftime('%Y-%m-%d')
            if isinstance(pedido['horaEntrega'], (datetime.time, datetime.datetime)):
                pedido['horaEntrega'] = pedido['horaEntrega'].strftime('%H:%M')
            elif isinstance(pedido['horaEntrega'], str) and ':' in pedido['horaEntrega']:
                pedido['horaEntrega'] = pedido['horaEntrega'][:5]

            cursor.execute("SELECT id, nombre FROM users")
            usuarios = cursor.fetchall()
            cursor.execute("SELECT id, nombre FROM producto")
            productos = cursor.fetchall()
            metodos_pago = obtener_metodos_pago(conexion_MySQLdb)
            tipos_entrega = obtener_tipos_entrega(conexion_MySQLdb)

    if request.method == 'POST':
        data_form = request.form
        print("Datos recibidos del formulario:", dict(data_form))
        resultado = actualizar_pedido(id, data_form)

        if resultado is True:
            flash('Pedido actualizado correctamente', 'success')
            return redirect(url_for('lista_pedidos'))
        else:
            flash(f'Error: {resultado}', 'error')
            return render_template(
                'public/pedido/editar_pedido.html',
                pedido=pedido,
                usuarios=usuarios,
                productos=productos,
                metodos_pago=metodos_pago,
                tipos_entrega=tipos_entrega,
                form_data=data_form
            )

    return render_template(
        'public/pedido/editar_pedido.html',
        pedido=pedido,
        usuarios=usuarios,
        productos=productos,
        metodos_pago=metodos_pago,
        tipos_entrega=tipos_entrega
    )

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
    
