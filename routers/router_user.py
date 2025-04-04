from app import app
from flask import render_template, request, flash, redirect, url_for, session, jsonify
from mysql.connector.errors import Error
from controllers.funciones_user import lista_usuariosBD, obtener_usuario_por_id, buscarUsuarioBD, eliminar_usuario, procesar_usuario
from conexion.conexionBD import connectionBD
from flask_mail import Mail, Message
import secrets
import re
from datetime import datetime, timedelta
from controllers.funciones_user import actualizar_password
from controllers.funciones_user import actualizar_datos_usuario
import os
from werkzeug.utils import secure_filename
from middleware import roles_required  # Importación del middleware
from controllers.funciones_user import cambiar_estado_usuario
from app import app, mail  # Añade mail aquí


PATH_URL = "public/usuario"
EXPIRACION_TOKEN = timedelta(hours=1)
tokens_recuperacion = {}

# ============================================== RUTAS PROTEGIDAS CON ROLES ==============================================

@app.route('/registrar-usuario', methods=['GET', 'POST'])
@roles_required('administrador', 'superadmin')
def viewFormUsuario():
    if request.method == 'POST':
        data_form = request.form
        print("Datos recibidos:", data_form)  # Depuración
        resultado = procesar_usuario(data_form)
        if isinstance(resultado, int) and resultado > 0:
            flash('Usuario registrado con éxito', 'success')
            return redirect(url_for('viewFormUsuario'))
        else:
            flash(f'Error al registrar usuario: {resultado}', 'error')
    return render_template('public/nuevosUsuarios/registro_usuario.html')

@app.route('/activar-usuario/<int:user_id>')
@roles_required('administrador','superadmin')
def activar_usuario(user_id):
    resultado = cambiar_estado_usuario(user_id, 'activo')
    if resultado > 0:
        flash('Usuario activado', 'success')
    else:
        flash('Error al activar', 'error')
    return redirect(url_for('lista_usuarios'))

@app.route('/desactivar-usuario/<int:user_id>')
@roles_required('administrador','superadmin')  # Añade esta ruta
def desactivar_usuario(user_id):
    resultado = cambiar_estado_usuario(user_id, 'inactivo')
    if resultado > 0:
        flash('Usuario desactivado', 'success')
    else:
        flash('Error al desactivar', 'error')
    return redirect(url_for('lista_usuarios'))

@app.route('/lista-de-usuarios')
@roles_required('administrador','superadmin')  # Decorador aplicado
def lista_usuarios():
    usuarios = lista_usuariosBD()
    return render_template('public/nuevosUsuarios/lista_usuarios.html', resp_usuariosBD=usuarios)

@app.route("/editar-usuario/<int:id>", methods=['GET'])
@roles_required('administrador','superadmin')  # Decorador aplicado
def viewEditarUsuario(id):
    usuario = obtener_usuario_por_id(id)
    if usuario:
        return render_template('public/nuevosUsuarios/editar_usuario.html', usuario=usuario)
    flash('El usuario no existe.', 'error')
    return redirect(url_for('lista_usuarios'))

@app.route("/detalles-usuario/<int:id>", methods=['GET'])
@roles_required('administrador','superadmin')  # Decorador aplicado
def detallesUsuario(id):
    usuario = obtener_usuario_por_id(id)
    if usuario:
        return render_template('public/nuevosUsuarios/detalles_usuario.html', usuario=usuario)
    flash('El usuario no existe.', 'error')
    return redirect(url_for('lista_usuarios'))

