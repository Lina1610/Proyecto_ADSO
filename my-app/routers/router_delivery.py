from app import app
from flask import render_template, request, flash,jsonify, redirect, url_for, session
from mysql.connector.errors import Error
from controllers.funciones_delivery import *
from conexion.conexionBD import connectionBD

PATH_URL = "public/entrega"

@app.route('/registrar-entrega', methods=['GET', 'POST'])
def viewFormEntrega():
    if 'conectado' not in session:  # Si el usuario no está conectado
        flash('Primero debes iniciar sesión.', 'error')
        return redirect(url_for('inicio'))  # Redirige a la página de inicio

    if request.method == 'POST':  # Si es un POST, procesamos el formulario
        try:
            data_form = request.form  # Captura los datos del formulario
            resultado = procesar_entrega(data_form)  # Procesa los datos de la entrega

            if isinstance(resultado, int) and resultado > 0:  # Si el registro fue exitoso
                flash('Entrega registrada con éxito', 'success')
            else:  # Si hubo un error en el registro
                flash(f'Error al registrar entrega: {resultado}', 'error')
        except Exception as e:  # Captura cualquier excepción durante el procesamiento
            flash(f'Error inesperado: {str(e)}', 'error')

        return redirect(url_for('viewFormEntrega'))  # Redirige al formulario vacío

    # Si es un GET, solo mostramos el formulario
    try:
        with connectionBD() as conexion_MySQLdb:
            with conexion_MySQLdb.cursor(dictionary=True) as cursor:
                # Obtener las direcciones del usuario
                cursor.execute("""
                    SELECT 
                        d.id, 
                        d.nombre_completo, 
                        CONCAT_WS(', ', d.domicilio, d.barrio, d.referencias) AS direccion_completa,
                        m.nombre AS municipio,
                        dp.nombre AS departamento
                    FROM 
                        direccion d
                    JOIN 
                        municipio m ON d.municipio_id = m.id
                    JOIN 
                        departamento dp ON d.departamento_id = dp.id
                    WHERE 
                        d.estado = 'Activo'
                """)
                direcciones = cursor.fetchall()  # Obtiene todas las direcciones activas
    except Error as e:  # Captura errores de la base de datos
        flash(f'Error al cargar direcciones: {str(e)}', 'error')
        direcciones = []  # Si hay un error, devuelve una lista vacía

    return render_template(
        f'{PATH_URL}/registro_entrega.html',
        direcciones=direcciones
    )

@app.route('/guardar-pedido', methods=['POST'])
def guardar_pedido():
    if 'conectado' not in session:  # Si el usuario no está conectado
        return jsonify({"status": "error", "mensaje": "Debes iniciar sesión para realizar esta acción."})

    try:
        data = request.get_json()  # Obtener los datos del pedido
        metodo_pago_id = data.get('metodo_pago_id')
        tipo_entrega = data.get('tipo_entrega')
        direccion_id = data.get('direccion_id')
        users_id = session.get('users_id')  # Obtener el ID del usuario desde la sesión
        total = data.get('total')  # Total del pedido

        # Validar los datos
        if not metodo_pago_id or not tipo_entrega or not users_id or not total:
            return jsonify({"status": "error", "mensaje": "Faltan datos obligatorios."})

        if tipo_entrega == 'Domicilio' and not direccion_id:
            return jsonify({"status": "error", "mensaje": "Debes seleccionar una dirección para entrega a domicilio."})

        # Crear la entrega
        entrega_id = procesar_entrega(tipo_entrega, direccion_id)
        if isinstance(entrega_id, str):  # Si hay un error
            return jsonify({"status": "error", "mensaje": entrega_id})

        # Crear el pedido
        pedido_id = crear_pedido(users_id, metodo_pago_id, entrega_id, total)
        if isinstance(pedido_id, str):  # Si hay un error
            return jsonify({"status": "error", "mensaje": pedido_id})

        return jsonify({"status": "success", "mensaje": "Pedido registrado con éxito.", "pedido_id": pedido_id})

    except Exception as e:
        return jsonify({"status": "error", "mensaje": f"Error al registrar el pedido: {str(e)}"})
    

def crear_pedido(users_id, metodo_pago_id, entrega_id, total):
    """Crea un registro en la tabla 'pedido'."""
    try:
        with connectionBD() as conexion_MySQLdb:
            with conexion_MySQLdb.cursor(dictionary=True) as cursor:
                sql = """
                    INSERT INTO pedido (
                        fecha, estado, total, entrega_id, users_id, metodo_pago_id
                    ) VALUES (NOW(), %s, %s, %s, %s, %s)
                """
                valores = (
                    'Pendiente',  # Estado por defecto
                    total,
                    entrega_id,
                    users_id,
                    metodo_pago_id
                )
                cursor.execute(sql, valores)
                conexion_MySQLdb.commit()
                return cursor.lastrowid  # Devuelve el ID del pedido creado
    except Exception as e:
        return f"Error al crear el pedido: {str(e)}"