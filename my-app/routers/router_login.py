from app import app
from flask import render_template, request, flash, redirect, url_for, jsonify, session
from conexion.conexionBD import connectionBD
from werkzeug.security import check_password_hash
from datetime import datetime, timedelta

from controllers.funciones_login import *
from controllers.funciones_address import *
from controllers.funciones_order import *

PATH_URL_LOGIN = "public/login"

@app.route('/login', methods=['GET'])
def inicio():
    if 'conectado' in session:
        return render_template('public/base_cpanel.html', dataLogin=dataLoginSesion())
    else:
        return render_template(f'{PATH_URL_LOGIN}/base_login.html')

@app.route('/mi-perfil', methods=['GET'])
def perfil():
    if 'conectado' in session:
        user_id = session.get('id')
        rol = session.get('rol')

        # Obtener información del perfil
        info_perfil = info_perfil_session()

        # Obtener direcciones del usuario
        direcciones = obtener_direcciones_usuario(user_id)

        # Obtener pedidos del usuario
        pedidos = obtener_pedidos(user_id)

        # Siempre redirigir al perfil del sitio web (perfil.html)
        return render_template(
            'public/perfil/perfil.html',
            info_perfil_session=info_perfil,
            direcciones=direcciones,
            pedidos=pedidos
        )
    else:
        flash('Primero debes iniciar sesión.', 'error')
        return redirect(url_for('inicio'))
    
@app.route('/perfil-aplicativo', methods=['GET'])
def perfil_aplicativo():
    if 'conectado' in session:
        rol = session.get('rol')

        # Verificar que el rol sea válido para acceder al aplicativo
        if rol not in ['administrador', 'superadmin', 'empleado']:
            flash('Acceso denegado.', 'error')
            return redirect(url_for('inicio'))

        # Obtener información del perfil
        info_perfil = info_perfil_session()

        return render_template(
            'public/perfil/perfil_aplicativo.html',
            info_perfil_session=info_perfil
        )
    else:
        flash('Primero debes iniciar sesión.', 'error')
        return redirect(url_for('inicio'))

@app.route('/register-user', methods=['GET'])
def cpanelRegisterUser():
    if 'conectado' in session:
        return redirect(url_for('inicio'))
    else:
        return render_template(f'{PATH_URL_LOGIN}/auth_register.html', form_data={})

@app.route('/recovery-password', methods=['GET'])
def cpanelRecoveryPassUser():
    if 'conectado' in session:
        return redirect(url_for('inicio'))
    else:
        return render_template(f'{PATH_URL_LOGIN}/auth_forgot_password.html')

