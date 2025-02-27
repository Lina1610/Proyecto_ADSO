from app import app
from flask import render_template, request, flash, redirect, url_for, session
from controllers.funciones_product import procesar_producto  # Asegúrate de que esta función esté importada correctamente
from controllers.funciones_product import obtener_productos
from controllers.funciones_product import obtener_producto_por_id
from controllers.funciones_product import actualizar_producto 
from controllers.funciones_product import eliminar_producto
from controllers.funciones_product import buscarProductoBD
from flask import jsonify

PATH_URL = "public/producto"

# funcion para registrar un producto
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


# funcion para poder vcer los detalles del producto
@app.route('/detalles-producto/<int:id>')
def detalles_producto(id):
    if 'conectado' in session:
        producto = obtener_producto_por_id(id)  # Obtener el producto por su ID
        if producto:
            return render_template('public/producto/detalles_producto.html', producto=producto)
        else:
            flash('Producto no encontrado', 'error')
            return redirect(url_for('lista_productos'))
    else:
        flash('Primero debes iniciar sesión.', 'error')
        return redirect(url_for('inicio'))
    
# funcio para poder eliminar los productos
@app.route('/eliminar-producto/<int:id>', methods=['DELETE'])
def eliminar_producto_route(id):
    if 'conectado' in session:
        resultado = eliminar_producto(id)
        if resultado and resultado > 0:
            return {'success': True, 'message': 'Producto eliminado correctamente'}
        return {'success': False, 'message': 'Error al eliminar producto'}
    return {'success': False, 'message': 'Usuario no autenticado'}, 401

@app.route("/buscando-producto", methods=['POST'])
def viewBuscarProductoBD():
    try:
        search_query = request.json.get('busqueda')  # Obtener el término de búsqueda desde el JSON
        if not search_query:
            return jsonify({'error': 'No search query provided'}), 400

        resultadoBusqueda = buscarProductoBD(search_query)  # Buscar productos en la base de datos

        if resultadoBusqueda:
            # Si hay resultados, generar el HTML de la tabla
            html_resultados = ""
            for producto in resultadoBusqueda:
                html_resultados += f"""
                <tr id="producto_{producto['id']}">
                    <td>{producto['id']}</td>
                    <td>{producto['codigo']}</td>
                    <td>{producto['nombre']}</td>
                    <td>{producto['descripcion']}</td>
                    <td>$ {producto['precio']:,.2f}</td>
                    <td>{producto['cantidad']}</td>
                    <td width="10px">
                        <a href="/detalles-producto/{producto['id']}" class="btn btn-info btn-sm" title="Ver detalles">
                            <i class="bi bi-eye"></i> Ver detalles
                        </a>
                        <a href="/editar-producto/{producto['id']}" class="btn btn-success btn-sm" title="Actualizar">
                            <i class="bi bi-arrow-clockwise"></i> Actualizar
                        </a>
                        <a href="#" onclick="eliminarProducto('{producto['id']}');" class="btn btn-danger btn-sm" title="Eliminar">
                            <i class="bi bi-trash3"></i> Eliminar
                        </a>
                    </td>
                </tr>
                """
            return jsonify({'success': True, 'html': html_resultados})
        else:
            # Si no hay resultados, devolver un mensaje en HTML
            mensaje_html = f"""
            <tr>
                <td colspan="7" style="text-align:center;color: red;font-weight: bold;">
                    No resultados para la búsqueda: <strong style="color: #222;">{search_query}</strong>
                </td>
            </tr>
            """
            return jsonify({'success': False, 'html': mensaje_html})

    except Exception as e:
        print(f"Error en viewBuscarProductoBD: {e}")  # Log de depuración
        return jsonify({'error': str(e)}), 500  # Manejo de errores