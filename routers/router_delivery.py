from app import app
from flask import render_template, request, flash, jsonify, redirect, url_for, session
from mysql.connector.errors import Error
from controllers.funciones_delivery import *
from conexion.conexionBD import connectionBD

PATH_URL = "public/entrega"

@app.route('/registrar-entrega', methods=['GET', 'POST'])
def viewFormEntrega():
    if 'conectado' not in session:
        flash('Primero debes iniciar sesión.', 'error')
        return redirect(url_for('inicio'))

    direcciones = []
    try:
        with connectionBD() as conexion_MySQLdb:
            with conexion_MySQLdb.cursor(dictionary=True) as cursor:
                cursor.execute("""
                    SELECT 
                        d.id, 
                        d.nombre_completo, 
                        CONCAT_WS(', ', d.domicilio, d.barrio, d.referencias) AS direccion_completa,
                        m.nombre AS municipio,
                        dp.nombre AS departamento
                    FROM 
                        direccion d
                    JOIN 
                        municipio m ON d.municipio_id = m.id
                    JOIN 
                        departamento dp ON d.departamento_id = dp.id
                    WHERE 
                        d.estado = 'Activo'
                """)
                direcciones = cursor.fetchall()
    except Error as e:
        flash(f'Error al cargar direcciones: {str(e)}', 'error')

    if request.method == 'POST':
        data_form = request.form
        campos_requeridos = ['tipo', 'estado']
        
        # Validar campos obligatorios
        error = validar_campos_obligatorios(data_form, campos_requeridos)
        if error:
            flash(error, 'error')
            return render_template(f'{PATH_URL}/registro_entrega.html', data_form=data_form, direcciones=direcciones)

        tipo = data_form['tipo']
        estado = data_form['estado']
        costo_domicilio_str = data_form.get('costo_domicilio', '')
        direccion_id_str = data_form.get('direccion_id', '')

        # Validar tipo
        error = validar_tipo(tipo)
        if error:
            flash(error, 'error')
            return render_template(f'{PATH_URL}/registro_entrega.html', data_form=data_form, direcciones=direcciones)

        # Validar estado
        error = validar_estado(estado)
        if error:
            flash(error, 'error')
            return render_template(f'{PATH_URL}/registro_entrega.html', data_form=data_form, direcciones=direcciones)

        # Validar costo_domicilio
        costo_domicilio, error = validar_costo_domicilio(costo_domicilio_str)
        if error:
            flash(error, 'error')
            return render_template(f'{PATH_URL}/registro_entrega.html', data_form=data_form, direcciones=direcciones)

        # Validar direccion_id (ahora es opcional)
        direccion_id, error = validar_direccion_id(direccion_id_str, tipo)
        if error:
            flash(error, 'error')
            return render_template(f'{PATH_URL}/registro_entrega.html', data_form=data_form, direcciones=direcciones)

        # Verificar que la dirección exista si se proporcionó
        if direccion_id:
            error = verificar_direccion_existe(direccion_id)
            if error:
                flash(error, 'error')
                return render_template(f'{PATH_URL}/registro_entrega.html', data_form=data_form, direcciones=direcciones)

        # Si pasa todas las validaciones, procesar la entrega
        resultado = procesar_entrega(tipo, direccion_id)
        if isinstance(resultado, int) and resultado > 0:
            flash('Entrega registrada con éxito', 'success')
        else:
            flash(f'Error al registrar entrega: {resultado}', 'error')
        return redirect(url_for('viewFormEntrega'))

    return render_template(f'{PATH_URL}/registro_entrega.html', direcciones=direcciones)

@app.route('/guardar-pedido', methods=['POST'])
def guardar_pedido():
    if 'conectado' not in session:
        return jsonify({"status": "error", "mensaje": "Debes iniciar sesión para realizar esta acción."})

    try:
        data = request.get_json()
        metodo_pago_id = data.get('metodo_pago_id')
        tipo_entrega = data.get('tipo_entrega')
        direccion_id = data.get('direccion_id')
        users_id = session.get('users_id')
        total = data.get('total')

        # Validar datos obligatorios
        if not metodo_pago_id or not tipo_entrega or not users_id or not total:
            return jsonify({"status": "error", "mensaje": "Faltan datos obligatorios."})

        # Validar tipo_entrega
        error = validar_tipo(tipo_entrega)
        if error:
            return jsonify({"status": "error", "mensaje": error})

        # Validar direccion_id (ahora es opcional)
        direccion_id, error = validar_direccion_id(direccion_id, tipo_entrega)
        if error:
            return jsonify({"status": "error", "mensaje": error})

        # Verificar que la dirección exista si se proporcionó
        if direccion_id:
            error = verificar_direccion_existe(direccion_id)
            if error:
                return jsonify({"status": "error", "mensaje": error})

        # Crear la entrega
        entrega_id = procesar_entrega(tipo_entrega, direccion_id)
        if isinstance(entrega_id, str):
            return jsonify({"status": "error", "mensaje": entrega_id})

        # Crear el pedido
        pedido_id = crear_pedido(users_id, metodo_pago_id, entrega_id, total)
        if isinstance(pedido_id, str):
            return jsonify({"status": "error", "mensaje": pedido_id})

        return jsonify({"status": "success", "mensaje": "Pedido registrado con éxito.", "pedido_id": pedido_id})

    except Exception as e:
        return jsonify({"status": "error", "mensaje": f"Error al registrar el pedido: {str(e)}"})

