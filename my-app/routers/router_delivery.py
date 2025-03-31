from app import app
from flask import render_template, request, flash,jsonify, redirect, url_for, session
from mysql.connector.errors import Error
from controllers.funciones_delivery import *
from conexion.conexionBD import connectionBD
from migrations.migraciones import MigradorEntregas

PATH_URL = "public/entrega"

@app.route('/registrar-entrega', methods=['GET', 'POST'])
def viewFormEntrega():
    if 'conectado' not in session:
        if request.method == 'POST':
            return jsonify({"status": "error", "mensaje": "Primero debes iniciar sesión."}), 401
        flash('Primero debes iniciar sesión.', 'error')
        return redirect(url_for('inicio'))

    if request.method == 'POST':
        try:
            data_form = request.form
            users_id = session.get('users_id')
            
            if not users_id:
                return jsonify({"status": "error", "mensaje": "No se pudo identificar al usuario."}), 400

            # Validar campos obligatorios
            campos_requeridos = ['tipo']
            error = validar_campos_obligatorios(data_form, campos_requeridos)
            if error:
                return jsonify({"status": "error", "mensaje": error}), 400

            # Validar tipo de entrega
            error = validar_tipo(data_form['tipo'])
            if error:
                return jsonify({"status": "error", "mensaje": error}), 400

            # Validación específica para domicilio
            if data_form['tipo'] == 'Domicilio' and not data_form.get('direccion_id'):
                return jsonify({"status": "error", "mensaje": "Debes seleccionar una dirección para entrega a domicilio"}), 400

            # Procesar la entrega - Siempre pasar users_id
            resultado = procesar_entrega(
                tipo_entrega=data_form['tipo'],
                direccion_id=data_form.get('direccion_id'),
                users_id=users_id  # Esto es clave, pasar siempre el users_id
            )

            if isinstance(resultado, int) and resultado > 0:
                # Obtener la entrega recién creada para mostrarla
                nueva_entrega = buscar_entrega_por_id(resultado)
                return jsonify({
                    "status": "success",
                    "mensaje": "Entrega registrada con éxito",
                    "entrega": nueva_entrega
                })
            else:
                return jsonify({"status": "error", "mensaje": f"Error al registrar entrega: {resultado}"}), 500

        except Exception as e:
            return jsonify({"status": "error", "mensaje": f"Error inesperado: {str(e)}"}), 500

    # Para GET, renderizar el formulario
    return render_template('public/entrega/form_entrega.html')

@app.route('/actualizar-entregas-sin-usuario')
def actualizar_entregas_sin_usuario():
    if 'conectado' not in session or session.get('rol') != 'admin':
        flash('Acceso restringido a administradores', 'error')
        return redirect(url_for('inicio'))
    
    try:
        with connectionBD() as conexion_MySQLdb:
            with conexion_MySQLdb.cursor() as cursor:
                # Actualizar entregas presenciales sin users_id
                cursor.execute("""
                    UPDATE entrega e 
                    JOIN pedido p ON e.id = p.entrega_id 
                    SET e.users_id = p.users_id 
                    WHERE e.tipo = 'Presencial' AND e.users_id IS NULL
                """)
                presenciales_actualizadas = cursor.rowcount
                
                # Actualizar entregas a domicilio sin users_id
                cursor.execute("""
                    UPDATE entrega e 
                    JOIN direccion d ON e.direccion_id = d.id 
                    SET e.users_id = d.users_id 
                    WHERE e.tipo = 'Domicilio' AND e.users_id IS NULL
                """)
                domicilio_actualizadas = cursor.rowcount
                
                conexion_MySQLdb.commit()
                
                flash(f'Actualización exitosa: {presenciales_actualizadas} entregas presenciales y {domicilio_actualizadas} entregas a domicilio actualizadas.', 'success')
        
        return redirect(url_for('lista_entregas'))
    except Exception as e:
        flash(f'Error al actualizar entregas: {str(e)}', 'error')
        return redirect(url_for('lista_entregas'))



