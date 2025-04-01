
from app import app
from flask import render_template, request, flash, redirect, url_for, session, jsonify
from mysql.connector.errors import Error
from conexion.conexionBD import connectionBD
from controllers.funciones_invoice import obtener_facturas, procesar_factura, actualizar_factura

PATH_URL = "public/factura"

# Función para buscar facturas en la base de datos
def buscarFacturaBD(search_query):
    try:
        with connectionBD() as conexion_MySQLdb:
            with conexion_MySQLdb.cursor(dictionary=True) as cursor:
                querySQL = """
                    SELECT f.id, f.estado, f.fecha, f.pedido_id
                    FROM factura f
                    JOIN pedido p ON f.pedido_id = p.id
                    JOIN users u ON p.users_id = u.id
                    WHERE f.id LIKE %s OR f.estado LIKE %s OR f.fecha LIKE %s OR f.pedido_id LIKE %s
                """
                search_pattern = f"%{search_query}%"
                cursor.execute(querySQL, (search_pattern, search_pattern, search_pattern, search_pattern))
                return cursor.fetchall()
    except Exception as e:
        print(f"Error en buscarFacturaBD: {e}")
        return None

# Función para eliminar una factura de la base de datos
def eliminar_factura(id):
    try:
        with connectionBD() as conexion_MySQLdb:
            with conexion_MySQLdb.cursor() as cursor:
                querySQL = "DELETE FROM factura WHERE id = %s"
                cursor.execute(querySQL, (id,))
                conexion_MySQLdb.commit()
                return cursor.rowcount  # Retorna el número de filas afectadas
    except Exception as e:
        print(f"Error en eliminar_factura: {e}")
        return None

# Ruta para registrar una factura
@app.route('/registrar-factura', methods=['GET', 'POST'])
def viewFormFactura():
    if 'conectado' not in session:
        flash('Primero debes iniciar sesión.', 'error')
        return redirect(url_for('inicio'))

    if request.method == 'POST':
        try:
            # Obtener los datos del formulario
            dataForm = {
                'estado': request.form.get('estado'),
                'pedido_id': request.form.get('pedido_id')
            }

            # Validar campos obligatorios
            if not dataForm['pedido_id']:
                flash('El ID del pedido es obligatorio', 'error')
                return redirect(url_for('viewFormFactura'))

            # Procesar la factura
            resultado = procesar_factura(dataForm)

            # Manejar el resultado
            if isinstance(resultado, int) and resultado > 0:
                flash('Factura registrada correctamente.', 'success')
                return redirect(url_for('lista_facturas'))  # Redirigir a lista de facturas
            else:
                flash(f'Error al registrar factura: {resultado}', 'error')
                return redirect(url_for('viewFormFactura'))
                
        except Exception as e:
            flash(f'Error inesperado: {str(e)}', 'error')
            return redirect(url_for('viewFormFactura'))

    # Si es GET, mostrar el formulario con los datos necesarios
    with connectionBD() as conexion_MySQLdb:
        with conexion_MySQLdb.cursor(dictionary=True) as cursor:
            # Obtener la lista de pedidos con el nombre del usuario asociado
            cursor.execute("""
                SELECT p.id AS pedido_id, u.nombre AS nombre_usuario, 
                       p.fecha, p.estado AS estado_pedido
                FROM pedido p
                JOIN users u ON p.users_id = u.id
                WHERE p.id NOT IN (SELECT pedido_id FROM factura)  # Solo pedidos sin factura
                ORDER BY p.fecha DESC
            """)
            pedidos = cursor.fetchall()

    return render_template(
        'public/factura/registro_factura.html',
        pedidos=pedidos
    )

# Ruta para la lista de facturas
@app.route('/lista-de-facturas')
def lista_facturas():
    if 'conectado' in session:
        facturas = obtener_facturas()
        return render_template('public/factura/lista_facturas.html', facturas=facturas)
    else:
        flash('Primero debes iniciar sesión.', 'error')
        return redirect(url_for('inicio'))

