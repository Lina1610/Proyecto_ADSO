from app import app
from flask import render_template, request, flash, redirect, url_for, session, jsonify
from conexion.conexionBD import connectionBD
from flask import Flask, session, jsonify
from controllers.funciones_address import obtener_direccion_por_id
from controllers.funciones_address import (
    obtener_direcciones_usuario,
    procesar_direccion,
    validar_claves_foraneas,
    obtener_direccion,
    buscar_direccionBD,
    actualizar_direccion
)
from controllers.funciones_login import info_perfil_session  # Importar la función necesaria

# Definición de la constante PATH_URL
PATH_URL = "public/direccion"


# Ruta para mostrar las direcciones del cliente
@app.route('/cliente-direcciones', methods=['GET'])
def cliente_direcciones():
    """
    Muestra las direcciones asociadas a un usuario conectado.
    Accesible para roles: cliente, administrador, superadmin, empleado.
    """
    if 'conectado' in session:
        # Permitir múltiples roles
        if session['rol'] in ['cliente', 'administrador', 'superadmin', 'empleado']:
            user_id = session.get('id')

            # Obtener las direcciones del usuario
            direcciones = obtener_direcciones_usuario(user_id)
            print("Direcciones obtenidas:", direcciones)

            # Obtener departamentos y municipios para el formulario
            with connectionBD() as conexion_MySQLdb:
                with conexion_MySQLdb.cursor(dictionary=True) as cursor:
                    cursor.execute("SELECT id, nombre FROM departamento")
                    departamentos = cursor.fetchall()

                    cursor.execute("SELECT id, nombre FROM municipio")
                    municipios = cursor.fetchall()

            # Renderizar la plantilla con los datos
            return render_template(
                'public/perfil/perfil_cliente.html',  # Asegúrate que este template sea adecuado para todos los roles
                info_perfil_session=info_perfil_session(),
                departamentos=departamentos,
                municipios=municipios,
                direcciones=direcciones
            )
        else:
            flash('Acceso denegado.', 'error')
            return redirect(url_for('inicio'))
    else:
        flash('Primero debes iniciar sesión.', 'error')
        return redirect(url_for('inicio'))


# Ruta para registrar una dirección (API JSON)
@app.route('/api/registrar-direccion', methods=['POST'])
def api_registrar_direccion():
    if 'conectado' not in session:
        return jsonify({"success": False, "error": "Debes iniciar sesión"}), 401
    
    try:
        # Para datos JSON
        if request.is_json:
            data = request.get_json()
        # Para datos de formulario tradicional
        else:
            data = request.form.to_dict()
        
        # Añadir el user_id de la sesión
        data['users_id'] = session.get('id')
        
        resultado = procesar_direccion(data)
        
        if isinstance(resultado, int) and resultado > 0:
            return jsonify({
                "success": True, 
                "message": "Dirección registrada con éxito",
                "direccion_id": resultado
            }), 200
        else:
            # Aquí devolvemos el mensaje de error como un string
            return jsonify({"success": False, "error": str(resultado)}), 400
            
    except Exception as e:
        print(f"Error al registrar dirección: {e}")
        return jsonify({"success": False, "error": "Error interno del servidor"}), 500

