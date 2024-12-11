from app import app
from flask import render_template, request, flash, redirect, url_for, session
from controllers.funciones_product import procesar_producto  # Asegúrate de que esta función esté importada correctamente

PATH_URL = "public/producto"

@app.route('/registrar-producto', methods=['GET', 'POST'])
def viewFormProducto():
    if 'conectado' in session:  # Verifica si el usuario está conectado
        if request.method == 'POST':  # Si es un POST, procesamos el formulario
            data_form = request.form  # Captura los datos del formulario
            resultado = procesar_producto(data_form)  # Procesa los datos del producto

            if isinstance(resultado, int) and resultado > 0:  # Si el registro fue exitoso
                flash('Producto registrado con éxito', 'success')
                return redirect(url_for('viewFormProducto'))  # Redirige al formulario vacío
            else:  # Si hubo un error en el registro
                flash(f'Error al registrar producto: {resultado}', 'error')
        
        # Si es un GET, solo mostramos el formulario
        return render_template('public/producto/registro_producto.html')
    else:
        flash('Primero debes iniciar sesión.', 'error')
        return redirect(url_for('inicio'))  # Redirige a la página de inicio si no está conectado
