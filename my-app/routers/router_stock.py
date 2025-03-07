from app import app
from flask import render_template, request, flash, redirect, url_for, session, jsonify
from mysql.connector.errors import Error

# Importando conexión a BD

# Importando cenexión a BD
from controllers.funciones_stock import *


PATH_URL = "public/stock"  
# Ruta base para las plantillas de inventario
@app.route ('/registrar-stock', methods=['GET', 'POST'])
def viewFormStock():
    if 'conectado' in session:
        if request.method == 'POST':
            dataForm = {
                'cantidad_disponible': request.form.get('cantidad_disponible'),
                'producto_id': request.form.get('producto_id'),
                'users_id': request.form.get('users_id')
            }

            resultado = procesar_stock(dataForm)

            if isinstance(resultado, int) and resultado > 0:
                flash('Stock registrado correctamente.', 'success')
            else:
                flash(resultado, 'error')

            return redirect(url_for('viewFormStock'))

        with connectionBD() as conexion_MySQLdb:
            with conexion_MySQLdb.cursor(dictionary=True) as cursor:
                cursor.execute("SELECT id, nombre FROM producto")
                productos = cursor.fetchall()

                cursor.execute("SELECT id, nombre FROM users WHERE rol != 'cliente'")
                usuarios = cursor.fetchall()

        return render_template('public/stock/registro_stock.html', productos=productos, usuarios=usuarios)
    else:
        flash('Primero debes iniciar sesión.', 'error')
        return redirect(url_for('inicio'))
    
@app.route('/lista-de-stock')
def lista_stock():
    if 'conectado' in session:
        # Obtener el número de página desde la URL (por defecto es 1)
        pagina = request.args.get('pagina', 1, type=int)

        # Obtener los datos de stock con paginación
        resp_stockBD, total_stock = obtener_stock(pagina=pagina, por_pagina=10)

        return render_template(
            'public/stock/lista_stock.html',
            resp_stockBD=resp_stockBD,
            pagina=pagina,
            total_stock=total_stock
        )
    else:
        flash('Primero debes iniciar sesión.', 'error')
        return redirect(url_for('inicio'))
@app.route('/editar-stock/<int:id>', methods=['GET'])
def viewEditarStock(id):
    if 'conectado' in session:
        # Obtener el stock por ID
        stock = obtener_stock_por_id(id)
        if stock:
            # Obtener la lista de productos y usuarios
            productos = obtener_productos()
            usuarios = obtener_usuarios()
            return render_template('public/stock/editar_stock.html', stock=stock, productos=productos, usuarios=usuarios)
        else:
            flash('El stock no existe.', 'error')
            return redirect(url_for('lista_stock'))
    else:
        flash('Primero debes iniciar sesión.', 'error')
        return redirect(url_for('inicio'))

@app.route('/actualizar-stock', methods=['POST'])
def actualizarStock():
    if 'conectado' in session:
        try:
            # Obtener los datos del formulario
            dataForm = {
                'id': request.form.get('id'),
                'cantidad_disponible': request.form.get('cantidad_disponible'),
                'producto_id': request.form.get('producto_id'),
                'users_id': request.form.get('users_id')
            }

            # Validar que la cantidad disponible sea mayor a cero
            cantidad_disponible = int(dataForm['cantidad_disponible'])
            if cantidad_disponible <= 0:
                flash('La cantidad disponible debe ser mayor a cero.', 'error')
                return redirect(url_for('viewEditarStock', id=dataForm['id']))

            # Actualizar el stock en la base de datos
            with connectionBD() as conexion_MySQLdb:
                with conexion_MySQLdb.cursor() as cursor:
                    sql = """
                        UPDATE stock
                        SET cantidad_disponible = %s,
                            producto_id = %s,
                            users_id = %s
                        WHERE id = %s
                    """
                    valores = (
                        dataForm['cantidad_disponible'],
                        dataForm['producto_id'],
                        dataForm['users_id'],
                        dataForm['id']
                    )
                    cursor.execute(sql, valores)
                    conexion_MySQLdb.commit()

            flash('Stock actualizado correctamente.', 'success')
            return redirect(url_for('lista_stock'))
        except Exception as e:
            print(f"Error en actualizarStock: {e}")
            flash('Ocurrió un error al actualizar el stock.', 'error')
            return redirect(url_for('viewEditarStock', id=dataForm['id']))
    else:
        flash('Primero debes iniciar sesión.', 'error')
        return redirect(url_for('inicio'))
    
@app.route('/detalles-stock/<int:id>')
def detalles_stock(id):
    if 'conectado' in session:
        stock = obtener_stock_por_id(id)
        if stock:
            return render_template('public/stock/detalles_stock.html', stock=stock)
        else:
            flash('Stock no encontrado', 'error')
            return redirect(url_for('lista_stock'))
    else:
        flash('Primero debes iniciar sesión.', 'error')
        return redirect(url_for('inicio'))
    
@app.route("/buscando-stock", methods=['POST'])
def viewBuscarStockBD():
    try:
        search_query = request.json.get('busqueda')  # Obtener el término de búsqueda desde el JSON
        if not search_query:
            return jsonify({'error': 'No search query provided'}), 400

        resultadoBusqueda = buscarStockBD(search_query)  # Buscar stock en la base de datos

        if resultadoBusqueda:
            # Si hay resultados, generar el HTML de la tabla
            html_resultados = ""
            for stock in resultadoBusqueda:
                html_resultados += f"""
                <tr id="stock_{stock['id']}">
                    <td>{stock['id']}</td>
                    <td>{stock['cantidad_disponible']}</td>
                    <td>{stock['fecha_registro']}</td>
                    <td>{stock['producto_nombre']} (ID: {stock['producto_id']})</td>
                    <td>{stock['usuario_nombre']} (ID: {stock['users_id']})</td>
                    <td width="10px">
                        <a href="/detalles-stock/{stock['id']}" class="btn btn-info btn-sm" title="Ver detalles">
                            <i class="bi bi-eye"></i> Ver detalles
                        </a>
                        <a href="/editar-stock/{stock['id']}" class="btn btn-success btn-sm" title="Actualizar">
                            <i class="bi bi-arrow-clockwise"></i> Actualizar
                        </a>
                        <a href="#" onclick="eliminarStock('{stock['id']}');" class="btn btn-danger btn-sm" title="Eliminar">
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
                <td colspan="6" style="text-align:center;color: red;font-weight: bold;">
                    No resultados para la búsqueda: <strong style="color: #222;">{search_query}</strong>
                </td>
            </tr>
            """
            return jsonify({'success': False, 'html': mensaje_html})

    except Exception as e:
        print(f"Error en viewBuscarStockBD: {e}")  # Log de depuración
        return jsonify({'error': str(e)}), 500  # Manejo de errores
    
@app.route('/eliminar-stock/<int:id>', methods=['DELETE'])
def eliminar_stock_route(id):
    if 'conectado' in session:
        resultado = eliminar_stock(id)
        if resultado and resultado > 0:
            return jsonify({'success': True, 'message': 'Stock eliminado correctamente'})
        return jsonify({'success': False, 'message': 'Error al eliminar stock'})
    return jsonify({'success': False, 'message': 'Usuario no autenticado'}), 401
    