@app.route('/actualizar-usuario', methods=['POST'])
@roles_required('administrador','superadmin')  # Decorador aplicado
def actualizarUsuario():
    id = request.form['id']
    nombre = request.form['nombre']
    apellido = request.form['apellido']
    tipo_documento = request.form['tipo_documento']
    documento = request.form['documento']
    correo = request.form['correo']
    telefono = request.form['telefono']
    rol = request.form['rol']
    estado = request.form['estado']

    # Validaciones similares a procesar_usuario
    # Validar que los campos no estén vacíos
    campos_requeridos = ['tipo_documento', 'documento', 'nombre', 'apellido', 'telefono', 'correo', 'rol', 'estado']
    for campo in campos_requeridos:
        if not request.form[campo].strip():
            flash(f"El campo {campo} es obligatorio.", 'error')
            return redirect(url_for('viewEditarUsuario', id=id))

    # Validar tipo de documento
    valores_permitidos = ['Cedula ciudadania', 'Tarjeta identidad', 'Cedula extranjeria', 'NIT']
    if tipo_documento not in valores_permitidos:
        flash(f"El tipo de documento '{tipo_documento}' no es válido.", 'error')
        return redirect(url_for('viewEditarUsuario', id=id))

    # Validar documento y teléfono como números
    try:
        documento = int(documento)
        telefono = int(telefono)
    except ValueError:
        flash('El documento y el teléfono deben ser números válidos.', 'error')
        return redirect(url_for('viewEditarUsuario', id=id))

    # Validar documento: mayor a 0 y entre 10 y 15 dígitos
    if documento <= 0:
        flash("El documento debe ser mayor a 0.", 'error')
        return redirect(url_for('viewEditarUsuario', id=id))
    doc_str = str(documento)
    if len(doc_str) < 10 or len(doc_str) > 15:
        flash("El documento debe tener entre 10 y 15 dígitos.", 'error')
        return redirect(url_for('viewEditarUsuario', id=id))

    # Validar teléfono: mayor a 0 y entre 7 y 13 dígitos
    if telefono <= 0:
        flash("El teléfono debe ser mayor a 0.", 'error')
        return redirect(url_for('viewEditarUsuario', id=id))
    tel_str = str(telefono)
    if len(tel_str) < 7 or len(tel_str) > 13:
        flash("El teléfono debe tener entre 7 y 13 dígitos.", 'error')
        return redirect(url_for('viewEditarUsuario', id=id))

    # Validar longitud de nombre y apellido (mínimo 2, máximo 100)
    if len(nombre) < 2 or len(apellido) < 2:
        flash("El nombre y apellido deben tener al menos 2 caracteres.", 'error')
        return redirect(url_for('viewEditarUsuario', id=id))
    if len(nombre) > 100 or len(apellido) > 100:
        flash("El nombre o apellido no puede exceder los 100 caracteres.", 'error')
        return redirect(url_for('viewEditarUsuario', id=id))

    # Validar correo: máximo 50 caracteres y formato válido
    if len(correo) > 50:
        flash("El correo no puede exceder los 50 caracteres.", 'error')
        return redirect(url_for('viewEditarUsuario', id=id))
    email_pattern = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    if not re.match(email_pattern, correo):
        flash("El correo no tiene un formato válido.", 'error')
        return redirect(url_for('viewEditarUsuario', id=id))

    # Verificar si el documento o correo ya existen (excepto para el usuario actual)
    with connectionBD() as conexion_MySQLdb:
        with conexion_MySQLdb.cursor(dictionary=True) as cursor:
            querySQL = "SELECT * FROM users WHERE (documento = %s OR correo = %s) AND id != %s"
            cursor.execute(querySQL, (documento, correo, id))
            usuario_existente = cursor.fetchone()

            if usuario_existente:
                flash('El documento o correo ya está registrado en el sistema.', 'error')
                return redirect(url_for('viewEditarUsuario', id=id))

    # Si pasa todas las validaciones, actualizar el usuario
    with connectionBD() as conexion_MySQLdb:
        with conexion_MySQLdb.cursor(dictionary=True) as cursor:
            querySQL = """
                UPDATE users
                SET nombre = %s, apellido = %s, tipo_documento = %s, documento = %s, 
                    correo = %s, telefono = %s, rol = %s, estado = %s
                WHERE id = %s
            """
            valores = (nombre, apellido, tipo_documento, documento, correo, telefono, rol, estado, id)
            cursor.execute(querySQL, valores)
            conexion_MySQLdb.commit()

    flash('Usuario actualizado correctamente.', 'success')
    return redirect(url_for('lista_usuarios'))