@app.route('/saved-register', methods=['POST'])
def cpanelResgisterUserBD():
    if request.method == 'POST' and 'nombre' in request.form and 'contrasena' in request.form:
        tipo_documento = request.form['tipo_documento'].strip()
        documento = request.form['documento'].strip()
        nombre = request.form['nombre'].strip()
        apellido = request.form['apellido'].strip()
        telefono = request.form['telefono'].strip()
        correo = request.form['correo'].strip()
        contrasena = request.form['contrasena'].strip()
        confirm_contrasena = request.form['confirm_contrasena'].strip()

        print(f"Datos recibidos: {tipo_documento}, {documento}, {nombre}, {apellido}, {telefono}, {correo}, {contrasena}")  # Depuración

        # Validaciones
        if not all([tipo_documento, documento, nombre, apellido, telefono, correo, contrasena, confirm_contrasena]):
            flash('Todos los campos son obligatorios.', 'error')
            return render_template(f'{PATH_URL_LOGIN}/auth_register.html', form_data=request.form)

        if tipo_documento not in ['Cedula ciudadania', 'Tarjeta identidad', 'Cedula extranjeria', 'NIT']:
            flash('Seleccione un tipo de documento válido.', 'error')
            return render_template(f'{PATH_URL_LOGIN}/auth_register.html', form_data=request.form)

        if not documento.isdigit():
            flash('El documento debe contener solo números.', 'error')
            return render_template(f'{PATH_URL_LOGIN}/auth_register.html', form_data=request.form)

        if len(documento) < 6 or len(documento) > 15:
            flash('El documento debe tener entre 6 y 15 caracteres.', 'error')
            return render_template(f'{PATH_URL_LOGIN}/auth_register.html', form_data=request.form)

        if not nombre.isalpha() or not apellido.isalpha():
            flash('El nombre y apellido deben contener solo letras.', 'error')
            return render_template(f'{PATH_URL_LOGIN}/auth_register.html', form_data=request.form)

        if len(nombre) > 100 or len(apellido) > 100:
            flash('El nombre y apellido no deben exceder 100 caracteres.', 'error')
            return render_template(f'{PATH_URL_LOGIN}/auth_register.html', form_data=request.form)

        if not telefono.isdigit():
            flash('El teléfono debe contener solo números.', 'error')
            return render_template(f'{PATH_URL_LOGIN}/auth_register.html', form_data=request.form)

        if len(telefono) < 7 or len(telefono) > 10:
            flash('El teléfono debe tener entre 7 y 10 dígitos.', 'error')
            return render_template(f'{PATH_URL_LOGIN}/auth_register.html', form_data=request.form)

        if not re.match(r'[^@]+@[^@]+\.[^@]+', correo):
            flash('El correo electrónico no es válido.', 'error')
            return render_template(f'{PATH_URL_LOGIN}/auth_register.html', form_data=request.form)

        if len(correo) > 50:
            flash('El correo no debe exceder 50 caracteres.', 'error')
            return render_template(f'{PATH_URL_LOGIN}/auth_register.html', form_data=request.form)

        if len(contrasena) < 8 or len(contrasena) > 50:
            flash('La contraseña debe tener entre 8 y 50 caracteres.', 'error')
            return render_template(f'{PATH_URL_LOGIN}/auth_register.html', form_data=request.form)

        if not re.match(r'^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{8,50}$', contrasena):
            flash('La contraseña debe incluir letras y números.', 'error')
            return render_template(f'{PATH_URL_LOGIN}/auth_register.html', form_data=request.form)

        if contrasena != confirm_contrasena:
            flash('Las contraseñas no coinciden.', 'error')
            return render_template(f'{PATH_URL_LOGIN}/auth_register.html', form_data=request.form)

        # Verificar duplicados
        with connectionBD() as conexion_MySQLdb:
            with conexion_MySQLdb.cursor(dictionary=True) as cursor:
                cursor.execute("SELECT * FROM users WHERE documento = %s", (documento,))
                if cursor.fetchone():
                    flash('El documento ya está registrado.', 'error')
                    return render_template(f'{PATH_URL_LOGIN}/auth_register.html', form_data=request.form)

                cursor.execute("SELECT * FROM users WHERE correo = %s", (correo,))
                if cursor.fetchone():
                    flash('El correo ya está registrado.', 'error')
                    return render_template(f'{PATH_URL_LOGIN}/auth_register.html', form_data=request.form)

        resultData = recibeInsertRegisterUser(
            tipo_documento, documento, nombre, apellido, telefono, correo, contrasena
        )
        if resultData != 0:
            flash('La cuenta fue creada correctamente.', 'success')
            return redirect(url_for('inicio'))
        else:
            flash('Hubo un error al crear la cuenta.', 'error')
            print("Error al crear la cuenta.")  # Depuración
            return render_template(f'{PATH_URL_LOGIN}/auth_register.html', form_data=request.form)
    else:
        flash('El método HTTP es incorrecto o faltan campos en el formulario.', 'error')
        print("Método HTTP incorrecto o faltan campos en el formulario.")  # Depuración
        return render_template(f'{PATH_URL_LOGIN}/auth_register.html', form_data=request.form)

@app.route("/actualizar-datos-perfil", methods=['POST'])
def actualizarPerfil():
    if 'conectado' not in session:
        return jsonify({"success": False, "error": "Primero debes iniciar sesión."}), 401

    respuesta = procesar_update_perfil(request.form)
    if respuesta == 1:
        return jsonify({"success": True, "message": "Los datos fueron actualizados correctamente."}), 200
    elif respuesta == 0:
        return jsonify({"success": False, "error": "La contraseña actual es incorrecta."}), 400
    elif respuesta == 3:
        return jsonify({"success": False, "error": "La contraseña actual es obligatoria."}), 400
    elif respuesta == -1:
        return jsonify({"success": False, "error": "Error al actualizar los datos. Por favor, intenta de nuevo."}), 500
    else:
        return jsonify({"success": False, "error": "Error inesperado."}), 500

@app.route("/actualizar-password", methods=['POST'])
def actualizarPassword():
    if 'conectado' not in session:
        return jsonify({"success": False, "error": "Inicia sesión primero."}), 401

    respuesta = procesar_update_password(request.form)
    if respuesta == 1:
        return jsonify({"success": True, "message": "Contraseña actualizada correctamente."}), 200
    elif respuesta == 0:
        return jsonify({"success": False, "error": "Contraseña actual incorrecta."}), 400
    elif respuesta == 2:
        return jsonify({"success": False, "error": "Las contraseñas no coinciden."}), 400
    elif respuesta == 3:
        return jsonify({"success": False, "error": "Todos los campos son obligatorios."}), 400
    elif respuesta == 4:
        return jsonify({"success": False, "error": "La nueva contraseña debe tener entre 8 y 20 caracteres."}), 400
    elif respuesta == 5:
        return jsonify({"success": False, "error": "Debe combinar al menos dos de: letras, números o caracteres especiales (@$!%*?&)."}), 400
    elif respuesta == 6:
        return jsonify({"success": False, "error": "La contraseña no puede contener solo números."}), 400
    elif respuesta == 7:
        return jsonify({"success": False, "error": "La contraseña no puede contener solo letras."}), 400
    elif respuesta == 8:
        return jsonify({"success": False, "error": "La nueva contraseña no puede ser igual a la actual."}), 400
    else:
        return jsonify({"success": False, "error": "Error al actualizar."}), 500