# Ruta para el aplicativo (Interfaz web)
@app.route('/registrar-direccion', methods=['GET', 'POST'])
def viewFormDireccion():
    """
    Muestra el formulario para registrar una nueva dirección y procesa su envío.
    Solo accesible si el usuario está conectado.
    """
    print("🔍 Sesión en viewFormDireccion:", session)  # 🛠 Depuración
    # Verificar si el usuario está conectado y tiene un ID válido
    if 'conectado' not in session or 'id' not in session:
        flash('Primero debes iniciar sesión.', 'error')
        return redirect(url_for('inicio'))
    
    # Obtener el rol del usuario
    rol_usuario = session.get('rol', '')
    print(f"🔍 Rol del usuario: {rol_usuario}")  # 🛠 Depuración
    
    # Obtener datos de departamento, municipios y usuarios
    with connectionBD() as conexion_MySQLdb:
        with conexion_MySQLdb.cursor(dictionary=True) as cursor:
            cursor.execute("SELECT id, nombre FROM departamento")
            departamentos = cursor.fetchall()
            cursor.execute("SELECT id, nombre FROM municipio")
            municipios = cursor.fetchall()
            cursor.execute("SELECT id, nombre FROM users")
            users = cursor.fetchall()
    
    if request.method == 'POST':
        print("🔍 Datos del formulario recibidos:", request.form)  # 🛠 Depuración
        # Procesar la dirección con las validaciones
        resultado = procesar_direccion(request.form)
        
        if isinstance(resultado, int) and resultado > 0:
            flash('Dirección registrada con éxito', 'success')
            print("🔍 Sesión DESPUÉS de registrar la dirección:", session)  # 🛠 Depuración
            # Redirigir según el rol del usuario
            if rol_usuario == 'cliente':
                return redirect(url_for('cliente_direcciones'))
            else:
                return redirect(url_for('lista_direcciones'))
        else:
            # En caso de error, renderizar el formulario nuevamente con los datos ingresados
            flash(f'Error al registrar dirección: {resultado}', 'error')
            return render_template(
                f'{PATH_URL}/registro_direccion.html',
                departamentos=departamentos,
                municipios=municipios,
                users=users,
                form_data=request.form  # Pasar los datos del formulario para repoblar los campos
            )
    
    # Si es GET, mostrar el formulario vacío
    return render_template(
        f'{PATH_URL}/registro_direccion.html',
        departamentos=departamentos,
        municipios=municipios,
        users=users,
        form_data={}  # Formulario vacío
    )


# Ruta para obtener departamentos
@app.route('/obtener-departamentos', methods=['GET'])
def obtener_departamentos():
    """
    Obtiene todos los departamentos disponibles.
    Retorna un JSON con los departamentos o un mensaje de error.
    """
    try:
        with connectionBD() as conexion_MySQLdb:
            with conexion_MySQLdb.cursor(dictionary=True) as cursor:
                cursor.execute("SELECT id, nombre FROM departamento")
                departamentos = cursor.fetchall()
                return jsonify(departamentos)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# Ruta para obtener municipios según departamento
@app.route('/obtener_municipios', methods=['GET'])
def obtener_municipios():
    """
    Obtiene los municipios asociados a un departamento específico.
    Retorna un JSON con los municipios o un mensaje de error.
    """
    departamento_id = request.args.get('departamento_id')
    if not departamento_id or not departamento_id.isdigit():
        return jsonify({"error": "ID de departamento inválido"}), 400
    
    try:
        with connectionBD() as conexion_MySQLdb:
            with conexion_MySQLdb.cursor(dictionary=True) as cursor:
                cursor.execute("SELECT id FROM departamento WHERE id = %s", (int(departamento_id),))
                if cursor.fetchone() is None:
                    return jsonify([])  # Devuelve lista vacía si no hay municipios
                
                cursor.execute("SELECT id, nombre FROM municipio WHERE departamento_id = %s", (int(departamento_id),))
                municipios = cursor.fetchall()
                return jsonify(municipios)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Ruta para listar direcciones
@app.route('/lista-de-direccion')
def lista_direcciones():
    """
    Muestra una lista de todas las direcciones registradas.
    Solo accesible si el usuario está conectado y tiene un rol de administrador.
    """
    print("🔍 Sesión en lista_direcciones:", session)  # 🛠 Depuración
    if 'conectado' in session:
        if session['rol'] in ['superadmin', 'administrador', 'empleado']:
            try:
                direcciones = obtener_direccion() or []  # Asegurar que no sea None
                print("Datos de direcciones obtenidos:", direcciones)  # Depuración
                return render_template('public/direccion/lista_direccion.html', direcciones=direcciones)
            except Exception as e:
                print(f"Error al obtener las direcciones: {e}")
                flash('Error al obtener las direcciones. Por favor, inténtalo de nuevo.', 'error')
                return redirect(url_for('inicio'))
        else:
            flash('Acceso denegado.', 'error')
            return redirect(url_for('inicio'))
    else:
        flash('Primero debes iniciar sesión.', 'error')
        return redirect(url_for('inicio'))


# Ruta para mostrar los detalles de una dirección
@app.route('/detalles-direccion/<int:id>')
def detalles_direccion(id):
    """
    Muestra los detalles de una dirección específica por su ID.
    Solo accesible si el usuario está conectado.
    """
    print(f"ID recibido en detalles_direccion: {id}")  # Depuración

    # Obtener la dirección por su ID
    direccion = obtener_direccion_por_id(id)

    # Si la dirección no existe, mostrar un mensaje de error
    if not direccion:
        print("No se encontró la dirección en la base de datos.")  # Depuración
        flash('No existe la dirección.', 'error')
        return redirect(url_for('lista_direcciones'))
    
    print(f"Datos de la dirección obtenidos: {direccion}")  # Depuración
    return render_template('public/direccion/detalles_direccion.html', direccion=direccion)