@app.route('/eliminar-usuario/<int:id>', methods=['GET'])
@roles_required('administrador', 'superadmin')
def eliminarUsuario(id):
    resultado = eliminar_usuario(id)
    print(f"Resultado de eliminar_usuario: {resultado}")
    
    if resultado:
        flash('Usuario eliminado correctamente.', 'success')
    else:
        flash('Error al eliminar el usuario', 'error')
    
    # Redireccionar a la lista de usuarios
    return redirect(url_for('lista_usuarios'))  # Ajusta 'lista_usuarios' a tu ruta correcta

# ============================================== RUTAS PÚBLICAS ==============================================

@app.route("/buscando-usuario", methods=['POST'])
def viewBuscarUsuarioBD():
    busqueda = request.json['busqueda']
    resultadoBusqueda = buscarUsuarioBD(busqueda)

    if resultadoBusqueda:
        html_resultados = render_template('public/nuevosUsuarios/busqueda_usuario.html', dataBusqueda=resultadoBusqueda)
        return jsonify({'success': True, 'html': html_resultados})
    
    mensaje_error = f'No resultados para la búsqueda: "{busqueda}"'
    return jsonify({'success': False, 'mensaje': mensaje_error})

@app.route('/recuperar-password', methods=['GET', 'POST'])
def recuperarPassword():
    if request.method == 'POST':
        correo = request.form['correo']
        usuario = buscarUsuarioBD(correo)
        if usuario:
            usuario = usuario[0]
            token = secrets.token_urlsafe(16)
            tokens_recuperacion[token] = {
                'user_id': usuario['id'],
                'fecha_creacion': datetime.utcnow()
            }
            enlace = url_for('resetPassword', token=token, _external=True)
            msg = Message('Recuperación de contraseña', sender=app.config['MAIL_USERNAME'], recipients=[correo])
            msg.body = f'Usa este enlace para restablecer tu contraseña: {enlace}'
            mail.send(msg)
            flash('Revisa tu correo para restablecer tu contraseña.', 'success')
        else:
            flash('El correo no está registrado.', 'error')
    return render_template('public/login/auth_forgot_password.html')

@app.route('/reset-password/<token>', methods=['GET', 'POST'])
def resetPassword(token):
    if token not in tokens_recuperacion:
        flash('Token inválido o expirado.', 'error')
        return redirect(url_for('inicio'))

    token_data = tokens_recuperacion[token]
    if datetime.utcnow() - token_data['fecha_creacion'] > EXPIRACION_TOKEN:
        del tokens_recuperacion[token]
        flash('El enlace ha expirado. Solicita uno nuevo.', 'error')
        return redirect(url_for('recuperarPassword'))

    if request.method == 'POST':
        nueva_password = request.form['password']
        if actualizar_password(token_data['user_id'], nueva_password):
            del tokens_recuperacion[token]
            flash('Contraseña restablecida con éxito.', 'success')
            return redirect(url_for('inicio'))
        flash('Hubo un error al restablecer la contraseña.', 'error')
    
    return render_template('public/login/auth_reset_password.html', token=token)