@app.route('/cliente-perfil')
def perfil_cliente():
    if 'conectado' in session:
        if session['rol'] == 'cliente':
            user_id = session['id']

            with connectionBD() as conexion_MySQLdb:
                with conexion_MySQLdb.cursor(dictionary=True, buffered=True) as cursor:
                    cursor.execute("""
                        SELECT nombre, apellido, documento, correo, telefono, 
                               rol, estado, tipo_documento
                        FROM users
                        WHERE id = %s
                    """, (user_id,))
                    user_data = cursor.fetchone()
            
            info_perfil_session = {
                'nombre': user_data.get('nombre', session.get('nombre')),
                'apellido': user_data.get('apellido', session.get('apellido')),
                'documento': user_data.get('documento', session.get('documento')),
                'correo': user_data.get('correo', session.get('correo')),
                'telefono': user_data.get('telefono', session.get('telefono')),
                'rol': user_data.get('rol', session.get('rol')),
                'estado': user_data.get('estado', session.get('estado')),
                'tipo_documento': user_data.get('tipo_documento')
            }

            with connectionBD() as conexion_MySQLdb:
                with conexion_MySQLdb.cursor(dictionary=True) as cursor:
                    cursor.execute("""
                        SELECT d.id, d.nombre_completo, d.barrio, d.domicilio, d.referencias, d.telefono,
                               m.nombre AS nombre_municipio, dp.nombre AS nombre_departamento
                        FROM direccion d
                        JOIN municipio m ON d.municipio_id = m.id
                        JOIN departamento dp ON d.departamento_id = dp.id
                        WHERE d.users_id = %s
                    """, (user_id,))
                    direcciones = cursor.fetchall()

            pedidos = obtener_pedidos(user_id)

            with connectionBD() as conexion_MySQLdb:
                with conexion_MySQLdb.cursor(dictionary=True) as cursor:
                    cursor.execute("SELECT id, nombre FROM departamento ORDER BY nombre")
                    departamentos = cursor.fetchall()
                    cursor.execute("SELECT id, nombre, departamento_id FROM municipio ORDER BY nombre")
                    municipios = cursor.fetchall()

            return render_template(
                'public/perfil/perfil_cliente.html',
                info_perfil_session=info_perfil_session,
                direcciones=direcciones,
                pedidos=pedidos,
                departamentos=departamentos,
                municipios=municipios
            )
        else:
            return redirect(url_for('perfil'))
    else:
        flash('Acceso denegado.', 'error')
        return redirect(url_for('inicio'))

@app.route('/login', methods=['GET', 'POST'])
def loginCliente():
    if 'conectado' in session:
        return redirect(url_for('inicio'))

    if request.method == 'POST' and 'documento' in request.form and 'contrasena' in request.form:
        documento = request.form['documento'].strip()
        contrasena = request.form['contrasena'].strip()

        # Validaciones
        if not documento or not contrasena:
            flash('Todos los campos son obligatorios.', 'error')
            return render_template(f'{PATH_URL_LOGIN}/base_login.html')

        if not documento.isdigit():
            flash('El documento debe contener solo números.', 'error')
            return render_template(f'{PATH_URL_LOGIN}/base_login.html')

        if len(documento) < 6 or len(documento) > 15:
            flash('El documento debe tener entre 6 y 15 caracteres.', 'error')
            return render_template(f'{PATH_URL_LOGIN}/base_login.html')

        if len(contrasena) < 8:
            flash('La contraseña debe tener al menos 8 caracteres.', 'error')
            return render_template(f'{PATH_URL_LOGIN}/base_login.html')

        with connectionBD() as conexion_MySQLdb:
            cursor = conexion_MySQLdb.cursor(dictionary=True)
            cursor.execute(
                "SELECT id, nombre, apellido, telefono, correo, documento, contrasena, rol, estado FROM users WHERE documento = %s AND estado = 'activo'", 
                [documento]
            )
            account = cursor.fetchone()

            if account:
                if check_password_hash(account['contrasena'], contrasena):
                    session['rol'] = account['rol']
                    session['estado'] = account['estado']
                    session['conectado'] = True
                    session['id'] = account['id']
                    session['nombre'] = account['nombre']
                    session['apellido'] = account['apellido']
                    session['telefono'] = account['telefono']
                    session['correo'] = account['correo']
                    session['documento'] = account['documento']

                    flash('Sesión iniciada correctamente', 'success')

                    if session['rol'] == 'cliente':
                        return redirect(url_for('indexPrincipal'))  # Redirige al sitio web para clientes
                    elif session['rol'] in ['administrador', 'superadmin', 'empleado']:
                        return redirect(url_for('perfil_aplicativo'))  # Redirige al panel para otros roles
                else:
                    flash('Contraseña incorrecta', 'error')
                    return render_template(f'{PATH_URL_LOGIN}/base_login.html')
            else:
                flash('Usuario inactivo o no existe', 'error')
                return render_template(f'{PATH_URL_LOGIN}/base_login.html')
    else:
        # Manejar el método GET: renderizar el formulario de login
        return render_template(f'{PATH_URL_LOGIN}/base_login.html')

