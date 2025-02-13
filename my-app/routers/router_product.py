from app import app
from flask import render_template, request, flash, redirect, url_for, session
from controllers.funciones_product import procesar_producto  # Asegúrate de que esta función esté importada correctamente
from controllers.funciones_product import obtener_productos
from controllers.funciones_product import obtener_producto_por_id
from controllers.funciones_product import actualizar_producto

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


# lista productos
@app.route('/lista-de-productos')
def lista_productos():
    if 'conectado' in session:
        productos = obtener_productos()
        return render_template('public/producto/lista_productos.html', productos=productos)
    else:
        flash('Primero debes iniciar sesión.', 'error')
        return redirect(url_for('inicio'))

#editar producto

@app.route('/editar-producto/<int:id>', methods=['GET', 'POST'])
def viewEditarProducto(id):
    if 'conectado' in session:
        if request.method == 'GET':
            # Obtener los datos del producto por su ID
            producto = obtener_producto_por_id(id)
            if producto:
                return render_template('public/producto/editar_producto.html', producto=producto)
            else:
                flash('Producto no encontrado', 'error')
                return redirect(url_for('lista_productos'))
        elif request.method == 'POST':
            # Procesar la actualización del producto
            data_form = request.form
            resultado = actualizar_producto(id, data_form)
            if resultado:
                flash('Producto actualizado correctamente', 'success')
            else:
                flash('Error al actualizar el producto', 'error')
            return redirect(url_for('lista_productos'))
    else:
        flash('Primero debes iniciar sesión.', 'error')
        return redirect(url_for('inicio'))