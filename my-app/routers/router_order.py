from app import app
from flask import render_template, request, flash, redirect, url_for, session,  jsonify
from mysql.connector.errors import Error


from mysql.connector import Error
from conexion.conexionBD import connectionBD
# Importando cenexión a BD
from controllers.funciones_order import *

PATH_URL = "public/pedido"



@app.route('/registrar-pedido', methods=['GET', 'POST'])
def viewFormPedido():
    if 'conectado' in session:  # Verifica si el usuario está conectado
        if request.method == 'POST':  # Si es un POST, procesamos el formulario
            data_form = request.form  # Captura los datos del formulario
            resultado = procesar_pedido(data_form)  # Procesa los datos del pedido

            if isinstance(resultado, int) and resultado > 0:  # Si el registro fue exitoso
                flash('Pedido registrado con éxito', 'success')
                return redirect(url_for('viewFormPedido'))  # Redirige al formulario vacío
            else:  # Si hubo un error en el registro
                flash(f'Error al registrar pedido: {resultado}', 'error')
                return redirect(url_for('viewFormPedido'))  # Redirige al formulario vacío

        # Si es un GET, obtener los datos de usuarios, productos, métodos de pago y entregas
        with connectionBD() as conexion_MySQLdb:
            with conexion_MySQLdb.cursor(dictionary=True) as cursor:
                # Obtener usuarios
                cursor.execute("SELECT id, nombre FROM users")
                usuarios = cursor.fetchall()

                # Obtener productos
                cursor.execute("SELECT id, nombre FROM producto")
                productos = cursor.fetchall()

                # Obtener métodos de pago (valores del ENUM)
                metodos_pago = obtener_metodos_pago(conexion_MySQLdb)

                # Obtener entregas
                cursor.execute("SELECT id, descripcion FROM entrega")  # Ajusta la consulta según tu tabla
                entregas = cursor.fetchall()

        # Pasar los datos a la plantilla
        return render_template(
            f'{PATH_URL}/registro_pedido.html',
            usuarios=usuarios,
            productos=productos,
            metodos_pago=metodos_pago,
            entregas=entregas  # Pasar las entregas a la plantilla
        )
    else:
        flash('Primero debes iniciar sesión.', 'error')
        return redirect(url_for('inicio'))