@app.route('/closed-session', methods=['GET'])
def cerraSesion():
    if request.method == 'GET':
        if 'conectado' in session:
            session.pop('conectado', None)
            session.pop('id', None)
            session.pop('nombre', None)
            session.pop('apellido', None)
            session.pop('telefono', None)
            session.pop('correo', None)
            session.pop('documento', None)
            flash('Tu sesión fue cerrada correctamente.', 'success')
            return redirect(url_for('inicio'))
        else:
            flash('Recuerde, debe iniciar sesión.', 'error')
            return render_template(f'{PATH_URL_LOGIN}/base_login.html')
@app.route('/obtener-detalles-pedido/<int:pedido_id>', methods=['GET'])
def obtener_detalles_pedido(pedido_id):
    if 'conectado' in session:
        try:
            with connectionBD() as conexion_MySQLdb:
                with conexion_MySQLdb.cursor(dictionary=True) as cursor:
                    cursor.execute("""
                        SELECT p.id, p.fecha, p.fechaEntrega, p.horaEntrega, p.estado, 
                               p.total AS total_pedido,
                               mp.metodo AS metodo_pago, 
                               e.tipo AS tipo_entrega,
                               e.costo_domicilio,
                               e.estado AS estado_entrega,
                               e.direccion_id,
                               u.nombre AS usuario_nombre, u.apellido,
                               pr.nombre AS producto_nombre
                        FROM pedido p
                        JOIN users u ON p.users_id = u.id
                        JOIN producto pr ON p.producto_id = pr.id
                        JOIN metodo_pago mp ON p.metodo_pago_id = mp.id
                        JOIN entrega e ON p.entrega_id = e.id
                        WHERE p.id = %s AND p.users_id = %s
                    """, (pedido_id, session['id']))
                    pedido = cursor.fetchone()
                    
                    if not pedido:
                        return jsonify({'error': 'Pedido no encontrado'}), 404
                    
                    pedido['fechaEntrega'] = pedido['fechaEntrega'].strftime('%d/%m/%Y') if pedido['fechaEntrega'] else "No disponible"
                    pedido['fecha'] = pedido['fecha'].strftime('%d/%m/%Y %H:%M')
                    
                    if isinstance(pedido['horaEntrega'], timedelta):
                        horas, segundos = divmod(pedido['horaEntrega'].seconds, 3600)
                        minutos = (segundos // 60)
                        pedido['horaEntrega'] = f"{horas:02d}:{minutos:02d}"
                    else:
                        pedido['horaEntrega'] = pedido['horaEntrega'].strftime('%H:%M') if pedido['horaEntrega'] else "No disponible"
                    
                    pedido['usuario_nombre'] = f"{pedido['usuario_nombre']} {pedido['apellido']}"
                    
                    cursor.execute("""
                        SELECT dp.id, dp.cantidad, dp.precio_unitario, dp.total,
                               p.nombre AS producto_nombre
                        FROM detalle_pedido dp
                        JOIN producto p ON dp.producto_id = p.id
                        WHERE dp.pedido_id = %s
                    """, (pedido_id,))
                    detalles_pedido = cursor.fetchall()
                    
                    for detalle in detalles_pedido:
                        detalle['precio_unitario'] = float(detalle['precio_unitario'])
                        detalle['total'] = float(detalle['total'])
                    
                    pedido['total_pedido'] = float(pedido['total_pedido'])
                    pedido['costo_domicilio'] = float(pedido['costo_domicilio']) if pedido['costo_domicilio'] else None
                    
                    return jsonify({
                        'pedido': pedido,
                        'detalles_pedido': detalles_pedido
                    })
                    
        except Exception as e:
            print(f"Error al obtener detalles del pedido: {e}")
            return jsonify({'error': str(e)}), 500
    else:
        return jsonify({'error': 'Usuario no autorizado'}), 401
