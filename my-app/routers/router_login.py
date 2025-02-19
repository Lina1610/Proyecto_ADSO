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
        info_perfil = info_perfil_session()  # Obtener los datos del usuario
        if info_perfil:
            return render_template('public/perfil/perfil.html', info_perfil_session=info_perfil)
        else:
            flash('No se pudieron cargar los datos del perfil.', 'error')
            return redirect(url_for('inicio'))
    else:
        flash('Primero debes iniciar sesión.', 'error')
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
    if 'conectado' in session:
        respuesta = procesar_update_perfil(request.form)
        if respuesta == 1:
            flash('Los datos fueron actualizados correctamente.', 'success')
        elif respuesta == 0:
            flash('La contraseña actual es incorrecta.', 'error')
        elif respuesta == 2:
            flash('Las contraseñas no coinciden.', 'error')
        elif respuesta == 3:
            flash('La contraseña actual es obligatoria.', 'error')
        else:
            flash('Error al actualizar los datos.', 'error')
        return redirect(url_for('perfil'))
    else:
        flash('Primero debes iniciar sesión.', 'error')
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

            conexion_MySQLdb = connectionBD()
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

                    # 🔥 Redirigir según el rol 🔥
                    if session['rol'] == 'cliente':
                        return redirect(url_for('home'))  # Cliente va a index.html
                    else:
                        return redirect(url_for('inicio'))  # Admin/empleado a base_cpanel.html
                else:
                    flash('Contraseña incorrecta', 'error')
                    return render_template(f'{PATH_URL_LOGIN}/base_login.html')
            else:
                flash('Usuario inactivo o no existe', 'error')
                return render_template(f'{PATH_URL_LOGIN}/base_login.html')
        else:
            flash('Complete todos los campos', 'error')
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