# Ruta para guardar una dirección (API JSON)
@app.route('/api/guardar-direccion', methods=['POST'])
def guardar_direccion():
    """
    Guarda una nueva dirección en la base de datos desde el modal del carrito.
    Retorna una respuesta JSON con el resultado.
    """
    if 'conectado' not in session:
        return jsonify({"success": False, "error": "Debes iniciar sesión"}), 401

    try:
        # Obtener los datos del formulario como JSON
        data = request.get_json()
        
        if not data:
            return jsonify({"success": False, "error": "Datos no proporcionados"}), 400

        # Validar campos obligatorios
        campos_requeridos = ['nombre_completo', 'barrio', 'domicilio', 'telefono', 'departamento_id', 'municipio_id']
        for campo in campos_requeridos:
            if campo not in data or not str(data[campo]).strip():
                return jsonify({"success": False, "error": f"El campo {campo} es obligatorio"}), 400

        # Añadir el user_id de la sesión
        data['users_id'] = session.get('id')

        # Procesar la dirección con las validaciones
        resultado = procesar_direccion(data)
        
        if isinstance(resultado, int) and resultado > 0:
            return jsonify({
                "success": True, 
                "message": "Dirección guardada correctamente",
                "direccion_id": resultado
            }), 201
        else:
            return jsonify({"success": False, "error": str(resultado)}), 400
            
    except Exception as e:
        print(f"Error al guardar la dirección: {e}")
        return jsonify({"success": False, "error": "Error interno del servidor"}), 500


# Ruta para mostrar el formulario de edición de una dirección
@app.route('/editar-direccion/<int:id>', methods=['GET'])
def viewEditarDireccion(id):
    """
    Muestra el formulario para editar una dirección específica por su ID.
    Solo accesible si el usuario está conectado.
    """
    if 'conectado' in session:
        # Obtener la dirección por su ID
        direccion = obtener_direccion_por_id(id)

        if direccion:
            # Obtener departamentos para el formulario
            with connectionBD() as conexion_MySQLdb:
                with conexion_MySQLdb.cursor(dictionary=True) as cursor:
                    cursor.execute("SELECT id, nombre FROM departamento")
                    departamentos = cursor.fetchall()

            return render_template(
                'public/direccion/editar_direccion.html',
                direccion=direccion,
                departamentos=departamentos
            )
        else:
            flash(' La dirección no existe.', 'error')
            return redirect(url_for('lista_direcciones'))
    else:
        flash('Primero debes iniciar sesión.', 'error')
        return redirect(url_for('inicio')) 


# Ruta para actualizar una dirección (sitio web)
@app.route('/actualizar-direccion', methods=['POST'])
def actualizarDireccion():
    """
    Actualiza una dirección existente en la base de datos.
    Solo accesible si el usuario está conectado.
    """
    if 'conectado' in session:
        if request.method == 'POST':
            # Obtener los datos del formulario
            data_form = request.form
            id_direccion = data_form.get('id')

            # Validar que la dirección exista
            direccion = obtener_direccion_por_id(id_direccion)
            if not direccion:
                flash('La dirección no existe.', 'error')
                return redirect(url_for('lista_direcciones'))

            # Actualizar la dirección usando la función con validaciones
            resultado = actualizar_direccion(id_direccion, data_form)
            if "correctamente" in resultado:
                flash('Dirección actualizada correctamente.', 'success')
                return redirect(url_for('lista_direcciones'))
            else:
                flash(f'Error al actualizar la dirección: {resultado}', 'error')
                return redirect(url_for('lista_direcciones'))
    else:
        flash('Primero debes iniciar sesión.', 'error')
        return redirect(url_for('inicio'))


