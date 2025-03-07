from app import app
from flask import render_template, request, flash, redirect, url_for, session
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
                # Nueva consulta SQL con JOIN
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
                print(direcciones)  # Depuración: Verifica los datos obtenidos
    except Error as e:  # Captura errores de la base de datos
        flash(f'Error al cargar direcciones: {str(e)}', 'error')
        direcciones = []  # Si hay un error, devuelve una lista vacía

    return render_template(
        f'{PATH_URL}/registro_entrega.html',
        direcciones=direcciones
    )
