from flask import Blueprint, render_template, request, flash, redirect, url_for, session, jsonify
from conexion.conexionBD import connectionBD
from controllers.funciones_installment import procesar_abono

from controllers.funciones_installment import obtener_abonos
from controllers.funciones_installment import actualizar_abono
from controllers.funciones_installment import buscarAbonoBD
from controllers.funciones_installment import eliminar_abono

from app import app



@app.route('/registrar-abono', methods=['GET', 'POST'])
def viewFormAbono():
    if 'conectado' in session:
        if request.method == 'POST':
            dataForm = {
                'numero_abonos': request.form.get('numero_abonos'),
                'estado': request.form.get('estado'),
                'monto': request.form.get('monto'),
                'pedido_id': request.form.get('pedido_id')
            }

            resultado = procesar_abono(dataForm)

            if isinstance(resultado, int) and resultado > 0:
                flash('Abono registrado correctamente.', 'success')
            else:
                flash(resultado, 'error')

            return redirect(url_for('viewFormAbono'))

        with connectionBD() as conexion_MySQLdb:
            with conexion_MySQLdb.cursor(dictionary=True) as cursor:
                cursor.execute("""
                    SELECT p.id AS pedido_id, u.nombre AS nombre_usuario
                    FROM pedido p
                    JOIN users u ON p.users_id = u.id
                """)
                pedidos = cursor.fetchall()

        return render_template('public/abono/registro_abono.html', pedidos=pedidos)
    else:
        flash('Primero debes iniciar sesión.', 'error')
        return redirect(url_for('inicio'))
    
@app.route('/lista-de-abonos')
def lista_abonos():
    if 'conectado' in session:
        abonos = obtener_abonos()  # Función para obtener los abonos desde la base de datos
        print("Abonos pasados al template:", abonos)  # Depuración
        return render_template('public/abono/lista_abonos.html', abonos=abonos)
    else:
        flash('Primero debes iniciar sesión.', 'error')
        return redirect(url_for('inicio'))
    
@app.route('/detalles-abono/<int:id>')
def detalles_abono(id):
    if 'conectado' in session:
        with connectionBD() as conexion_MySQLdb:
            with conexion_MySQLdb.cursor(dictionary=True) as cursor:
                # Consulta SQL para obtener detalles del abono y el pedido asociado
                sql = """
                    SELECT 
                        abono.id AS abono_id,
                        abono.numero_abonos,
                        abono.estado AS estado_abono,
                        abono.monto,
                        abono.pedido_id,
                        pedido.id AS pedido_id,
                        pedido.fecha AS fecha_pedido,
                        pedido.fechaEntrega,
                        pedido.horaEntrega,
                        pedido.estado AS estado_pedido,
                        pedido.total,
                        users.nombre AS nombre_usuario
                    FROM 
                        abono
                    JOIN 
                        pedido ON abono.pedido_id = pedido.id
                    JOIN 
                        users ON pedido.users_id = users.id
                    WHERE 
                        abono.id = %s;
                """
                cursor.execute(sql, (id,))
                abono_pedido = cursor.fetchone()

        if abono_pedido:
            return render_template('public/abono/detalles_abono.html', abono_pedido=abono_pedido)
        else:
            flash('Abono no encontrado', 'error')
            return redirect(url_for('lista_abonos'))
    else:
        flash('Primero debes iniciar sesión.', 'error')
        return redirect(url_for('inicio'))
    
@app.route('/editar-abono/<int:id>', methods=['GET', 'POST'])
def viewEditarAbono(id):
    if 'conectado' in session:
        if request.method == 'GET':
            with connectionBD() as conexion_MySQLdb:
                with conexion_MySQLdb.cursor(dictionary=True) as cursor:
                    cursor.execute("SELECT * FROM abono WHERE id = %s", (id,))
                    abono = cursor.fetchone()

                    if not abono:
                        flash('Abono no encontrado', 'error')
                        return redirect(url_for('lista_abonos'))

            return render_template('public/abono/editar_abono.html', abono=abono)

        elif request.method == 'POST':
            data_form = request.form
            resultado = actualizar_abono(id, data_form)

            if resultado is True:
                flash('Abono actualizado correctamente', 'success')
            else:
                flash(f'Error al actualizar el abono: {resultado}', 'error')

            return redirect(url_for('lista_abonos'))
    else:
        flash('Primero debes iniciar sesión.', 'error')
        return redirect(url_for('inicio'))
    

@app.route("/buscando-abono", methods=['POST'])
def viewBuscarAbonoBD():
    try:
        search_query = request.json.get('busqueda')  # Obtener el término de búsqueda desde el JSON
        if not search_query:
            return jsonify({'error': 'No search query provided'}), 400

        resultadoBusqueda = buscarAbonoBD(search_query)  # Buscar abonos en la base de datos

        if resultadoBusqueda:
            # Si hay resultados, generar el HTML de la tabla
            html_resultados = ""
            for abono in resultadoBusqueda:
                html_resultados += f"""
                <tr id="abono_{abono['id']}">
                    <td>{abono['id']}</td>
                    <td>{abono['numero_abonos']}</td>
                    <td>{abono['estado']}</td>
                    <td>$ {abono['monto']}</td>
                    <td>{abono['pedido_id']}</td>
                    <td>{abono['fecha_pedido']}</td>
                    <td>{abono['nombre_usuario']}</td>
                    <td width="10px">
                        <a href="/detalles-abono/{abono['id']}" class="btn btn-info btn-sm" title="Ver detalles">
                            <i class="bi bi-eye"></i> Ver detalles
                        </a>
                        <a href="/editar-abono/{abono['id']}" class="btn btn-success btn-sm" title="Actualizar">
                            <i class="bi bi-arrow-clockwise"></i> Actualizar
                        </a>
                        <a href="#" onclick="eliminarAbono('{abono['id']}');" class="btn btn-danger btn-sm" title="Eliminar">
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
                <td colspan="7" style="text-align:center;color: red;font-weight: bold;">
                    No resultados para la búsqueda: <strong style="color: #222;">{search_query}</strong>
                </td>
            </tr>
            """
            return jsonify({'success': False, 'html': mensaje_html})

    except Exception as e:
        print(f"Error en viewBuscarAbonoBD: {e}")  # Log de depuración
        return jsonify({'error': str(e)}), 500  # Manejo de errores
    
@app.route('/eliminar-abono/<int:id>', methods=['DELETE'])
def eliminar_abono_route(id):
    if 'conectado' in session:
        resultado = eliminar_abono(id)
        if resultado and resultado > 0:
            return jsonify({'success': True, 'message': 'Abono eliminado correctamente'})
        return jsonify({'success': False, 'message': 'Error al eliminar abono'})
    return jsonify({'success': False, 'message': 'Usuario no autenticado'}), 401
