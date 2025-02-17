from app import app
from flask import render_template, request, flash, redirect, url_for, session, jsonify
from mysql.connector.errors import Error
from controllers.funciones_user import lista_usuariosBD, obtener_usuario_por_id, buscarUsuarioBD, eliminar_usuario, procesar_usuario
from conexion.conexionBD import connectionBD
from flask_mail import Mail, Message
import secrets
from datetime import datetime, timedelta
from controllers.funciones_user import actualizar_password




# Configuración del correo
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'EMAIL_SENDER'
app.config['MAIL_PASSWORD'] = 'EMAIL_PASSWORD'

mail = Mail(app)

PATH_URL = "public/usuario"

EXPIRACION_TOKEN = timedelta(hours=1)

tokens_recuperacion = {}

@app.route('/registrar-usuario', methods=['GET', 'POST'])
def viewFormUsuario():
    if 'conectado' in session:
        if request.method == 'POST':
            data_form = request.form
            resultado = procesar_usuario(data_form)
            if isinstance(resultado, int) and resultado > 0:
                flash('Usuario registrado con éxito', 'success')
                return redirect(url_for('viewFormUsuario'))
            else:
                flash(f'Error al registrar usuario: {resultado}', 'error')
        return render_template('public/nuevosUsuarios/registro_usuario.html')
    else:
        flash('Primero debes iniciar sesión.', 'error')
        return redirect(url_for('inicio'))

@app.route('/lista-de-usuarios')
def lista_usuarios():
    if 'conectado' in session:
        usuarios = lista_usuariosBD()
        return render_template('public/nuevosUsuarios/lista_usuarios.html', resp_usuariosBD=usuarios)
    else:
        flash('Primero debes iniciar sesión.', 'error')
        return redirect(url_for('inicio'))

@app.route("/editar-usuario/<int:id>", methods=['GET'])
def viewEditarUsuario(id):
    if 'conectado' in session:
        usuario = obtener_usuario_por_id(id)
        if usuario:
            return render_template('public/nuevosUsuarios/editar_usuario.html', usuario=usuario)
        else:
            flash('El usuario no existe.', 'error')
            return redirect(url_for('usuarios'))
    else:
        flash('Primero debes iniciar sesión.', 'error')
        return redirect(url_for('inicio'))

@app.route("/detalles-usuario/<int:id>", methods=['GET'])
def detallesUsuario(id):
    if 'conectado' in session:
        usuario = obtener_usuario_por_id(id)
        if usuario:
            return render_template('public/nuevosUsuarios/detalles_usuario.html', usuario=usuario)
        else:
            flash('El usuario no existe.', 'error')
            return redirect(url_for('usuarios'))
    else:
        flash('Primero debes iniciar sesión.', 'error')
        return redirect(url_for('inicio'))

@app.route('/actualizar-usuario', methods=['POST'])
def actualizarUsuario():
    if 'conectado' in session:
        id = request.form['id']
        nombre = request.form['nombre']
        apellido = request.form['apellido']
        tipo_documento = request.form['tipo_documento']
        documento = request.form['documento']
        correo = request.form['correo']
        telefono = request.form['telefono']
        rol = request.form['rol']
        estado = request.form['estado']

        with connectionBD() as conexion_MySQLdb:
            with conexion_MySQLdb.cursor(dictionary=True) as cursor:
                querySQL = """
                    UPDATE users
                    SET nombre = %s, apellido = %s, tipo_documento = %s, documento = %s, correo = %s, telefono = %s, rol = %s, estado = %s
                    WHERE id = %s
                """
                valores = (nombre, apellido, tipo_documento, documento, correo, telefono, rol, estado, id)
                cursor.execute(querySQL, valores)
                conexion_MySQLdb.commit()

        flash('Usuario actualizado correctamente.', 'success')
        return redirect(url_for('usuarios'))
    else:
        flash('Primero debes iniciar sesión.', 'error')
        return redirect(url_for('inicio'))

@app.route("/buscando-usuario", methods=['POST'])
def viewBuscarUsuarioBD():
    resultadoBusqueda = buscarUsuarioBD(request.json['busqueda'])
    if resultadoBusqueda:
        return render_template('public/nuevosUsuarios/busqueda_usuario.html', dataBusqueda=resultadoBusqueda)
    else:
        return jsonify({'success': False, 'html': '<tr><td colspan="6" class="text-center">No se encontraron resultados.</td></tr>'})

@app.route('/eliminar-usuario/<int:id>', methods=['GET'])
def eliminarUsuario(id):
    if 'conectado' in session:
        resultado = eliminar_usuario(id)
        if resultado:
            flash('Usuario eliminado correctamente.', 'success')
            return jsonify({"success": True})
        else:
            flash('Error al eliminar el usuario', 'error')
            return jsonify({"success": False})
    else:
        flash('Primero debes iniciar sesión', 'error')
        return jsonify({"success": False})

# Recuperación de contraseña
from datetime import datetime, timedelta

# Tiempo de expiración del token (por ejemplo, 1 hora)
EXPIRACION_TOKEN = timedelta(hours=1)

tokens_recuperacion = {}

@app.route('/recuperar-password', methods=['GET', 'POST'])
def recuperarPassword():
    if request.method == 'POST':
        correo = request.form['correo']
        usuario = buscarUsuarioBD(correo)
        
        if usuario:  # Si se encuentra un usuario
            usuario = usuario[0]  # Asegúrate de obtener el primer usuario en la lista
            token = secrets.token_urlsafe(16)
            tokens_recuperacion[token] = {
                'user_id': usuario['id'],
                'fecha_creacion': datetime.utcnow()  # Guardamos la fecha y hora en UTC
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
    # Verificar si el token es válido
    if token not in tokens_recuperacion:
        flash('Token inválido o expirado.', 'error')
        return redirect(url_for('inicio'))  # Redirige al inicio si el token no es válido

    # Verificar si el token ha expirado
    token_data = tokens_recuperacion[token]
    fecha_creacion = token_data['fecha_creacion']
    if datetime.utcnow() - fecha_creacion > EXPIRACION_TOKEN:
        flash('El enlace ha expirado. Solicita uno nuevo.', 'error')
        del tokens_recuperacion[token]  # Eliminar el token expirado
        return redirect(url_for('recuperarPassword'))  # Redirige al formulario de recuperación de contraseña

    if request.method == 'POST':
        nueva_password = request.form['password']  # Obtener la nueva contraseña desde el formulario
        user_id = token_data['user_id']  # Obtener el ID del usuario asociado al token
        
        # Actualizar la contraseña en la base de datos
        if actualizar_password(user_id, nueva_password):
            flash('Contraseña restablecida con éxito.', 'success')
            del tokens_recuperacion[token]  # Eliminar el token una vez usado
            return redirect(url_for('inicio'))  # Redirigir al inicio si todo sale bien
        else:
            flash('Hubo un error al restablecer la contraseña.', 'error')
    
    return render_template('public/login/auth_reset_password.html', token=token)