# Ruta para actualizar una dirección (cliente, interfaz web)
@app.route('/actualizar-direccion-web', methods=['POST'])
def actualizar_direccion_web():
    """
    Actualiza una dirección existente a través de una solicitud JSON.
    Retorna una respuesta JSON con el resultado.
    """
    print(f"📌 Método recibido: {request.method}")  # 🔥 Esto te dirá si realmente está llegando un POST
    try:
        data = request.json
        print(f"📩 Datos recibidos: {data}")  # 🔥 Verifica que estás recibiendo datos
        direccion_id = data.get('id')

        if not direccion_id:
            return jsonify({'error': 'ID de dirección no proporcionado'}), 400

        # Actualizar la dirección con las validaciones
        resultado = actualizar_direccion(direccion_id, data)

        if "correctamente" in resultado:
            return jsonify({'mensaje': resultado}), 200
        else:
            return jsonify({'error': resultado}), 400
    except Exception as e:
        print(f"❌ Error en actualizar_direccion_web: {e}")
        return jsonify({'error': 'Error interno del servidor'}), 500


# Ruta para actualizar una dirección (API)
@app.route('/actualizar-direccion-api', methods=['POST'])
def actualizarDireccionAPI():
    """
    Actualiza una dirección existente a través de una API JSON.
    Retorna una respuesta JSON con el resultado.
    """
    if 'conectado' in session:
        if request.method == 'POST':
            data_json = request.get_json()
            id_direccion = data_json.get('id')

            direccion = obtener_direccion_por_id(id_direccion)
            if not direccion:
                return jsonify({"success": False, "error": "La dirección no existe."})

            # Actualizar la dirección con las validaciones
            resultado = actualizar_direccion(id_direccion, data_json)
            if "correctamente" in resultado:
                response = jsonify({"success": True, "message": "Felicitaciones, dirección actualizada correctamente 😁"})
                response.mimetype = "application/json; charset=utf-8"
                return response
            else:
                return jsonify({"success": False, "error": f"Error al actualizar la dirección: {resultado}"})
    else:
        return jsonify({"success": False, "error": "Primero debes iniciar sesión."})


# Ruta para obtener los datos de una dirección (cliente)
@app.route('/obtener-direccion/<int:id>', methods=['GET'])
def obtener_datos_direccion(id):
    """
    Obtiene los datos de una dirección específica por su ID.
    Retorna un JSON con los datos o un mensaje de error.
    """
    if 'conectado' in session:
        try:
            direccion = obtener_direccion_por_id(id)
            if direccion:
                return jsonify({"success": True, "direccion": direccion})
            else:
                return jsonify({"success": False, "error": "La dirección no existe."})
        except Exception as e:
            print(f"Error al obtener los datos de la dirección: {e}")
            return jsonify({"success": False, "error": f"Error al obtener los datos: {str(e)}"})
    else:
        return jsonify({"success": False, "error": "Primero debes iniciar sesión."})


# Ruta para activar una dirección
@app.route('/activar-direccion/<int:id>')
def activar_direccion(id):
    """
    Activa una dirección específica por su ID.
    Solo accesible si el usuario está conectado.
    """
    if 'conectado' in session:
        try:
            with connectionBD() as conexion_MySQLdb:
                with conexion_MySQLdb.cursor(dictionary=True) as cursor:
                    sql = "UPDATE direccion SET estado = 'Activo' WHERE id = %s"
                    cursor.execute(sql, (id,))
                    conexion_MySQLdb.commit()

            flash('Dirección activada correctamente.', 'success')
        except Exception as e:
            print(f"Error al activar la dirección: {e}")
            flash('Error al activar la dirección.', 'error')
    else:
        flash('Primero debes iniciar sesión.', 'error')
    return redirect(url_for('lista_direcciones'))


# Ruta para desactivar una dirección
@app.route('/desactivar-direccion/<int:id>')
def desactivar_direccion(id):
    """
    Desactiva una dirección específica por su ID.
    Solo accesible si el usuario está conectado.
    """
    if 'conectado' in session:
        try:
            with connectionBD() as conexion_MySQLdb:
                with conexion_MySQLdb.cursor(dictionary=True) as cursor:
                    sql = "UPDATE direccion SET estado = 'Inactivo' WHERE id = %s"
                    cursor.execute(sql, (id,))
                    conexion_MySQLdb.commit()

            flash('Dirección desactivada correctamente.', 'success')
        except Exception as e:
            print(f"Error al desactivar la dirección: {e}")
            flash('Error al desactivar la dirección.', 'error')
    else:
        flash('Primero debes iniciar sesión.', 'error')
    return redirect(url_for('lista_direcciones'))


