from app import app
from flask import render_template, request, flash, redirect, url_for, session, jsonify
from mysql.connector.errors import Error
from conexion.conexionBD import connectionBD

# Importando conexión a BD
from controllers.funciones_invoice import *

PATH_URL = "public/factura"
@app.route('/registrar-factura', methods=['GET', 'POST'])
def viewFormFactura():
    if 'conectado' in session:
        if request.method == 'POST':
            # Obtener los datos del formulario
            dataForm = {
                'estado': request.form.get('estado'),
                'pedido_id': request.form.get('pedido_id'),
                'users_id': request.form.get('users_id')  # Obtener el users_id del campo oculto
            }

            # Procesar la factura
            resultado = procesar_factura(dataForm)

            # Manejar el resultado
            if isinstance(resultado, int) and resultado > 0:
                flash('Factura registrada correctamente.', 'success')
            else:
                flash(resultado, 'error')  # Mostrar mensaje de error

            return redirect(url_for('registrar_factura'))

        # Si es GET, mostrar el formulario con los datos necesarios
        with connectionBD() as conexion_MySQLdb:
            with conexion_MySQLdb.cursor(dictionary=True) as cursor:
                # Obtener la lista de pedidos con el nombre del usuario asociado y el users_id
                cursor.execute("""
                    SELECT p.id AS pedido_id, u.nombre AS nombre_usuario, p.users_id
                    FROM pedido p
                    JOIN users u ON p.users_id = u.id
                """)
                pedidos = cursor.fetchall()

        return render_template(
            'public/factura/registro_factura.html',  # Ruta corregida
            pedidos=pedidos
        )
    else:
        flash('Primero debes iniciar sesión.', 'error')
        return redirect(url_for('inicio'))