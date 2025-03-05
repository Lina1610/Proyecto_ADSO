from app import app
from flask import render_template, request, flash, redirect, url_for, session, jsonify
from mysql.connector.errors import Error

# Importando conexión a BD

# Importando cenexión a BD
from controllers.funciones_stock import *


PATH_URL = "public/stock"  
# Ruta base para las plantillas de inventario
@app.route ('/registrar-stock', methods=['GET', 'POST'])
def viewFormStock():
    if 'conectado' in session:
        if request.method == 'POST':
            dataForm = {
                'cantidad_disponible': request.form.get('cantidad_disponible'),
                'producto_id': request.form.get('producto_id'),
                'users_id': request.form.get('users_id')
            }

            resultado = procesar_stock(dataForm)

            if isinstance(resultado, int) and resultado > 0:
                flash('Stock registrado correctamente.', 'success')
            else:
                flash(resultado, 'error')

            return redirect(url_for('viewFormStock'))

        with connectionBD() as conexion_MySQLdb:
            with conexion_MySQLdb.cursor(dictionary=True) as cursor:
                cursor.execute("SELECT id, nombre FROM producto")
                productos = cursor.fetchall()

                cursor.execute("SELECT id, nombre FROM users WHERE rol != 'cliente'")
                usuarios = cursor.fetchall()

        return render_template('public/stock/registro_stock.html', productos=productos, usuarios=usuarios)
    else:
        flash('Primero debes iniciar sesión.', 'error')
        return redirect(url_for('inicio'))