# Ruta para eliminar una dirección (método GET)
@app.route('/eliminar-direccion/<int:id>', methods=['GET'])
def eliminar_direccion(id):
    """
    Elimina una dirección específica por su ID.
    Solo accesible si el usuario está conectado.
    """
    if 'conectado' in session:
        try:
            with connectionBD() as conexion_MySQLdb:
                with conexion_MySQLdb.cursor(dictionary=True) as cursor:
                    sql = "DELETE FROM direccion WHERE id = %s"
                    cursor.execute(sql, (id,))
                    conexion_MySQLdb.commit()

            flash('Dirección eliminada correctamente.', 'success')
        except Exception as e:
            print(f"Error al eliminar la dirección: {e}")
            flash('Error al eliminar la dirección.', 'error')
    else:
        flash('Primero debes iniciar sesión.', 'error')
    return redirect(url_for('lista_direcciones'))


# Ruta para eliminar una dirección (método DELETE)
@app.route('/eliminar-direccion/<int:id>', methods=['DELETE'])
def eliminar_direccion_route(id):
    """
    Elimina una dirección específica por su ID.
    Devuelve una respuesta JSON para manejarla en JavaScript.
    """
    if 'conectado' not in session:
        return jsonify({'success': False, 'error': 'Primero debes iniciar sesión.'}), 403

    try:
        with connectionBD() as conexion_MySQLdb:
            with conexion_MySQLdb.cursor(dictionary=True) as cursor:
                sql = "DELETE FROM direccion WHERE id = %s"
                cursor.execute(sql, (id,))
                conexion_MySQLdb.commit()

        return jsonify({'success': True, 'message': 'Dirección eliminada correctamente.'}), 200
    except Exception as e:
        print(f"Error al eliminar la dirección: {e}")
        return jsonify({'success': False, 'error': 'Error al eliminar la dirección.'}), 500


# Ruta para buscar direcciones
@app.route("/buscando-direccion", methods=['POST'])
def viewBuscarDireccionBD():
    """
    Busca direcciones en la base de datos según un término de búsqueda.
    Retorna un JSON con los resultados en formato HTML para una tabla.
    """
    try:
        search_query = request.json.get('busqueda')  # Obtener el término de búsqueda desde el JSON
        if not search_query:
            return jsonify({'error': 'No search query provided'}), 400

        resultadoBusqueda = buscar_direccionBD(search_query)  # Buscar direcciones en la base de datos

        if resultadoBusqueda:
            # Si hay resultados, generar el HTML de la tabla
            html_resultados = ""
            for direccion in resultadoBusqueda:
                html_resultados += f"""
                <tr id="direccion_{direccion['id']}">
                    <td>{direccion['id']}</td>
                    <td>{direccion['nombre_completo']}</td>
                    <td>{direccion['municipio_nombre']}</td>
                    <td>{direccion['departamento_nombre']}</td>
                    <td>{direccion['usuario_nombre']}</td>

                    <!-- Columna de Estado -->
                    <td>
                        <span class="badge bg-{'success' if direccion['estado'] == 'Activo' else 'danger'}">
                            {direccion['estado']}
                        </span>
                    </td>

                    <!-- Columna de Activación/Desactivación -->
                    <td>
                        {"<a href='/activar-direccion/" + str(direccion['id']) + "' class='btn btn-sm btn-success' title='Activar dirección'><i class='bi bi-check-circle'></i> Activar</a>" if direccion['estado'] == 'Inactivo' else "<a href='/desactivar-direccion/" + str(direccion['id']) + "' class='btn btn-sm btn-warning' title='Desactivar dirección'><i class='bi bi-x-circle'></i> Desactivar</a>"}
                    </td>

                    <!-- Columna de Acciones -->
                    <td>
                        <a href="/detalles-direccion/{direccion['id']}" class="btn btn-info btn-sm" title="Ver detalles">
                            <i class="bi bi-eye"></i> Detalles
                        </a>
                        <a href="/editar-direccion/{direccion['id']}" class="btn btn-success btn-sm" title="Actualizar">
                            <i class="bi bi-arrow-clockwise"></i> Actualizar
                        </a>
                        <a href="#" onclick="eliminarDireccion('{direccion['id']}');" class="btn btn-danger btn-sm" title="Eliminar">
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
                <td colspan="8" style="text-align:center;color: red;font-weight: bold;">
                    No resultados para la búsqueda: <strong style="color: #222;">{search_query}</strong>
                </td>
            </tr>
            """
            return jsonify({'success': False, 'html': mensaje_html})

    except Exception as e:
        print(f"Error en viewBuscarDireccionBD: {e}")  # Log de depuración
        return jsonify({'error': str(e)}), 500  # Manejo de errores