# Ruta para buscar facturas
@app.route("/buscando-factura", methods=['POST'])
def viewBuscarFacturaBD():
    try:
        search_query = request.json.get('busqueda')  # Obtener el término de búsqueda desde el JSON
        if not search_query:
            return jsonify({'error': 'No search query provided'}), 400

        resultadoBusqueda = buscarFacturaBD(search_query)  # Buscar facturas en la base de datos

        if resultadoBusqueda:
            # Si hay resultados, generar el HTML de la tabla
            html_resultados = ""
            for factura in resultadoBusqueda:
                html_resultados += f"""
                <tr id="factura_{factura['id']}">
                    <td>{factura['id']}</td>
                    <td>{factura['estado']}</td>
                    <td>{factura['fecha']}</td>
                    <td>{factura['pedido_id']}</td>
                    <td width="10px">
                        <a href="/detalles-factura/{factura['id']}" class="btn btn-info btn-sm" title="Ver detalles">
                            <i class="bi bi-eye"></i> Ver detalles
                        </a>
                        <a href="/editar-factura/{factura['id']}" class="btn btn-success btn-sm" title="Actualizar">
                            <i class="bi bi-arrow-clockwise"></i> Actualizar
                        </a>
                        <a href="#" onclick="eliminarFactura('{factura['id']}');" class="btn btn-danger btn-sm" title="Eliminar">
                            <i class="bi bi-trash3"></i> Eliminar
                        </a>
                    </td>
                </tr>
                """
            return jsonify({'success': True, 'html': html_resultados})
        else:
            # Si no hay resultados, devolver un mensaje en HTML
            mensaje_html = f"""
            <tr>
                <td colspan="5" style="text-align:center;color: red;font-weight: bold;">
                    No resultados para la búsqueda: <strong style="color: #222;">{search_query}</strong>
                </td>
            </tr>
            """
            return jsonify({'success': False, 'html': mensaje_html})

    except Exception as e:
        print(f"Error en viewBuscarFacturaBD: {e}")  # Log de depuración
        return jsonify({'error': str(e)}), 500  # Manejo de errores

# Ruta para eliminar una factura
@app.route('/eliminar-factura/<int:id>', methods=['GET'])
def eliminar_factura_route(id):
    if 'conectado' in session:  # Verifica si el usuario está autenticado
        resultado = eliminar_factura(id)  # Llama a la función para eliminar la factura
        print(f"Resultado de eliminar_factura: {resultado}, tipo: {type(resultado)}")  # Depuración

        if resultado == True:  # Comprobación explícita
            flash('Factura eliminada correctamente.', 'success')
        else:
            flash('Error al eliminar la factura', 'error')

        # Redireccionar a la lista de facturas
        return redirect(url_for('lista_facturas'))  # Ajusta 'lista_facturas' a tu ruta correcta
    else:
        flash('Usuario no autenticado', 'error')
        return redirect(url_for('inicio'))  # Redirigir al inicio si no está autenticado

@app.route('/detalles-factura/<int:id>')
def detalles_factura(id):
    if 'conectado' in session:
        with connectionBD() as conexion_MySQLdb:
            with conexion_MySQLdb.cursor(dictionary=True) as cursor:
                # Consulta SQL para obtener detalles de la factura y el pedido asociado
                sql = """
                    SELECT 
                        factura.id AS factura_id,
                        factura.estado AS estado_factura,
                        factura.fecha AS fecha_factura,
                        factura.pedido_id,
                        pedido.id AS pedido_id,
                        pedido.fecha AS fecha_pedido,
                        pedido.fechaEntrega,
                        pedido.horaEntrega,
                        pedido.estado AS estado_pedido,
                        pedido.total,
                        users.nombre AS nombre_usuario,
                        producto.nombre AS nombre_producto,
                        metodo_pago.metodo AS metodo_pago
                    FROM 
                        factura
                    JOIN 
                        pedido ON factura.pedido_id = pedido.id
                    JOIN 
                        users ON pedido.users_id = users.id
                    JOIN 
                        producto ON pedido.producto_id = producto.id
                    JOIN 
                        metodo_pago ON pedido.metodo_pago_id = metodo_pago.id
                    WHERE 
                        factura.id = %s;
                """
                cursor.execute(sql, (id,))
                factura_pedido = cursor.fetchone()

                # Depuración: Imprimir los datos obtenidos
                print("Datos de la factura y pedido:", factura_pedido)

        if factura_pedido:
            return render_template('public/factura/detalles_factura.html', factura_pedido=factura_pedido)
        else:
            flash('Factura no encontrada', 'error')
            return redirect(url_for('lista_facturas'))
    else:
        flash('Primero debes iniciar sesión.', 'error')
        return redirect(url_for('inicio'))

# Ruta para editar una factura
@app.route('/editar-factura/<int:id>', methods=['GET', 'POST'])
def viewEditarFactura(id):
    if 'conectado' in session:
        if request.method == 'GET':
            with connectionBD() as conexion_MySQLdb:
                with conexion_MySQLdb.cursor(dictionary=True) as cursor:
                    cursor.execute("SELECT * FROM factura WHERE id = %s", (id,))
                    factura = cursor.fetchone()

                    if not factura:
                        flash('Factura no encontrada', 'error')
                        return redirect(url_for('lista_facturas'))

            return render_template('public/factura/editar_factura.html', factura=factura)

        elif request.method == 'POST':
            data_form = request.form
            resultado = actualizar_factura(id, data_form)

            if resultado is True:
                flash('Factura actualizada correctamente', 'success')
            else:
                flash(f'Error al actualizar la factura: {resultado}', 'error')

            return redirect(url_for('lista_facturas'))
    else:
        flash('Primero debes iniciar sesión.', 'error')
        return redirect(url_for('inicio'))
