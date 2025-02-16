from app import app
from flask import render_template, request, flash, redirect, url_for, session, jsonify
from mysql.connector.errors import Error
from controllers.funciones_user import lista_usuariosBD
from controllers.funciones_user import obtener_usuario_por_id
from conexion.conexionBD import connectionBD
from controllers.funciones_user import buscarUsuarioBD
from controllers.funciones_user import eliminar_usuario
from controllers.funciones_user import procesar_usuario







PATH_URL = "public/usuario"


@app.route('/registrar-usuario', methods=['GET', 'POST'])
def viewFormUsuario():
    if 'conectado' in session:
        if request.method == 'POST':
            data_form = request.form  # Captura los datos del formulario
            resultado = procesar_usuario(data_form)  # Procesa los datos del usuario

            if isinstance(resultado, int) and resultado > 0:  # Si el registro fue exitoso
                flash('Usuario registrado con éxito', 'success')
                return redirect(url_for('viewFormUsuario'))  # Redirige al formulario vacío
            else:  # Si hubo un error en el registro
                flash(f'Error al registrar usuario: {resultado}', 'error')
        
        return render_template('public/nuevosUsuarios/registro_usuario.html')
    else:
        flash('Primero debes iniciar sesión.', 'error')
        return redirect(url_for('inicio'))

# En router_user.py
@app.route('/lista-de-usuarios')
def lista_usuarios():
    if 'conectado' in session:
        usuarios = lista_usuariosBD()  # Obtener la lista de usuarios desde la BD
        print("Usuarios obtenidos en la ruta:", usuarios)  # Depuración
        return render_template('public/nuevosUsuarios/lista_usuarios.html', resp_usuariosBD=usuarios)
    else:
        flash('Primero debes iniciar sesión.', 'error')
        return redirect(url_for('inicio'))

@app.route("/editar-usuario/<int:id>", methods=['GET'])
def viewEditarUsuario(id):
    if 'conectado' in session:
        usuario = obtener_usuario_por_id(id)  # Función para obtener los detalles del usuario
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
        usuario = obtener_usuario_por_id(id)  # Función para obtener los detalles del usuario
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
                    SET 
                        nombre = %s,
                        apellido = %s,
                        tipo_documento = %s,
                        documento = %s,
                        correo = %s,
                        telefono = %s,
                        rol = %s,
                        estado = %s
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
        resultado = eliminar_usuario(id)  # Llama a la función para eliminar el usuario
        if resultado:
            flash('Felicitaciones, El Usuario fue eliminado correctamente 😁', 'success')
            return jsonify({"success": True})
        else:
            flash('Error al eliminar el usuario', 'error')
            return jsonify({"success": False})
    else:
        flash('Primero debes iniciar sesión', 'error')
        return jsonify({"success": False})