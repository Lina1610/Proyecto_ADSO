from app import app
from flask import render_template, request, flash,jsonify, redirect, url_for, session
from mysql.connector.errors import Error
from controllers.funciones_delivery import *
from conexion.conexionBD import connectionBD

PATH_URL = "public/entrega"

@app.route('/registrar-entrega', methods=['GET', 'POST'])
def viewFormEntrega():
    if 'conectado' not in session:  # Si el usuario no está conectado
        flash('Primero debes iniciar sesión.', 'error')
        return redirect(url_for('inicio'))  # Redirige a la página de inicio

    if request.method == 'POST':  # Si es un POST, procesamos el formulario
        try:
            data_form = request.form  # Captura los datos del formulario
            resultado = procesar_entrega(data_form)  # Procesa los datos de la entrega

            if isinstance(resultado, int) and resultado > 0:  # Si el registro fue exitoso
                flash('Entrega registrada con éxito', 'success')
            else:  # Si hubo un error en el registro
                flash(f'Error al registrar entrega: {resultado}', 'error')
        except Exception as e:  # Captura cualquier excepción durante el procesamiento
            flash(f'Error inesperado: {str(e)}', 'error')

        return redirect(url_for('viewFormEntrega'))  # Redirige al formulario vacío

    # Si es un GET, solo mostramos el formulario
    try:
        with connectionBD() as conexion_MySQLdb:
            with conexion_MySQLdb.cursor(dictionary=True) as cursor:
                # Obtener las direcciones del usuario
                cursor.execute("""
                    SELECT ac
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
                direcciones = cursor.fetchall()  # Obtiene todas las direcciones activas
    except Error as e:  # Captura errores de la base de datos
        flash(f'Error al cargar direcciones: {str(e)}', 'error')
        direcciones = []  # Si hay un error, devuelve una lista vacía

    return render_template(
        f'{PATH_URL}/registro_entrega.html',
        direcciones=direcciones
    )

@app.route('/guardar-pedido', methods=['POST'])
def guardar_pedido():
    if 'conectado' not in session:  # Si el usuario no está conectado
        return jsonify({"status": "error", "mensaje": "Debes iniciar sesión para realizar esta acción."})

    try:
        data = request.get_json()  # Obtener los datos del pedido
        metodo_pago_id = data.get('metodo_pago_id')
        tipo_entrega = data.get('tipo_entrega')
        direccion_id = data.get('direccion_id')
        users_id = session.get('users_id')  # Obtener el ID del usuario desde la sesión
        total = data.get('total')  # Total del pedido

        # Validar los datos
        if not metodo_pago_id or not tipo_entrega or not users_id or not total:
            return jsonify({"status": "error", "mensaje": "Faltan datos obligatorios."})

        if tipo_entrega == 'Domicilio' and not direccion_id:
            return jsonify({"status": "error", "mensaje": "Debes seleccionar una dirección para entrega a domicilio."})

        # Crear la entrega
        entrega_id = procesar_entrega(tipo_entrega, direccion_id)
        if isinstance(entrega_id, str):  # Si hay un error
            return jsonify({"status": "error", "mensaje": entrega_id})

        # Crear el pedido
        pedido_id = crear_pedido(users_id, metodo_pago_id, entrega_id, total)
        if isinstance(pedido_id, str):  # Si hay un error
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
                    'Pendiente',  # Estado por defecto
                    total,
                    entrega_id,
                    users_id,
                    metodo_pago_id
                )
                cursor.execute(sql, valores)
                conexion_MySQLdb.commit()
                return cursor.lastrowid  # Devuelve el ID del pedido creado
    except Exception as e:
        return f"Error al crear el pedido: {str(e)}"
    
@app.route('/lista-de-entregas')
def lista_entregas():
    if 'conectado' in session:
        entregas = obtener_entregas()
        print("Datos enviados a la plantilla:", entregas)  # Depuración
        if isinstance(entregas, list):  # Asegúrate de que entregas sea una lista
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
    if 'conectado' in session:
        if request.method == 'GET':
            # Obtener la entrega por su ID
            entrega = buscar_entrega_por_id(id)
            if isinstance(entrega, dict):
                # No necesitas seleccionar direcciones si no existe la tabla `direccion`
                return render_template('public/entrega/editar_entrega.html', entrega=entrega)
            else:
                flash(entrega, 'error')
                return redirect(url_for('lista_entregas'))

        elif request.method == 'POST':
            # Procesar el formulario de edición
            data_form = {
                'tipo': request.form.get('tipo'),
                'estado': request.form.get('estado'),
                'costo_domicilio': request.form.get('costo_domicilio'),
                'direccion_id': request.form.get('direccion_id')
            }

            # Actualizar la entrega
            resultado = actualizar_entrega(id, data_form)
            if isinstance(resultado, int):
                flash('Entrega actualizada correctamente.', 'success')
            else:
                flash(resultado, 'error')

            return redirect(url_for('lista_entregas'))
    else:
        flash('Primero debes iniciar sesión.', 'error')
        return redirect(url_for('inicio'))

@app.route('/eliminar-entrega/<int:id>', methods=['DELETE'])
def eliminar_entrega_route(id):
    if 'conectado' in session:  # Verifica si el usuario está autenticado
        resultado = eliminar_entrega(id)  # Llama a la función para eliminar la entrega
        if resultado and resultado > 0:
            return jsonify({'success': True, 'message': 'Entrega eliminada correctamente'})
        return jsonify({'success': False, 'message': 'Error al eliminar entrega'})
    return jsonify({'success': False, 'message': 'Usuario no autenticado'}), 401

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