def crear_pedido(users_id, metodo_pago_id, entrega_id, total):
    """Crea un registro en la tabla 'pedido'."""
    try:
        with connectionBD() as conexion_MySQLdb:
            with conexion_MySQLdb.cursor(dictionary=True) as cursor:
                sql = """
                    INSERT INTO pedido (
                        fecha, estado, total, entrega_id, users_id, metodo_pago_id
                    ) VALUES (NOW(), %s, %s, %s, %s, %s)
                """
                valores = (
                    'Pendiente',
                    total,
                    entrega_id,
                    users_id,
                    metodo_pago_id
                )
                cursor.execute(sql, valores)
                conexion_MySQLdb.commit()
                return cursor.lastrowid
    except Exception as e:
        return f"Error al crear el pedido: {str(e)}"

@app.route('/lista-de-entregas')
def lista_entregas():
    if 'conectado' in session:
        entregas = obtener_entregas()
        print("Datos enviados a la plantilla:", entregas)
        if isinstance(entregas, list):
            return render_template('public/entrega/lista_entregas.html', entregas=entregas)
        else:
            flash("Error al obtener las entregas.", 'error')
            return redirect(url_for('inicio'))
    else:
        flash('Primero debes iniciar sesión.', 'error')
        return redirect(url_for('inicio'))

@app.route('/detalles-entrega/<int:id>')
def detalles_entrega(id):
    if 'conectado' in session:
        entrega = buscar_entrega_por_id(id)
        if isinstance(entrega, dict):
            return render_template('public/entrega/detalles_entrega.html', entrega=entrega)
        else:
            flash(entrega, 'error')
            return redirect(url_for('lista_entregas'))
    else:
        flash('Primero debes iniciar sesión.', 'error')
        return redirect(url_for('inicio'))

@app.route('/editar-entrega/<int:id>', methods=['GET', 'POST'])
def viewEditarEntrega(id):
    if 'conectado' not in session:
        flash('Primero debes iniciar sesión.', 'error')
        return redirect(url_for('inicio'))

    entrega = buscar_entrega_por_id(id)
    if not isinstance(entrega, dict):
        flash('No se encontró la entrega', 'error')
        return redirect(url_for('lista_entregas'))

    if request.method == 'POST':
        data_form = request.form
        tipo_entrega = data_form.get('tipo')
        
        # Validar campos obligatorios
        campos_requeridos = ['tipo', 'estado']
        error = validar_campos_obligatorios(data_form, campos_requeridos)
        if error:
            flash(error, 'error')
            return render_template('public/entrega/editar_entrega.html',
                                entrega=entrega,
                                entrega_id=id)

        # Validar tipo y estado
        error = validar_tipo(tipo_entrega)
        if error:
            flash(error, 'error')
            return render_template('public/entrega/editar_entrega.html',
                                entrega=entrega,
                                entrega_id=id)

        error = validar_estado(data_form.get('estado'))
        if error:
            flash(error, 'error')
            return render_template('public/entrega/editar_entrega.html',
                                entrega=entrega,
                                entrega_id=id)

        # Validar costo domicilio
        costo_domicilio, error = validar_costo_domicilio(data_form.get('costo_domicilio', ''))
        if error:
            flash(error, 'error')
            return render_template('public/entrega/editar_entrega.html',
                                entrega=entrega,
                                entrega_id=id)

        # Validar dirección SOLO para domicilio
        direccion_id = None
        if tipo_entrega == 'Domicilio':
            direccion_id, error = validar_direccion_id(
                data_form.get('direccion_id', ''),
                tipo_entrega
            )
            if error:
                flash(error, 'error')
                return render_template('public/entrega/editar_entrega.html',
                                    entrega=entrega,
                                    entrega_id=id)

        # Preparar datos para actualización
        datos_actualizacion = {
            'tipo': tipo_entrega,
            'estado': data_form.get('estado'),
            'costo_domicilio': costo_domicilio,
            'direccion_id': direccion_id if tipo_entrega == 'Domicilio' else None
        }

        # Actualizar la entrega
        resultado = actualizar_entrega(id, datos_actualizacion)
        if isinstance(resultado, int) and resultado > 0:
            flash('Entrega actualizada correctamente.', 'success')
            return redirect(url_for('lista_entregas'))
        else:
            flash('Error al actualizar la entrega', 'error')
    
    # GET request - Mostrar formulario
    return render_template('public/entrega/editar_entrega.html',
                         entrega=entrega,
                         entrega_id=id)