@app.route('/guardar-pedido', methods=['POST'])
def guardar_pedido():
    if 'conectado' not in session:
        return jsonify({"status": "error", "mensaje": "Debes iniciar sesión"}), 401

    try:
        data = request.get_json()
        users_id = session['users_id']
        
        # Validaciones básicas
        required_fields = ['metodo_pago_id', 'tipo_entrega', 'total']
        for field in required_fields:
            if field not in data:
                return jsonify({"status": "error", "mensaje": f"Falta el campo {field}"}), 400

        # Crear entrega primero (asegurando users_id)
        entrega_id = procesar_entrega(
            tipo_entrega=data['tipo_entrega'],
            direccion_id=data.get('direccion_id'),
            users_id=users_id  # Pasar siempre el users_id
        )

        # Resto del código para crear el pedido...
        pedido_id = crear_pedido(
            users_id=users_id,
            metodo_pago_id=data['metodo_pago_id'],
            entrega_id=entrega_id,
            total=data['total']
        )

        return jsonify({
            "status": "success",
            "mensaje": "Pedido creado correctamente",
            "pedido_id": pedido_id,
            "entrega_id": entrega_id
        })

    except Exception as e:
        return jsonify({"status": "error", "mensaje": str(e)}), 500

    
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
    if 'conectado' not in session:
        flash('Primero debes iniciar sesión.', 'error')
        return redirect(url_for('inicio'))

    if request.method == 'GET':
        entrega = buscar_entrega_por_id(id)
        if not isinstance(entrega, dict):
            flash(entrega, 'error')
            return redirect(url_for('lista_entregas'))
        
        return render_template('public/entrega/editar_entrega.html', entrega=entrega)

    elif request.method == 'POST':
        # Obtener la entrega actual primero
        entrega_actual = buscar_entrega_por_id(id)
        if not entrega_actual:
            flash('La entrega no existe', 'error')
            return redirect(url_for('lista_entregas'))

        # Procesar el formulario manteniendo los valores existentes
        data_form = {
            'tipo': request.form.get('tipo'),
            'estado': request.form.get('estado'),
            'costo_domicilio': request.form.get('costo_domicilio', entrega_actual.get('costo_domicilio')),
            'direccion_id': entrega_actual.get('direccion_id')  # Mantener el valor actual
        }

        # Actualizar la entrega
        resultado = actualizar_entrega(id, data_form)
        if isinstance(resultado, int) and resultado > 0:
            flash('Entrega actualizada correctamente.', 'success')
        else:
            flash(resultado if resultado else 'Error al actualizar', 'error')

        return redirect(url_for('lista_entregas'))

@app.route('/eliminar-entrega/<int:id>', methods=['GET'])
def eliminar_entrega_route(id):
    if 'conectado' in session:  # Verifica si el usuario está autenticado
        resultado = eliminar_entrega(id)  # Llama a la función para eliminar la entrega
        print(f"Resultado de eliminar_entrega: {resultado}, tipo: {type(resultado)}")  # Depuración

        if resultado == True:  # Comprobación explícita
            flash('Entrega eliminada correctamente.', 'success')
        else:
            flash('Error al eliminar la entrega', 'error')

        # Redireccionar a la lista de entregas
        return redirect(url_for('lista_entregas'))  # Ajusta 'lista_entregas' a tu ruta correcta
    else:
        flash('Usuario no autenticado', 'error')
        return redirect(url_for('inicio'))  # Redirigir al inicio si no está autenticado

from flask import render_template_string


