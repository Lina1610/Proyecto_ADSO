
from app import app
from flask import render_template, request, flash, redirect, url_for, session, jsonify
from mysql.connector.errors import Error

# Importando conexión a BD
from controllers.funciones_home import *

PATH_URL = "public/abono"

@app.route('/registrar-abono', methods=['GET'])
def viewFormAbono():
    if 'conectado' in session:
        return render_template('public/abono/registro_abono.html')
    else:
        flash('Primero debes iniciar sesión.', 'error')
        return redirect(url_for('inicio'))

