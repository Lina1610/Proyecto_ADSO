from app import app
from flask import Flask, jsonify, request
from flask import render_template, request, flash, redirect, url_for, session, jsonify
from mysql.connector.errors import Error


# Importando conexión a BD
from controllers.funciones_address import * 
 
PATH_URL = "public/direccion"

# Función para registrar una dirección
@app.route('/registrar-direccion', methods=['GET', 'POST'])
def viewFormDireccion():
    if 'conectado' in session:  # Verifica si el usuario está conectado
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

                cursor.execute("SELECT id, nombre FROM municipio")
                municipios = cursor.fetchall()

                # Obtener usuarios
                cursor.execute("SELECT id, nombre FROM users")
                users = cursor.fetchall()

        # Pasar los datos a la plantilla
        return render_template(
            f'{PATH_URL}/registro_direccion.html',
            departamentos=departamentos,
            municipios=municipios,
            users=users
        )
    else:
        flash('Primero debes iniciar sesión.', 'error')
        return redirect(url_for('inicio'))

@app.route('/obtener_municipios', methods=['GET'])
def obtener_municipios():
    departamento_id = request.args.get('departamento_id')
    try:
        with connectionBD() as conexion_MySQLdb:
            with conexion_MySQLdb.cursor(dictionary=True) as cursor:
                # Verifica si el departamento_id existe en la tabla departamento
                cursor.execute("SELECT id FROM departamento WHERE id = %s", (departamento_id,))
                if not cursor.fetchone():
                    return jsonify({"error": "El departamento_id no existe"}), 404

                # Obtiene los municipios asociados al departamento_id
                cursor.execute("SELECT id, nombre FROM municipio WHERE departamento_id = %s", (departamento_id,))
                municipios = cursor.fetchall()
                return jsonify(municipios)
    except Exception as e:
        return jsonify({"error": str(e)}), 500