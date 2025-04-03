from werkzeug.utils import secure_filename
import uuid
import os
from conexion.conexionBD import connectionBD
import datetime
import re
from os import remove
from os import path
import openpyxl
from flask import send_file

# Función para procesar y guardar un nuevo producto en la base de datos
def procesar_producto(dataForm, imagen):
    try:
        # Validamos que precio, cantidad y total sean mayores a 0
        precio_decimal = float(dataForm['precio'])
        total_decimal = float(dataForm['total'])
        cantidad = int(dataForm['cantidad'])
        if precio_decimal <= 0:
            return 'El precio debe ser mayor a 0.'
        if total_decimal <= 0:
            return 'El total debe ser mayor a 0.'
        if cantidad <= 0:
            return 'La cantidad debe ser mayor a 0.'

        # Validamos que el total sea igual a precio * cantidad
        if abs(total_decimal - (precio_decimal * cantidad)) > 0.01:
            return 'El total no coincide con precio * cantidad.'

        # Procesamos la imagen si se proporciona
        ruta_imagen_db = None
        if imagen and imagen.filename:
            nombre_imagen = secure_filename(imagen.filename)
            extension = nombre_imagen.split('.')[-1]
            nombre_unico = f"{uuid.uuid4()}.{extension}"
            ruta_imagen = os.path.join('static', 'assets', 'img', 'productos', nombre_unico)
            imagen.save(ruta_imagen)
            ruta_imagen_db = f"/static/assets/img/productos/{nombre_unico}"

        # Conectamos a la base de datos y ejecutamos la consulta INSERT
        with connectionBD() as conexion_MySQLdb:
            with conexion_MySQLdb.cursor(dictionary=True) as cursor:
                sql = """
                    INSERT INTO producto (
                        codigo, nombre, descripcion, precio, estado, cantidad, total, imagen
                    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                """
                valores = (
                    dataForm['codigo'],
                    dataForm['nombre'],
                    dataForm['descripcion'],
                    precio_decimal,
                    dataForm['estado'],
                    cantidad,
                    total_decimal,
                    ruta_imagen_db
                )
                cursor.execute(sql, valores)
                conexion_MySQLdb.commit()
                resultado_insert = cursor.rowcount
                return resultado_insert

    except Exception as e:
        return f'Se produjo un error en procesar_producto: {str(e)}'

# Función para obtener todos los productos (usada en algunas rutas)
def obtener_productos():
    try:
        with connectionBD() as conexion_MySQLdb:
            with conexion_MySQLdb.cursor(dictionary=True) as cursor:
                querySQL = "SELECT * FROM producto ORDER BY id DESC"
                cursor.execute(querySQL)
                productos = cursor.fetchall()
                
                # Convertimos decimales a float para manipulación en Python
                for producto in productos:
                    if 'precio' in producto:
                        producto['precio'] = float(producto['precio'])
                    if 'total' in producto:
                        producto['total'] = float(producto['total'])
                
                return productos
    except Exception as e:
        print(f"Error en obtener_productos: {e}")
        return []

# Función para buscar productos por nombre o código
def buscarProductoBD(search):
    try:
        with connectionBD() as conexion_MySQLdb:
            with conexion_MySQLdb.cursor(dictionary=True) as mycursor:
                querySQL = ("""
                    SELECT 
                        id, codigo, nombre, descripcion, precio, cantidad, estado, total
                    FROM producto
                    WHERE nombre LIKE %s OR codigo LIKE %s
                    ORDER BY id DESC
                """)
                search_pattern = f"%{search}%"
                mycursor.execute(querySQL, (search_pattern, search_pattern))
                resultado_busqueda = mycursor.fetchall()
                return resultado_busqueda

    except Exception as e:
        print(f"Ocurrió un error en la función buscarProductoBD: {e}")
        return []

