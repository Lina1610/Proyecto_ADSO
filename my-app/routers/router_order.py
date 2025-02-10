from app import app
from flask import render_template, request, flash, redirect, url_for, session,  jsonify
from mysql.connector.errors import Error


# Importando cenexión a BD
from controllers.funciones_home import *

PATH_URL = "public/pedido"


@app.route('/registrar-pedido', methods=['GET', 'POST'])
def viewFormPedido():
    if 'conectado' in session:
        if request.method == 'POST':
            data_form = request.form
            from controllers.funciones_order import procesar_pedido
            resultado = procesar_pedido(data_form)

            if "éxito" in resultado.lower():
                flash(resultado, 'success')
                return redirect(url_for('viewFormPedido'))  # Recargar el formulario
            else:
                flash(resultado, 'error')  # Mostrar mensaje de error al usuario

        return render_template(f'{PATH_URL}/registro_pedido.html')
    else:
        flash('Primero debes iniciar sesión.', 'error')
        return redirect(url_for('inicio'))