@app.route("/buscando-entrega", methods=['POST'])
def viewBuscarEntregaBD():
    try:
        search_query = request.json.get('busqueda', '').strip()
        entregas = buscar_entregaBD(search_query) if search_query else obtener_entregas()

        if entregas:
            html_resultados = render_template_string("""
                {% for entrega in entregas %}
                <tr id="entrega_{{ entrega.id }}">
                    <td>{{ loop.index }}</td>
                    <td>{{ entrega.tipo }}</td>
                    <td>{{ entrega.estado }}</td>
                    <td>
                        {% if entrega.costo_domicilio %}
                            ${{ "{:,.0f}".format(entrega.costo_domicilio) }}
                        {% else %}
                            N/A
                        {% endif %}
                    </td>
                    <td>{{ entrega.nombre_usuario or 'N/A' }}</td>
                    <td>
                        {% if entrega.direccion_completa %}
                            {{ entrega.direccion_completa }}
                        {% else %}
                            Establecimiento físico
                        {% endif %}
                    </td>
                    <td>
                        {% if entrega.municipio %}
                            {{ entrega.municipio }}, {{ entrega.departamento }}
                        {% else %}
                            N/A
                        {% endif %}
                    </td>
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
            return jsonify({'success': False, 'html': '<tr><td colspan="8" class="text-center">No se encontraron resultados</td></tr>'})
    except Exception as e:
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

@app.route('/debug-entregas')
def debug_entregas():
    if 'conectado' not in session:
        return "No conectado"
    
    with connectionBD() as conexion_MySQLdb:
        with conexion_MySQLdb.cursor(dictionary=True) as cursor:
            # Ver entregas recientes
            cursor.execute("SELECT id, tipo, users_id, direccion_id FROM entrega ORDER BY id DESC LIMIT 5")
            entregas = cursor.fetchall()
            
            # Ver usuarios
            cursor.execute("SELECT id, nombre FROM users WHERE id IN (SELECT DISTINCT users_id FROM entrega WHERE users_id IS NOT NULL)")
            usuarios = cursor.fetchall()
            
            return render_template_string("""
                <h2>Últimas 5 entregas</h2>
                <pre>{{ entregas|tojson(indent=2) }}</pre>
                <h2>Usuarios en entregas</h2>
                <pre>{{ usuarios|tojson(indent=2) }}</pre>
            """, entregas=entregas, usuarios=usuarios)

@app.route('/crear-entrega', methods=['POST'])
def crear_entrega():
    users_id = session.get('users_id')
    
    # Depuración de sesión
    print(f"Sesión actual - users_id: {users_id}")
    
    if not users_id:
        flash('Debes iniciar sesión para crear una entrega', 'error')
        return redirect(url_for('inicio'))
    
    tipo_entrega = request.form.get('tipo_entrega')
    direccion_id = request.form.get('direccion_id') if tipo_entrega == 'Domicilio' else None
    
    # Validaciones
    if not tipo_entrega:
        flash('Debe seleccionar un tipo de entrega', 'error')
        return redirect(url_for('lista_entregas'))
    
    entrega_id = procesar_entrega(
        tipo_entrega=tipo_entrega, 
        direccion_id=direccion_id, 
        users_id=users_id
    )
    
    if isinstance(entrega_id, int):
        flash('Entrega creada correctamente', 'success')
    else:
        flash(f'Error al crear entrega: {entrega_id}', 'error')
    
    return redirect(url_for('lista_entregas'))

@app.route('/admin/migrar-entregas')
def migrar_entregas():
    if 'conectado' not in session or session.get('rol') != 'superadmin':
        flash('Acceso restringido a administradores', 'error')
        return redirect(url_for('inicio'))

    try:
        registros = MigradorEntregas.migrar_users_id()
        if registros is None:
            flash('Error en la migración', 'error')
        elif registros == 0:
            flash('No hay registros pendientes de migración', 'info')
        else:
            flash(f'Migración exitosa: {registros} registros actualizados', 'success')
    except Exception as e:
        flash(f'Error: {str(e)}', 'error')
    
    return redirect(url_for('lista_entregas'))

@app.route('/mis-entregas')
def mis_entregas():
    if 'conectado' not in session:
        flash('Primero debes iniciar sesión.', 'error')
        return redirect(url_for('inicio'))
    
    user_id = session['users_id']
    entregas = obtener_entregas_cliente(user_id)
    
    return render_template('public/cliente/mis_entregas.html', entregas=entregas)