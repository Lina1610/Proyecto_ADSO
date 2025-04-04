from app import app
from flask import render_template, request, flash, redirect, url_for, session
from controllers.funciones_product import procesar_producto, obtener_productos, obtener_producto_por_id, actualizar_producto, eliminar_producto, buscarProductoBD, obtener_todos_los_productos, codigo_existe
from flask import jsonify
import re

PATH_URL = "public/producto"

# Ruta para registrar un nuevo producto
@app.route('/registrar-producto', methods=['GET', 'POST'])
def viewFormProducto():
    if 'conectado' not in session:
        flash('Primero debes iniciar sesión.', 'error')
        return redirect(url_for('inicio'))

    if request.method == 'POST':
        data_form = request.form
        imagen = request.files.get('imagen')

        data_form_dict = {
            'codigo': data_form.get('codigo', '').strip(),
            'nombre': data_form.get('nombre', '').strip(),
            'descripcion': data_form.get('descripcion', '').strip(),
            'estado': data_form.get('estado', '').strip(),
            'precio': data_form.get('precio', ''),
            'cantidad': data_form.get('cantidad', ''),
            'total': data_form.get('total', ''),
            'imagen': imagen
        }

        # Validaciones manuales
        # 1. Validar que el código sea obligatorio, solo contenga números y no exceda 10 caracteres
        if not data_form_dict['codigo']:
            flash('El código es obligatorio.', 'error')
            return render_template('public/producto/registro_producto.html', data_form=data_form_dict)
        if not re.match(r'^\d+$', data_form_dict['codigo']):
            flash('El código solo debe contener números.', 'error')
            return render_template('public/producto/registro_producto.html', data_form=data_form_dict)
        if len(data_form_dict['codigo']) > 10:
            flash('El código no puede exceder 10 caracteres.', 'error')
            data_form_dict['codigo'] = data_form_dict['codigo'][:10]
            return render_template('public/producto/registro_producto.html', data_form=data_form_dict)

        # 2. Validar que el nombre sea obligatorio y no exceda 100 caracteres
        if not data_form_dict['nombre']:
            flash('El nombre es obligatorio.', 'error')
            return render_template('public/producto/registro_producto.html', data_form=data_form_dict)
        if len(data_form_dict['nombre']) > 100:
            flash('El nombre no puede exceder 100 caracteres.', 'error')
            data_form_dict['nombre'] = data_form_dict['nombre'][:100]
            return render_template('public/producto/registro_producto.html', data_form=data_form_dict)

        # 3. Validar que la descripción sea obligatoria y no exceda 100 caracteres
        if not data_form_dict['descripcion']:
            flash('La descripción es obligatoria.', 'error')
            return render_template('public/producto/registro_producto.html', data_form=data_form_dict)
        if len(data_form_dict['descripcion']) > 100:
            flash('La descripción no puede exceder 100 caracteres.', 'error')
            data_form_dict['descripcion'] = data_form_dict['descripcion'][:100]
            return render_template('public/producto/registro_producto.html', data_form=data_form_dict)

        # 4. Validar que el precio sea obligatorio, numérico y mayor a 0
        if not data_form_dict['precio']:
            flash('El precio es obligatorio.', 'error')
            return render_template('public/producto/registro_producto.html', data_form=data_form_dict)
        try:
            precio = float(data_form_dict['precio'])
            if precio <= 0:
                flash('El precio debe ser mayor a 0.', 'error')
                return render_template('public/producto/registro_producto.html', data_form=data_form_dict)
            data_form_dict['precio'] = precio
        except (ValueError, TypeError):
            flash('El precio debe ser un número válido (solo números y punto decimal).', 'error')
            return render_template('public/producto/registro_producto.html', data_form=data_form_dict)

        # 5. Validar que la cantidad sea obligatoria, numérica y mayor a 0
        if not data_form_dict['cantidad']:
            flash('La cantidad es obligatoria.', 'error')
            return render_template('public/producto/registro_producto.html', data_form=data_form_dict)
        try:
            cantidad = int(data_form_dict['cantidad'])
            if cantidad <= 0:
                flash('La cantidad debe ser mayor a 0.', 'error')
                return render_template('public/producto/registro_producto.html', data_form=data_form_dict)
            data_form_dict['cantidad'] = cantidad
        except (ValueError, TypeError):
            flash('La cantidad debe ser un número entero válido (solo números).', 'error')
            return render_template('public/producto/registro_producto.html', data_form=data_form_dict)

        # 6. Validar que el total sea obligatorio, numérico y mayor a 0
        if not data_form_dict['total']:
            flash('El total es obligatorio.', 'error')
            return render_template('public/producto/registro_producto.html', data_form=data_form_dict)
        try:
            total = float(data_form_dict['total'])
            if total <= 0:
                flash('El total debe ser mayor a 0.', 'error')
                return render_template('public/producto/registro_producto.html', data_form=data_form_dict)
            data_form_dict['total'] = total
        except (ValueError, TypeError):
            flash('El total debe ser un número válido (solo números y punto decimal).', 'error')
            return render_template('public/producto/registro_producto.html', data_form=data_form_dict)

        # 7. Validar que el estado sea obligatorio y solo permita "Disponible" o "No disponible"
        if data_form_dict['estado'] not in ['Disponible', 'No disponible']:
            flash('El estado es obligatorio y debe ser "Disponible" o "No disponible".', 'error')
            return render_template('public/producto/registro_producto.html', data_form=data_form_dict)

        # 8. Validar la imagen (opcional, pero si se sube, debe ser jpg, png o jpeg)
        if imagen and imagen.filename:
            allowed_extensions = {'jpg', 'png', 'jpeg'}
            extension = imagen.filename.rsplit('.', 1)[1].lower() if '.' in imagen.filename else ''
            if extension not in allowed_extensions:
                flash('La imagen debe ser en formato jpg, png o jpeg.', 'error')
                return render_template('public/producto/registro_producto.html', data_form=data_form_dict)

        # Nueva validación: Verificar si el código ya existe
        if codigo_existe(data_form_dict['codigo']):
            flash('El código ya existe. Por favor, usa un código diferente.', 'error')
            return render_template('public/producto/registro_producto.html', data_form=data_form_dict)

        # Si todas las validaciones pasan, procesamos el producto
        resultado = procesar_producto(data_form_dict, imagen)
        if isinstance(resultado, int) and resultado > 0:
            flash('Producto registrado con éxito', 'success')
            return redirect(url_for('viewFormProducto'))
        else:
            flash(f'Error al registrar producto: {resultado}', 'error')
            return render_template('public/producto/registro_producto.html', data_form=data_form_dict)

    return render_template('public/producto/registro_producto.html', data_form={})

