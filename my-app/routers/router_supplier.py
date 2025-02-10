from app import app
from flask import render_template, request, flash, redirect, url_for, session
from controllers.funciones_supplier import procesar_proveedor  # Asegúrate de que esta función esté importada correctamente

PATH_URL = "public/proveedor"

@app.route('/registrar-proveedor', methods=['GET', 'POST'])
def viewFormProveedor():
    if 'conectado' in session:  # Verifica si el usuario está conectado
        if request.method == 'POST':  # Si es un POST, procesamos el formulario
            data_form = request.form  # Captura los datos del formulario
            resultado = procesar_proveedor(data_form)  # Procesa los datos del proveedor

            if isinstance(resultado, int) and resultado > 0:  # Si el registro fue exitoso
                flash('Proveedor registrado con éxito', 'success')
                return redirect(url_for('viewFormProveedor'))  # Redirige al formulario vacío
            else:  # Si hubo un error en el registro
                flash(f'Error al registrar proveedor: {resultado}', 'error')
        
        # Si es un GET, solo mostramos el formulario
        return render_template('public/proveedor/registro_proveedor.html')
    else:
        flash('Primero debes iniciar sesión.', 'error')
        return redirect(url_for('inicio'))  # Redirige a la página de inicio si no está conectado