# Función para actualizar un producto existente
# Función para actualizar un producto existente (incluyendo imagen)
def actualizar_producto(id, dataForm, imagen=None):
    try:
        # Validaciones de campos numéricos
        precio_decimal = float(dataForm['precio'])
        total_decimal = float(dataForm['total'])
        cantidad = int(dataForm['cantidad'])
        
        if precio_decimal <= 0:
            return False
        if total_decimal <= 0:
            return False
        if cantidad <= 0:
            return False

        # Validar que el total sea igual a precio * cantidad
        if abs(total_decimal - (precio_decimal * cantidad)) > 0.01:
            return False

        # Procesar imagen si se proporciona
        ruta_imagen_db = None
        if imagen and imagen.filename:
            # Eliminar la imagen anterior si existe
            producto_actual = obtener_producto_por_id(id)
            if producto_actual and producto_actual.get('imagen'):
                ruta_imagen_antigua = producto_actual['imagen'].replace('/static', 'static')
                if path.exists(ruta_imagen_antigua):
                    remove(ruta_imagen_antigua)
            
            # Guardar la nueva imagen
            nombre_imagen = secure_filename(imagen.filename)
            extension = nombre_imagen.split('.')[-1]
            nombre_unico = f"{uuid.uuid4()}.{extension}"
            ruta_imagen = os.path.join('static', 'assets', 'img', 'productos', nombre_unico)
            imagen.save(ruta_imagen)
            ruta_imagen_db = f"/static/assets/img/productos/{nombre_unico}"

        with connectionBD() as conexion_MySQLdb:
            with conexion_MySQLdb.cursor(dictionary=True) as cursor:
                if ruta_imagen_db:
                    sql = """
                        UPDATE producto 
                        SET codigo = %s, nombre = %s, descripcion = %s, precio = %s, 
                            estado = %s, cantidad = %s, total = %s, imagen = %s
                        WHERE id = %s
                    """
                    valores = (
                        dataForm['codigo'], dataForm['nombre'], dataForm['descripcion'], precio_decimal,
                        dataForm['estado'], cantidad, total_decimal, ruta_imagen_db, id
                    )
                else:
                    sql = """
                        UPDATE producto 
                        SET codigo = %s, nombre = %s, descripcion = %s, precio = %s, 
                            estado = %s, cantidad = %s, total = %s
                        WHERE id = %s
                    """
                    valores = (
                        dataForm['codigo'], dataForm['nombre'], dataForm['descripcion'], precio_decimal,
                        dataForm['estado'], cantidad, total_decimal, id
                    )
                
                cursor.execute(sql, valores)
                conexion_MySQLdb.commit()
                return cursor.rowcount > 0
    except Exception as e:
        print(f"Error en actualizar_producto: {e}")
        return False

# Función para obtener un producto por su ID
def obtener_producto_por_id(id):
    try:
        with connectionBD() as conexion_MySQLdb:
            with conexion_MySQLdb.cursor(dictionary=True) as cursor:
                querySQL = "SELECT * FROM producto WHERE id = %s"
                cursor.execute(querySQL, (id,))
                producto = cursor.fetchone()
                if producto:
                    producto['precio'] = float(producto['precio']) if producto['precio'] is not None else 0.0
                    producto['total'] = float(producto['total']) if producto['total'] is not None else 0.0
                return producto
    except Exception as e:
        print(f"Error en obtener_producto_por_id: {e}")
        return None

# Función para eliminar un producto
def eliminar_producto(id):
    try:
        with connectionBD() as conexion_MySQLdb:
            with conexion_MySQLdb.cursor(dictionary=True) as cursor:
                cursor.execute("SELECT id FROM producto WHERE id = %s", (id,))
                existe_antes = cursor.fetchone() is not None
                
                if not existe_antes:
                    return False
                
                querySQL = "DELETE FROM producto WHERE id = %s"
                cursor.execute(querySQL, (id,))
                conexion_MySQLdb.commit()
                
                cursor.execute("SELECT id FROM producto WHERE id = %s", (id,))
                existe_despues = cursor.fetchone() is not None
                
                return existe_antes and not existe_despues
    except Exception as e:
        print(f"Error en eliminar_producto: {e}")
        return False

# Función para obtener todos los productos (usada en la lista de productos)
def obtener_todos_los_productos():
    try:
        with connectionBD() as conexion_MySQLdb:
            with conexion_MySQLdb.cursor(dictionary=True) as cursor:
                querySQL = "SELECT * FROM producto ORDER BY id DESC"
                cursor.execute(querySQL)
                productos = cursor.fetchall()
                
                for producto in productos:
                    if 'precio' in producto:
                        producto['precio'] = float(producto['precio'])
                    if 'total' in producto:
                        producto['total'] = float(producto['total'])
                
                return productos
    except Exception as e:
        print(f"Error en obtener_todos_los_productos: {e}")
        return []

# Nueva función para verificar si un código ya existe
def codigo_existe(codigo, id_excluir=None):
    try:
        with connectionBD() as conexion_MySQLdb:
            with conexion_MySQLdb.cursor(dictionary=True) as cursor:
                if id_excluir:
                    # Excluimos el ID del producto actual al editar
                    querySQL = "SELECT id FROM producto WHERE codigo = %s AND id != %s"
                    cursor.execute(querySQL, (codigo, id_excluir))
                else:
                    # Para registro, no excluimos ningún ID
                    querySQL = "SELECT id FROM producto WHERE codigo = %s"
                    cursor.execute(querySQL, (codigo,))
                resultado = cursor.fetchone()
                return resultado is not None  # True si el código ya existe, False si no
    except Exception as e:
        print(f"Error en codigo_existe: {e}")
        return False