# Ruta para listar todos los productos
@app.route('/lista-de-productos')
def lista_productos():
    if 'conectado' in session:
        productos = obtener_todos_los_productos()
        return render_template('public/producto/lista_productos.html', productos=productos)
    else:
        flash('Primero debes iniciar sesión.', 'error')
        return redirect(url_for('inicio'))

# Ruta para editar un producto existente
@app.route('/editar-producto/<int:id>', methods=['GET', 'POST'])
def viewEditarProducto(id):
    if 'conectado' not in session:
        flash('Primero debes iniciar sesión.', 'error')
        return redirect(url_for('inicio'))

    producto = obtener_producto_por_id(id)
    if not producto:
        flash('Producto no encontrado', 'error')
        return redirect(url_for('lista_productos'))

    if request.method == 'POST':
        data_form = request.form
        imagen = request.files.get('imagen')

        data_form_dict = {
            'codigo': data_form.get('codigo', '').strip(),
            'nombre': data_form.get('nombre', '').strip(),
            'descripcion': data_form.get('descripcion', '').strip(),
            'estado': data_form.get('estado', '').strip(),
            'precio': data_form.get('precio', ''),
            'cantidad': data_form.get('cantidad', ''),
            'total': data_form.get('total', '')
        }

        # Validaciones manuales
        if not data_form_dict['codigo']:
            flash('El código es obligatorio.', 'error')
            return render_template('public/producto/editar_producto.html', producto=producto, data_form=data_form_dict)
        if not re.match(r'^\d+$', data_form_dict['codigo']):
            flash('El código solo debe contener números.', 'error')
            return render_template('public/producto/editar_producto.html', producto=producto, data_form=data_form_dict)
        if len(data_form_dict['codigo']) > 10:
            flash('El código no puede exceder 10 caracteres.', 'error')
            data_form_dict['codigo'] = data_form_dict['codigo'][:10]
            return render_template('public/producto/editar_producto.html', producto=producto, data_form=data_form_dict)

        if not data_form_dict['nombre']:
            flash('El nombre es obligatorio.', 'error')
            return render_template('public/producto/editar_producto.html', producto=producto, data_form=data_form_dict)
        if len(data_form_dict['nombre']) > 100:
            flash('El nombre no puede exceder 100 caracteres.', 'error')
            data_form_dict['nombre'] = data_form_dict['nombre'][:100]
            return render_template('public/producto/editar_producto.html', producto=producto, data_form=data_form_dict)

        if not data_form_dict['descripcion']:
            flash('La descripción es obligatoria.', 'error')
            return render_template('public/producto/editar_producto.html', producto=producto, data_form=data_form_dict)
        if len(data_form_dict['descripcion']) > 100:
            flash('La descripción no puede exceder 100 caracteres.', 'error')
            data_form_dict['descripcion'] = data_form_dict['descripcion'][:100]
            return render_template('public/producto/editar_producto.html', producto=producto, data_form=data_form_dict)

        try:
            precio = float(data_form_dict['precio'])
            if precio <= 0:
                flash('El precio debe ser mayor a 0.', 'error')
                return render_template('public/producto/editar_producto.html', producto=producto, data_form=data_form_dict)
            data_form_dict['precio'] = precio
        except (ValueError, TypeError):
            flash('El precio debe ser un número válido.', 'error')
            return render_template('public/producto/editar_producto.html', producto=producto, data_form=data_form_dict)

        try:
            cantidad = int(data_form_dict['cantidad'])
            if cantidad <= 0:
                flash('La cantidad debe ser mayor a 0.', 'error')
                return render_template('public/producto/editar_producto.html', producto=producto, data_form=data_form_dict)
            data_form_dict['cantidad'] = cantidad
        except (ValueError, TypeError):
            flash('La cantidad debe ser un número entero válido.', 'error')
            return render_template('public/producto/editar_producto.html', producto=producto, data_form=data_form_dict)

        try:
            total = float(data_form_dict['total'])
            if total <= 0:
                flash('El total debe ser mayor a 0.', 'error')
                return render_template('public/producto/editar_producto.html', producto=producto, data_form=data_form_dict)
            data_form_dict['total'] = total
        except (ValueError, TypeError):
            flash('El total debe ser un número válido.', 'error')
            return render_template('public/producto/editar_producto.html', producto=producto, data_form=data_form_dict)

        if data_form_dict['estado'] not in ['Disponible', 'No disponible']:
            flash('El estado debe ser "Disponible" o "No disponible".', 'error')
            return render_template('public/producto/editar_producto.html', producto=producto, data_form=data_form_dict)

        # Validar imagen si se sube
        if imagen and imagen.filename:
            allowed_extensions = {'jpg', 'png', 'jpeg'}
            extension = imagen.filename.rsplit('.', 1)[1].lower() if '.' in imagen.filename else ''
            if extension not in allowed_extensions:
                flash('La imagen debe ser en formato jpg, png o jpeg.', 'error')
                return render_template('public/producto/editar_producto.html', producto=producto, data_form=data_form_dict)

        # Verificar si el código ya existe (excluyendo el actual)
        if codigo_existe(data_form_dict['codigo'], id_excluir=id):
            flash('El código ya existe. Usa un código diferente.', 'error')
            return render_template('public/producto/editar_producto.html', producto=producto, data_form=data_form_dict)

        # Actualizar producto
        resultado = actualizar_producto(id, data_form_dict, imagen)
        if resultado:
            flash('Producto actualizado correctamente', 'success')
        else:
            flash('Error al actualizar el producto', 'error')
        return redirect(url_for('lista_productos'))

    return render_template('public/producto/editar_producto.html', producto=producto, data_form=producto)
