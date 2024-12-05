from app import app
from flask import render_template, request, flash, redirect, url_for, session, jsonify
from mysql.connector.errors import Error

# Importando conexión a BD
from controllers.funciones_home import *

PATH_URL = "public/producto"

@app.route('/registrar-producto', methods=['GET'])
def viewFormProducto():
    if 'conectado' in session:
        return render_template('public/producto/registro_producto.html')
    else:
        flash('Primero debes iniciar sesión.', 'error')
        return redirect(url_for('inicio'))