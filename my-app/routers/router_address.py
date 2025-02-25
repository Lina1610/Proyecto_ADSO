from app import app
from flask import jsonify
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
                if session['rol'] == 'cliente':  # Si el usuario es un cliente
                    return redirect(url_for('perfil_cliente'))  # Redirige al perfil del cliente
                else:  # Si el usuario es administrador o empleado
                    return redirect(url_for('viewFormDireccion'))  # Redirige al formulario vacío
            else:  # Si hubo un error en el registro
                flash(f'Error al registrar dirección: {resultado}', 'error')
                if session['rol'] == 'cliente':  # Si el usuario es un cliente
                    return redirect(url_for('perfil_cliente'))  # Redirige al perfil del cliente
                else:  # Si el usuario es administrador o empleado
                    return redirect(url_for('viewFormDireccion'))  # Redirige al formulario vacío
        
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
    

# lista direcciones
@app.route('/lista-de-direccion')
def lista_direcciones():
    if 'conectado' in session:  # Verifica si el usuario está conectado
        try:
            # Obtener la lista de direcciones desde la base de datos
            direcciones = obtener_direccion()
            
            # Depuración: Verifica los datos obtenidos
            print(direcciones)
            
            # Renderizar la plantilla con los datos de las direcciones
            return render_template('public/direccion/lista_direccion.html', direcciones=direcciones)
        except Exception as e:
            # Manejo de errores: Si ocurre un error, muestra un mensaje y redirige al inicio
            print(f"Error al obtener las direcciones: {e}")
            flash('Error al obtener las direcciones. Por favor, inténtalo de nuevo.', 'error')
            return redirect(url_for('inicio'))
    else:
        # Si el usuario no está conectado, muestra un mensaje y redirige al inicio
        flash('Primero debes iniciar sesión.', 'error')
        return redirect(url_for('inicio'))
    