# Ruta para ver los detalles de un producto
@app.route('/detalles-producto/<int:id>')
def detalles_producto(id):
    if 'conectado' in session:
        producto = obtener_producto_por_id(id)
        if producto:
            return render_template('public/producto/detalles_producto.html', producto=producto)
        else:
            flash('Producto no encontrado', 'error')
            return redirect(url_for('lista_productos'))
    else:
        flash('Primero debes iniciar sesión.', 'error')
        return redirect(url_for('inicio'))

# Ruta para eliminar un producto
@app.route('/eliminar-producto/<int:id>', methods=['GET'])
def eliminar_producto_route(id):
    if 'conectado' in session:
        resultado = eliminar_producto(id)
        print(f"Resultado de eliminar_producto: {resultado}, tipo: {type(resultado)}")
        
        if resultado == True:
            flash('Producto eliminado correctamente.', 'success')
        else:
            flash('Error al eliminar el producto', 'error')
        
        return redirect(url_for('lista_productos'))
    else:
        flash('Usuario no autenticado', 'error')
        return redirect(url_for('inicio'))

# Ruta para buscar productos dinámicamente
@app.route("/buscando-producto", methods=['POST'])
def viewBuscarProductoBD():
    try:
        search_query = request.json.get('busqueda')
        if not search_query:
            return jsonify({'error': 'No search query provided'}), 400

        resultadoBusqueda = buscarProductoBD(search_query)

        if resultadoBusqueda:
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
            mensaje_html = f"""
            <tr>
                <td colspan="7" style="text-align:center;color: red;font-weight: bold;">
                    No resultados para la búsqueda: <strong style="color: #222;">{search_query}</strong>
                </td>
            </tr>
            """
            return jsonify({'success': False, 'html': mensaje_html})

    except Exception as e:
        print(f"Error en viewBuscarProductoBD: {e}")
        return jsonify({'error': str(e)}), 500
