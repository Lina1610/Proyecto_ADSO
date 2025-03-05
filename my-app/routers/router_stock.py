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
        resp_stockBD = obtener_stock()  # Cambia el nombre de la variable
        print(resp_stockBD)  # Depuración: Imprime los datos en la consola del servidor
        return render_template('public/stock/lista_stock.html', resp_stockBD=resp_stockBD)
    else:
        flash('Primero debes iniciar sesión.', 'error')
        return redirect(url_for('inicio'))
  
  
from flask import Blueprint, render_template, request, flash, redirect, url_for, session
from conexion.conexionBD import connectionBD

# Crear un Blueprint para las rutas de stock
router_stock = Blueprint('router_stock', __name__)

# Función para obtener un registro de stock por ID
def obtener_stock_por_id(id):
    try:
        with connectionBD() as conexion_MySQLdb:
            with conexion_MySQLdb.cursor(dictionary=True) as cursor:
                cursor.execute("""
                    SELECT s.id, s.cantidad_disponible, s.fecha_registro,
                           p.nombre AS producto_nombre, p.id AS producto_id,
                           u.nombre AS usuario_nombre, u.id AS users_id
                    FROM stock s
                    JOIN producto p ON s.producto_id = p.id
                    JOIN users u ON s.users_id = u.id
                    WHERE s.id = %s
                """, (id,))
                stock = cursor.fetchone()
                return stock
    except Exception as e:
        print(f"Error en obtener_stock_por_id: {e}")
        return None

# Función para obtener todos los productos
def obtener_productos():
    try:
        with connectionBD() as conexion_MySQLdb:
            with conexion_MySQLdb.cursor(dictionary=True) as cursor:
                cursor.execute("SELECT id, nombre FROM producto")
                productos = cursor.fetchall()
                return productos
    except Exception as e:
        print(f"Error en obtener_productos: {e}")
        return []

# Función para obtener todos los usuarios
def obtener_usuarios():
    try:
        with connectionBD() as conexion_MySQLdb:
            with conexion_MySQLdb.cursor(dictionary=True) as cursor:
                cursor.execute("SELECT id, nombre FROM users")
                usuarios = cursor.fetchall()
                return usuarios
    except Exception as e:
        print(f"Error en obtener_usuarios: {e}")
        return []

# Función para obtener todos los registros de stock
def obtener_stock():
    try:
        with connectionBD() as conexion_MySQLdb:
            with conexion_MySQLdb.cursor(dictionary=True) as cursor:
                cursor.execute("""
                    SELECT s.id, s.cantidad_disponible, s.fecha_registro,
                           p.nombre AS producto_nombre, p.id AS producto_id,
                           u.nombre AS usuario_nombre, u.id AS users_id
                    FROM stock s
                    JOIN producto p ON s.producto_id = p.id
                    JOIN users u ON s.users_id = u.id
                """)
                stock = cursor.fetchall()
                return stock
    except Exception as e:
        print(f"Error en obtener_stock: {e}")
        return []

# Ruta para listar el stock
@router_stock.route('/lista-de-stock')
def lista_stock():
    if 'conectado' in session:
        stock = obtener_stock()
        print(stock)  # Depuración: Imprime los datos en la consola del servidor
        return render_template('public/stock/lista_stock.html', resp_stockBD=stock)
    else:
        flash('Primero debes iniciar sesión.', 'error')
        return redirect(url_for('inicio'))

# Ruta para mostrar el formulario de edición de stock
@router_stock.route('/editar-stock/<int:id>', methods=['GET'])
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
            return redirect(url_for('router_stock.lista_stock'))
    else:
        flash('Primero debes iniciar sesión.', 'error')
        return redirect(url_for('inicio'))

# Ruta para actualizar el stock
@router_stock.route('/actualizar-stock', methods=['POST'])
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
                return redirect(url_for('router_stock.viewEditarStock', id=dataForm['id']))

            # Actualizar el stock en la base de datos
            with connectionBD() as conexion_MySQLdb:
                with conexion_MySQLdb.cursor(dictionary=True) as cursor:
                    sql = """
                        UPDATE stock
                        SET cantidad_disponible = %s, producto_id = %s, users_id = %s
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
            return redirect(url_for('router_stock.lista_stock'))
        except Exception as e:
            print(f"Error en actualizarStock: {e}")
            flash('Ocurrió un error al actualizar el stock.', 'error')
            return redirect(url_for('router_stock.viewEditarStock', id=dataForm['id']))
    else:
        flash('Primero debes iniciar sesión.', 'error')
        return redirect(url_for('inicio'))