from app import app
from flask import render_template, request, flash, redirect, url_for, session, jsonify
from mysql.connector.errors import Error

# Importando conexión a BD

# Importando cenexión a BD
from controllers.funciones_inventory import *


PATH_URL = "public/inventario"  # Ruta base para las plantillas de inventario

@app.route('/registrar-inventario', methods=['GET', 'POST'])
def viewFormInventario():
    if 'conectado' in session:  # Verifica si el usuario está conectado
        if request.method == 'POST':
            # Obtener los datos del formulario
            data_form = {
                'cantidad_disponible': request.form.get('cantidad_disponible'),
                'fecha_actualizacion': request.form.get('fecha_actualizacion')
            }

            # Llamar a la función externa para procesar el inventario
            resultado = procesar_inventario(data_form)

            if "éxito" in resultado.lower():
                flash(resultado, 'success')
            else:
                flash(resultado, 'error')  # Mostrar mensaje de error al usuario

            return redirect(url_for('viewFormInventario'))  # Recargar el formulario

        # Si es una solicitud GET, mostrar el formulario
        return render_template(f'{PATH_URL}/registro_inventario.html')

    else:
        flash('Primero debes iniciar sesión.', 'error')
        return redirect(url_for('inicio'))  # Redirige al inicio si no está conectado