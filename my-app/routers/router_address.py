from app import app
from flask import render_template, request, flash, redirect, url_for, session, jsonify
from mysql.connector.errors import Error

# Importando conexión a BD
from controllers.funciones_address import *

PATH_URL = "public/direccion"
@app.route('/registrar-direccion', methods=['GET', 'POST'])
def viewFormDireccion():
    if 'conectado' in session:  # Verifica si el usuario está conectado
        try:
            if request.method == 'POST':  # Si es un POST, procesamos el formulario
                data_form = request.form  # Captura los datos del formulario
                resultado = procesar_direccion(data_form)  # Procesa los datos de la dirección

                if isinstance(resultado, int) and resultado > 0:  # Si el registro fue exitoso
                    flash('Dirección registrada con éxito', 'success')
                    return redirect(url_for('viewFormDireccion'))  # Redirige al formulario vacío
                else:  # Si hubo un error en el registro
                    flash(f'Error al registrar dirección: {resultado}', 'error')

            # Si es un GET, obtener los datos de departamento y usuarios
            with connectionBD() as conexion_MySQLdb:
                with conexion_MySQLdb.cursor(dictionary=True) as cursor:
                    # Obtener departamentos
                    cursor.execute("SELECT id, nombre FROM departamento")
                    departamentos = cursor.fetchall()

                    # Obtener usuarios
                    cursor.execute("SELECT id, nombre FROM users")
                    users = cursor.fetchall()

            # Pasar los datos a la plantilla
            return render_template(
                f'{PATH_URL}/registro_direccion.html',
                departamentos=departamentos,
                users=users
            )

        except Exception as e:
            print(f"Error en viewFormDireccion: {e}")  # Debug
            flash('Ocurrió un error al cargar el formulario. Por favor, inténtalo de nuevo.', 'error')
            return redirect(url_for('inicio'))

    else:
        flash('Primero debes iniciar sesión.', 'error')
        return redirect(url_for('inicio'))
    
    