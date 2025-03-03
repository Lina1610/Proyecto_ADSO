from app import app
from flask import render_template, request, flash, redirect, url_for, session,  jsonify
from mysql.connector.errors import Error


from mysql.connector import Error
from conexion.conexionBD import connectionBD
# Importando cenexión a BD
from controllers.funciones_order import *

PATH_URL = "public/pedido"
from app import app
from flask import render_template, request, flash, redirect, url_for, session
from mysql.connector import Error
from conexion.conexionBD import connectionBD
from controllers.funciones_order import *

# Ruta para el formulario de registro de pedidos
@app.route('/registrar-pedido', methods=['GET', 'POST'])
def viewFormPedido():
    if 'conectado' in session:
        if request.method == 'POST':
            data_form = request.form
            resultado = procesar_pedido(data_form)

            if isinstance(resultado, int) and resultado > 0:
                flash('Pedido registrado con éxito', 'success')
                return redirect(url_for('viewFormPedido'))
            else:
                flash(f'Error al registrar pedido: {resultado}', 'error')
                return redirect(url_for('viewFormPedido'))

        with connectionBD() as conexion_MySQLdb:
            with conexion_MySQLdb.cursor(dictionary=True) as cursor:
                # Obtener usuarios
                cursor.execute("SELECT id, nombre FROM users")
                usuarios = cursor.fetchall()

                # Obtener productos
                cursor.execute("SELECT id, nombre FROM producto")
                productos = cursor.fetchall()

                # Obtener métodos de pago
                metodos_pago = obtener_metodos_pago(conexion_MySQLdb)

                # Obtener tipos de entrega
                tipos_entrega = obtener_tipos_entrega(conexion_MySQLdb)
                print("Tipos de entrega obtenidos:", tipos_entrega)  # Depuración

        return render_template(
            'public/pedido/registro_pedido.html',  # Asegúrate de que la ruta sea correcta
            usuarios=usuarios,
            productos=productos,
            metodos_pago=metodos_pago,
            tipos_entrega=tipos_entrega  # Pasar los tipos de entrega a la plantilla
        )
    else:
        flash('Primero debes iniciar sesión.', 'error')
        return redirect(url_for('inicio'))