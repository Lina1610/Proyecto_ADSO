from app import app
from flask import render_template, request, flash, redirect, url_for, session

# Importando mi conexión a BD
from conexion.conexionBD import connectionBD

# Para encriptar contraseña generate_password_hash
from werkzeug.security import check_password_hash

# Importando controllers para el modulo de login
from controllers.funciones_login import *
from flask import Flask, jsonify, request
from controllers.funciones_address import obtener_direcciones_usuario
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
        # Verificar que no sea un cliente intentando acceder al perfil administrativo
        if session['rol'] == 'cliente':
            return redirect(url_for('perfil_cliente'))
            
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
        
        # Redirigir según el rol del usuario
        if session.get('rol') == 'cliente':
            return redirect(url_for('perfil_cliente'))
        else:
            return redirect(url_for('perfil'))
    else:
        flash('Primero debes iniciar sesión.', 'error')
        return redirect(url_for('inicio'))

# También actualizar la función de actualizar contraseña
@app.route("/actualizar-password", methods=['POST'])
def actualizarPassword():
    if 'conectado' in session:
        respuesta = procesar_update_password(request.form)
        if respuesta == 1:
            flash('Contraseña actualizada correctamente.', 'success')
        elif respuesta == 0:
            flash('Contraseña actual incorrecta.', 'error')
        elif respuesta == 2:
            flash('Las contraseñas no coinciden.', 'error')
        elif respuesta == 3:
            flash('Debes ingresar tu contraseña actual.', 'error')
        else:
            flash('Error al actualizar.', 'error')
        
        # Redirigir según el rol del usuario
        if session.get('rol') == 'cliente':
            return redirect(url_for('perfil_cliente'))
        else:
            return redirect(url_for('perfil'))
    else:
        flash('Inicia sesión primero.', 'error')
        return redirect(url_for('inicio'))


@app.route('/cliente-perfil')
def perfil_cliente():
    if 'conectado' in session:
        if session['rol'] == 'cliente':
            # Obtener el ID del usuario de la sesión
            user_id = session.get('id')
            
            # Obtener departamentos y municipios desde la base de datos
            with connectionBD() as conexion_MySQLdb:
                with conexion_MySQLdb.cursor(dictionary=True) as cursor:
                    cursor.execute("SELECT id, nombre FROM departamento")
                    departamentos = cursor.fetchall()

                    cursor.execute("SELECT id, nombre FROM municipio")
                    municipios = cursor.fetchall()
            
            # Obtener las direcciones del usuario
            direcciones = obtener_direcciones_usuario(user_id)

            return render_template(
                'public/perfil/perfil_cliente.html',
                info_perfil_session=info_perfil_session(),
                departamentos=departamentos,
                municipios=municipios,
                direcciones=direcciones  # Agregamos las direcciones
            )
        else:
            # Si no es cliente, redirigir al perfil administrativo
            return redirect(url_for('perfil'))
    else:
        flash('Acceso denegado.', 'error')
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
                        return redirect(url_for('perfil'))  # Admin/empleado a base_cpanel.html
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
            return redirect(url_for('indexPrincipal'))
        else:
            flash('Recuerde, debe iniciar sesión.', 'error')
            return render_template(f'{PATH_URL_LOGIN}/base_login.html')
        


@app.route('/obtener_municipios', methods=['GET'], endpoint='obtener_municipios_2')
def obtener_municipios():
    departamento_id = request.args.get('departamento_id')
    try:
        with connectionBD() as conexion_MySQLdb:
            with conexion_MySQLdb.cursor(dictionary=True) as cursor:
                # Verifica si el departamento_id existe en la tabla departamento
                cursor.execute("SELECT id FROM departamento WHERE id = %s", (departamento_id,))
                if not cursor.fetchone():
                    return jsonify({"error": "El departamento_id no existe"}), 404

                # Obtiene los municipios asociados al departamento_id
                cursor.execute("SELECT id, nombre FROM municipio WHERE departamento_id = %s", (departamento_id,))
                municipios = cursor.fetchall()
                return jsonify(municipios)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@app.route('/mis-direcciones', methods=['GET'])
def mis_direcciones():
    if 'conectado' in session and session['rol'] == 'cliente':
        user_id = session.get('id')  # Obtener el ID del usuario desde la sesión
        try:
            with connectionBD() as conexion_MySQLdb:
                with conexion_MySQLdb.cursor(dictionary=True) as cursor:
                    # Consulta para obtener las direcciones del usuario
                    cursor.execute("""
                        SELECT d.id, d.nombre_completo, d.barrio, d.domicilio, d.referencias, d.telefono, 
                               dep.nombre AS departamento, mun.nombre AS municipio
                        FROM direccion d
                        JOIN departamento dep ON d.departamento_id = dep.id
                        JOIN municipio mun ON d.municipio_id = mun.id
                        WHERE d.users_id = %s
                    """, (user_id,))
                    direcciones = cursor.fetchall()

            # Renderizar la plantilla con las direcciones
            return render_template(
                'public/perfil/perfil_cliente.html',
                info_perfil_session=info_perfil_session(),
                direcciones=direcciones
            )
        except Exception as e:
            print(f"Error al obtener direcciones: {e}")
            flash('Error al obtener las direcciones.', 'error')
            return redirect(url_for('perfil_cliente'))
    else:
        flash('Debes iniciar sesión como cliente para ver tus direcciones.', 'error')
        return redirect(url_for('inicio'))