@app.route('/eliminar-entrega/<int:id>', methods=['GET'])
def eliminar_entrega_route(id):
    if 'conectado' in session:
        resultado = eliminar_entrega(id)
        print(f"Resultado de eliminar_entrega: {resultado}, tipo: {type(resultado)}")
        if resultado == True:
            flash('Entrega eliminada correctamente.', 'success')
        else:
            flash('Error al eliminar la entrega', 'error')
        return redirect(url_for('lista_entregas'))
    else:
        flash('Usuario no autenticado', 'error')
        return redirect(url_for('inicio'))

from flask import render_template_string

@app.route("/buscando-entrega", methods=['POST'])
def viewBuscarEntregaBD():
    try:
        search_query = request.json.get('busqueda', '').strip()
        print("Término de búsqueda recibido:", search_query)

        if not search_query:
            entregas = obtener_entregas()
        else:
            entregas = buscar_entregaBD(search_query)

        if entregas:
            html_resultados = render_template_string("""
                {% for entrega in entregas %}
                <tr id="entrega_{{ entrega.id }}">
                    <td>{{ loop.index }}</td>
                    <td>{{ entrega.tipo }}</td>
                    <td>{{ entrega.estado }}</td>
                    <td>{{ entrega.costo_domicilio }}</td>
                    <td>{{ entrega.direccion_completa }}</td>
                    <td>{{ entrega.nombre_usuario }}</td>
                    <td width="10px">
                        <a href="/detalles-entrega/{{ entrega.id }}" class="btn btn-info btn-sm" title="Ver detalles">
                            <i class="bi bi-eye"></i> Ver detalles
                        </a>
                        <a href="/editar-entrega/{{ entrega.id }}" class="btn btn-success btn-sm" title="Actualizar">
                            <i class="bi bi-arrow-clockwise"></i> Actualizar
                        </a>
                        <a href="#" onclick="eliminarEntrega('{{ entrega.id }}');" class="btn btn-danger btn-sm" title="Eliminar">
                            <i class="bi bi-trash3"></i> Eliminar
                        </a>
                    </td>
                </tr>
                {% endfor %}
            """, entregas=entregas)
            return jsonify({'success': True, 'html': html_resultados})
        else:
            mensaje_html = f"""
            <tr>
                <td colspan="7" style="text-align:center;color: red;font-weight: bold;">
                    No resultados para la búsqueda: <strong style="color: #222;">{search_query}</strong>
                </td>
            </tr>
            """
            return jsonify({'success': False, 'html': mensaje_html})

    except Exception as e:
        print(f"Error en viewBuscarEntregaBD: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/obtener-pedidos-cliente')
def obtener_pedidos_cliente():
    if 'conectado' in session:
        user_id = session['users_id']
        try:
            with connectionBD() as conexion_MySQLdb:
                with conexion_MySQLdb.cursor(dictionary=True) as cursor:
                    querySQL = """
                        SELECT p.id, p.fecha, p.fechaEntrega, p.horaEntrega, p.estado,
                               pr.nombre AS producto_nombre, mp.metodo AS metodo_pago,
                               e.tipo AS tipo_entrega, p.total
                        FROM pedido p
                        JOIN producto pr ON p.producto_id = pr.id
                        JOIN metodo_pago mp ON p.metodo_pago_id = mp.id
                        JOIN entrega e ON p.entrega_id = e.id
                        WHERE p.users_id = %s
                        ORDER BY p.id DESC
                    """
                    cursor.execute(querySQL, (user_id,))
                    pedidos = cursor.fetchall()
                    return jsonify(pedidos)
        except Exception as e:
            print(f"Error en obtener_pedidos_cliente: {e}")
            return jsonify([])
    else:
        return jsonify({"error": "Usuario no autenticado"}), 401
