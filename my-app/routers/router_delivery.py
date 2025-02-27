from app import app
from flask import render_template, request, flash, redirect, url_for, session,  jsonify
from mysql.connector.errors import Error
from controllers.funciones_home import lista_usuariosBD 

# Importando cenexión a BD
from controllers.funciones_delivery import *

PATH_URL = "public/entrega"


# Función para registrar una entrega (delivery)
@app.route('/registrar-entrega', methods=['GET', 'POST'])
def viewFormEntrega():
    if 'conectado' in session:  # Verifica si el usuario está conectado
        if request.method == 'POST':  # Si es un POST, procesamos el formulario
            data_form = request.form  # Captura los datos del formulario
            resultado = procesar_entrega(data_form)  # Procesa los datos de la entrega

            if isinstance(resultado, int) and resultado > 0:  # Si el registro fue exitoso
                flash('Entrega registrada con éxito', 'success')
                return redirect(url_for('viewFormEntrega'))  # Redirige al formulario vacío
            else:  # Si hubo un error en el registro
                flash(f'Error al registrar entrega: {resultado}', 'error')
        
        # Si es un GET, solo mostramos el formulario
        return render_template(f'{PATH_URL}/registro_entrega.html')
    else:
        flash('Primero debes iniciar sesión.', 'error')
        return redirect(url_for('inicio'))  # Redirige a la página de inicio si no está conectado