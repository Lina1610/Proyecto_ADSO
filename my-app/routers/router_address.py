from app import app
from flask import render_template, request, flash, redirect, url_for, session, jsonify
from conexion.conexionBD import connectionBD
from controllers.funciones_address import obtener_direccion_por_id
from controllers.funciones_address import (
    obtener_direcciones_usuario,
    procesar_direccion,
    validar_claves_foraneas,
    obtener_direccion
)
from controllers.funciones_login import info_perfil_session  # Importar la función necesaria

PATH_URL = "public/direccion"

# Ruta para mostrar las direcciones del cliente
@app.route('/cliente-direcciones', methods=['GET'])
def cliente_direcciones():
    if 'conectado' in session and session['rol'] == 'cliente':
        user_id = session.get('id')

        # Obtener las direcciones del cliente
        direcciones = obtener_direcciones_usuario(user_id)

        # Obtener departamentos y municipios para el formulario
        with connectionBD() as conexion_MySQLdb:
            with conexion_MySQLdb.cursor(dictionary=True) as cursor:
                cursor.execute("SELECT id, nombre FROM departamento")
                departamentos = cursor.fetchall()

                cursor.execute("SELECT id, nombre FROM municipio")
                municipios = cursor.fetchall()

        return render_template(
            'public/perfil/perfil_cliente.html',
            info_perfil_session=info_perfil_session(),  # Usar la función importada
            departamentos=departamentos,
            municipios=municipios,
            direcciones=direcciones
        )
    else:
        flash('Acceso denegado.', 'error')
        return redirect(url_for('inicio'))

# Ruta para registrar una dirección
@app.route('/registrar-direccion', methods=['GET', 'POST'])
def viewFormDireccion():
    if session.get('conectado'):
        rol_usuario = session.get('rol', '')
        
        if request.method == 'POST':
            data_form = request.form
            resultado = procesar_direccion(data_form)

            if isinstance(resultado, int) and resultado > 0:
                flash('Dirección registrada con éxito', 'success')
                return redirect(url_for('cliente_direcciones'))
            else:
                flash(f'Error al registrar dirección: {resultado}', 'error')
                return redirect(url_for('cliente_direcciones'))

        # Obtener datos de departamento, municipios y usuarios
        with connectionBD() as conexion_MySQLdb:
            with conexion_MySQLdb.cursor(dictionary=True) as cursor:
                cursor.execute("SELECT id, nombre FROM departamento")
                departamentos = cursor.fetchall()

                cursor.execute("SELECT id, nombre FROM municipio")
                municipios = cursor.fetchall()

                cursor.execute("SELECT id, nombre FROM users")
                users = cursor.fetchall()

        return render_template(
            f'{PATH_URL}/registro_direccion.html',
            departamentos=departamentos,
            municipios=municipios,
            users=users
        )
    else:
        flash('Primero debes iniciar sesión.', 'error')
        return redirect(url_for('inicio'))

# Ruta para obtener municipios según departamento
@app.route('/obtener_municipios', methods=['GET'])
def obtener_municipios():
    departamento_id = request.args.get('departamento_id')
    if not departamento_id or not departamento_id.isdigit():
        return jsonify({"error": "ID de departamento inválido"}), 400
    
    try:
        with connectionBD() as conexion_MySQLdb:
            with conexion_MySQLdb.cursor(dictionary=True) as cursor:
                cursor.execute("SELECT id FROM departamento WHERE id = %s", (int(departamento_id),))
                if cursor.fetchone() is None:
                    return jsonify([])  # Devuelve lista vacía si no hay municipios
                
                cursor.execute("SELECT id, nombre FROM municipio WHERE departamento_id = %s", (int(departamento_id),))
                municipios = cursor.fetchall()
                return jsonify(municipios)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Ruta para listar direcciones
@app.route('/lista-de-direccion')
def lista_direcciones():
    if session.get('conectado'):
        try:
            direcciones = obtener_direccion() or []  # Asegurar que no sea None
            print("Datos de direcciones obtenidos:", direcciones)  # Depuración
            return render_template('public/direccion/lista_direccion.html', direcciones=direcciones)
        except Exception as e:
            print(f"Error al obtener las direcciones: {e}")
            flash('Error al obtener las direcciones. Por favor, inténtalo de nuevo.', 'error')
            return redirect(url_for('inicio'))
    else:
        flash('Primero debes iniciar sesión.', 'error')
        return redirect(url_for('inicio'))
    
@app.route('/editar-direccion/<int:id>', methods=['GET', 'POST'])
def viewEditarDireccion(id):
    # Lógica para editar la dirección
    pass


@app.route('/detalles-direccion/<int:id>')
def detalles_direccion(id):
    # Obtener la dirección por su ID
    direccion = obtener_direccion_por_id(id)
    
    # Si la dirección no existe, pasar una lista vacía
    if not direccion:
        print("No se encontró la dirección.")  # Depuración
        return render_template('public/direccion/detalles_direccion.html', direccion=[])
    
    print(f"Datos de la dirección: {direccion}")  # Depuración
    return render_template('public/direccion/detalles_direccion.html', direccion=direccion)