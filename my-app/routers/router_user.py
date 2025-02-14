from app import app
from flask import render_template, request, flash, redirect, url_for, session, jsonify
from mysql.connector.errors import Error





# Importando conexión a BD
from controllers.funciones_user import *

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

    