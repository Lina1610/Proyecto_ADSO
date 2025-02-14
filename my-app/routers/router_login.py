from app import app
from flask import render_template, request, flash, redirect, url_for, session

# Importando mi conexión a BD
from conexion.conexionBD import connectionBD

# Para encriptar contraseña generate_password_hash
from werkzeug.security import check_password_hash

# Importando controllers para el modulo de login
from controllers.funciones_login import *

from controllers.funciones_login import recibeInsertRegisterUser, validarDataRegisterLogin, info_perfil_session, procesar_update_perfil, updatePefilSinPass, dataLoginSesion
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
        return render_template(f'public/perfil/perfil.html', info_perfil_session=info_perfil_session())
    else:
        return redirect(url_for('inicio'))


# Crear cuenta de usuario
@app.route('/register-user', methods=['GET'])
def cpanelRegisterUser():
    if 'conectado' in session:
        return redirect(url_for('inicio'))
    else:
        return render_template(f'{PATH_URL_LOGIN}/auth_register.html')


# Recuperar cuenta de usuario
@app.route('/recovery-password', methods=['GET'])
def cpanelRecoveryPassUser():
    if 'conectado' in session:
        return redirect(url_for('inicio'))
    else:
        return render_template(f'{PATH_URL_LOGIN}/auth_forgot_password.html')

# Crear cuenta de usuario
@app.route('/saved-register', methods=['POST'])
def cpanelResgisterUserBD():
    print("Iniciando cpanelResgisterUserBD...")  # Depuración
    if request.method == 'POST' and 'nombre' in request.form and 'contrasena' in request.form:
        tipo_documento = request.form['tipo_documento']
        documento = request.form['documento']
        nombre = request.form['nombre']
        apellido = request.form['apellido']
        telefono = request.form['telefono']
        correo = request.form['correo']
        contrasena = request.form['contrasena']

        print(f"Datos recibidos: {tipo_documento}, {documento}, {nombre}, {apellido}, {telefono}, {correo}, {contrasena}")  # Depuración

        resultData = recibeInsertRegisterUser(
            tipo_documento, documento, nombre, apellido, telefono, correo, contrasena
        )
        if resultData != 0:
            flash('La cuenta fue creada correctamente.', 'success')
            print("Cuenta creada correctamente.")  # Depuración
            return redirect(url_for('inicio'))
        else:
            flash('Hubo un error al crear la cuenta.', 'error')
            print("Error al crear la cuenta.")  # Depuración
            return redirect(url_for('inicio'))
    else:
        flash('El método HTTP es incorrecto o faltan campos en el formulario.', 'error')
        print("Método HTTP incorrecto o faltan campos en el formulario.")  # Depuración
        return redirect(url_for('inicio'))
    

# Actualizar datos de mi perfil
@app.route("/actualizar-datos-perfil", methods=['POST'])
def actualizarPerfil():
    if request.method == 'POST':
        if 'conectado' in session:
            respuesta = procesar_update_perfil(request.form)
            if respuesta == 1:
                flash('Los datos fuerón actualizados correctamente.', 'success')
                return redirect(url_for('inicio'))
            elif respuesta == 0:
                flash(
                    'La contraseña actual esta incorrecta, por favor verifique.', 'error')
                return redirect(url_for('perfil'))
            elif respuesta == 2:
                flash('Ambas claves deben se igual, por favor verifique.', 'error')
                return redirect(url_for('perfil'))
            elif respuesta == 3:
                flash('La Clave actual es obligatoria.', 'error')
                return redirect(url_for('perfil'))
        else:
            flash('primero debes iniciar sesión.', 'error')
            return redirect(url_for('inicio'))
    else:
        flash('primero debes iniciar sesión.', 'error')
        return redirect(url_for('inicio'))


# Validar sesión
@app.route('/login', methods=['GET', 'POST'])
def loginCliente():
    if 'conectado' in session:
        return redirect(url_for('inicio'))
    else:
        if request.method == 'POST' and 'documento' in request.form and 'contrasena' in request.form:

            documento = request.form['documento']
            contrasena = request.form['contrasena']

            # Comprobando si existe una cuenta
            conexion_MySQLdb = connectionBD()
            cursor = conexion_MySQLdb.cursor(dictionary=True)
            cursor.execute("SELECT * FROM users WHERE documento = %s", [documento])
            account = cursor.fetchone()

            if account:
                if check_password_hash(account['contrasena'], contrasena):
                    # Crear datos de sesión, para poder acceder a estos datos en otras rutas
                    session['conectado'] = True
                    session['id'] = account['id']
                    session['nombre'] = account['nombre']
                    session['apellido'] = account['apellido']
                    session['telefono'] = account['telefono']
                    session['correo'] = account['correo']
                    session['documento'] = account['documento']

                    flash('La sesión fue correcta.', 'success')
                    return redirect(url_for('inicio'))
                else:
                    # La contraseña es incorrecta
                    flash('Datos incorrectos, por favor revise.', 'error')
                    return render_template(f'{PATH_URL_LOGIN}/base_login.html')
            else:
                # El documento no existe
                flash('El usuario no existe, por favor verifique.', 'error')
                return render_template(f'{PATH_URL_LOGIN}/base_login.html')
        else:
            flash('Primero debes iniciar sesión.', 'error')
            return render_template(f'{PATH_URL_LOGIN}/base_login.html')
        
@app.route('/closed-session', methods=['GET'])
def cerraSesion():
    if request.method == 'GET':
        if 'conectado' in session:
            # Eliminar datos de sesión, esto cerrará la sesión del usuario
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