@app.route('/actualizar-datos-perfil', methods=['POST'])
def actualizar_datos_perfil():
    if 'conectado' not in session:
        return jsonify({'success': False, 'message': 'Debes iniciar sesión'})

    # Obtener los datos del formulario
    nombre = request.form['nombre'].strip()
    apellido = request.form['apellido'].strip()
    telefono = request.form['telefono'].strip()
    documento = request.form['documento'].strip()
    pass_actual = request.form['pass_actual'].strip()

    # Validaciones para Nombre
    if not nombre:
        return jsonify({'success': False, 'message': 'El nombre no puede estar vacío.'})
    if len(nombre) > 150:
        return jsonify({'success': False, 'message': 'El nombre no puede exceder los 150 caracteres.'})

    # Validaciones para Apellido
    if not apellido:
        return jsonify({'success': False, 'message': 'El apellido no puede estar vacío.'})
    if len(apellido) > 150:
        return jsonify({'success': False, 'message': 'El apellido no puede exceder los 150 caracteres.'})

    # Validaciones para Teléfono
    if not telefono:
        return jsonify({'success': False, 'message': 'El teléfono no puede estar vacío.'})
    if len(telefono) < 7 or len(telefono) > 13:
        return jsonify({'success': False, 'message': 'El teléfono debe tener entre 7 y 13 dígitos.'})
    if not telefono.isdigit():
        return jsonify({'success': False, 'message': 'El teléfono solo debe contener números.'})

    # Validar la contraseña actual
    user_id = session['id']
    with connectionBD() as conexion_MySQLdb:
        with conexion_MySQLdb.cursor(dictionary=True) as cursor:
            query = "SELECT contrasena FROM users WHERE id = %s"
            cursor.execute(query, (user_id,))
            usuario = cursor.fetchone()
            if not usuario or not check_password_hash(usuario['contrasena'], pass_actual):
                return jsonify({'success': False, 'message': 'La contraseña actual es incorrecta.'})

    # Actualizar los datos del usuario
    if actualizar_datos_usuario(user_id, nombre, apellido, documento, telefono=telefono):
        return jsonify({'success': True, 'message': 'Datos actualizados correctamente.', 'reload': True})
    return jsonify({'success': False, 'message': 'Error al actualizar datos'})

@app.route('/cambiar-contrasena', methods=['POST'])
@roles_required('administrador', 'superadmin')
def cambiar_contrasena():
    if 'conectado' not in session:
        flash('Debes iniciar sesión', 'error')
        return redirect(url_for('login'))

    try:
        user_id = request.form['user_id']
        nueva_password = request.form['new_pass_user'].strip()
        repetir_password = request.form['repetir_pass_user'].strip()

        # Validar que las contraseñas coincidan
        if nueva_password != repetir_password:
            flash('Las contraseñas no coinciden', 'error')
            return redirect(url_for('viewEditarUsuario', id=user_id))

        # Validar longitud de la contraseña
        if len(nueva_password) < 8 or len(nueva_password) > 20:
            flash('La contraseña debe tener entre 8 y 20 caracteres', 'error')
            return redirect(url_for('viewEditarUsuario', id=user_id))

        # Validar complejidad
        has_letters = bool(re.search(r'[a-zA-Z]', nueva_password))
        has_numbers = bool(re.search(r'[0-9]', nueva_password))
        has_special = bool(re.search(r'[!@#$%^&*]', nueva_password))
        
        if sum([has_letters, has_numbers, has_special]) < 2:
            flash('La contraseña debe contener al menos dos de: letras, números o caracteres especiales', 'error')
            return redirect(url_for('viewEditarUsuario', id=user_id))

        # Actualizar la contraseña
        if actualizar_password(user_id, nueva_password):
            flash('Contraseña actualizada correctamente', 'success')
            return redirect(url_for('viewEditarUsuario', id=user_id))
        
        flash('Error al actualizar la contraseña', 'error')
        return redirect(url_for('viewEditarUsuario', id=user_id))
    
    except KeyError as e:
        flash(f'Falta el campo {str(e)} en el formulario', 'error')
        return redirect(url_for('lista_usuarios'))
    except Exception as e:
        print(f"Error en cambiar_contrasena: {e}")
        flash('Error interno del servidor', 'error')
        return redirect(url_for('lista_usuarios'))