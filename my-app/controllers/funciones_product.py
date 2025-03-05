from werkzeug.utils import secure_filename
import uuid  # Modulo de python para crear un string

from conexion.conexionBD import connectionBD  # Conexión a BD

import datetime
import re
import os

from os import remove  # Modulo  para remover archivo
from os import path  # Modulo para obtener la ruta o directorio


import openpyxl  # Para generar el excel
# biblioteca o modulo send_file para forzar la descarga
from flask import send_file


from werkzeug.utils import secure_filename
import uuid
import os

def procesar_producto(dataForm, imagen):
    try:
        # Procesar el precio y convertirlo a un valor numérico decimal
        precio_sin_puntos = re.sub('[^0-9,\.]', '', dataForm['precio'])  # Limpiar cualquier carácter no numérico
        precio_decimal = float(precio_sin_puntos.replace(',', '.'))  # Reemplazar coma por punto para el decimal

        # Convertir unidad de medida a float si es necesario
        try:
            unidad_medida_float = float(dataForm['unidad_medida'])  # Convertir unidad de medida a float
        except ValueError:
            return 'La unidad de medida debe ser un número válido.'

        # Convertir el total a decimal (float) para asegurar su formato adecuado
        try:
            total_decimal = float(dataForm['total'])  # Convertir total a float (decimal)
        except ValueError:
            return 'El total debe ser un número válido.'

        # Procesar la imagen
        if imagen:
            # Generar un nombre único para la imagen
            nombre_imagen = secure_filename(imagen.filename)
            extension = nombre_imagen.split('.')[-1]
            nombre_unico = f"{uuid.uuid4()}.{extension}"
            
            # Guardar la imagen en la carpeta de imágenes
            ruta_imagen = os.path.join('static', 'assets', 'img', 'productos', nombre_unico)
            imagen.save(ruta_imagen)
            
            # Guardar la ruta de la imagen en la base de datos
            ruta_imagen_db = f"/static/assets/img/productos/{nombre_unico}"
        else:
            ruta_imagen_db = None  # Si no se sube una imagen

        with connectionBD() as conexion_MySQLdb:
            with conexion_MySQLdb.cursor(dictionary=True) as cursor:
                # SQL para insertar el producto
                sql = """
                    INSERT INTO producto (
                        codigo, nombre, descripcion, precio, estado, unidad_medida, cantidad, marca, total, imagen
                    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """

                # Creando una tupla con los valores del INSERT
                valores = (
                    dataForm['codigo'],  # Asegúrate de que el campo 'codigo' esté en el formulario
                    dataForm['nombre'], 
                    dataForm['descripcion'], 
                    precio_decimal,  # Usar el precio decimal procesado
                    dataForm['estado'], 
                    unidad_medida_float,  # Usar la unidad de medida como float
                    dataForm['cantidad'], 
                    dataForm['marca'], 
                    total_decimal,  # Usar el total como decimal
                    ruta_imagen_db  # Ruta de la imagen
                )
                
                cursor.execute(sql, valores)
                conexion_MySQLdb.commit()
                resultado_insert = cursor.rowcount
                return resultado_insert

    except Exception as e:
        return f'Se produjo un error en procesar_producto: {str(e)}'


def obtener_productos():
    try:
        with connectionBD() as conexion_MySQLdb:
            with conexion_MySQLdb.cursor(dictionary=True) as cursor:
                querySQL = "SELECT * FROM producto ORDER BY id DESC"
                cursor.execute(querySQL)
                productos = cursor.fetchall()
                
                # Convertir decimales a float para manipulación en Python
                for producto in productos:
                    if 'precio' in producto:
                        producto['precio'] = float(producto['precio'])
                    if 'total' in producto:
                        producto['total'] = float(producto['total'])
                
                return productos
    except Exception as e:
        print(f"Error en obtener_productos: {e}")
        return []
    
# buscar 
# Función para buscar productos en la base de datos
def buscarProductoBD(search):
    try:
        with connectionBD() as conexion_MySQLdb:
            with conexion_MySQLdb.cursor(dictionary=True) as mycursor:
                querySQL = ("""
                    SELECT 
                        id, codigo, nombre, descripcion, precio, cantidad, marca, estado, total
                    FROM producto
                    WHERE nombre LIKE %s OR codigo LIKE %s
                    ORDER BY id DESC
                """)
                search_pattern = f"%{search}%"  # Agregar "%" alrededor del término de búsqueda
                mycursor.execute(querySQL, (search_pattern, search_pattern))
                resultado_busqueda = mycursor.fetchall()
                return resultado_busqueda

    except Exception as e:
        print(f"Ocurrió un error en la función buscarProductoBD: {e}")
        return []

# actualizar producto
def actualizar_producto(id, data_form):
    try:
        with connectionBD() as conexion_MySQLdb:
            with conexion_MySQLdb.cursor(dictionary=True) as cursor:
                # Procesar el precio y total
                precio_sin_puntos = re.sub('[^0-9,\.]', '', data_form['precio'])
                precio_decimal = float(precio_sin_puntos.replace(',', '.'))
                total_decimal = float(data_form['total'])

                sql = """
                    UPDATE producto 
                    SET codigo = %s, nombre = %s, descripcion = %s, precio = %s, 
                        estado = %s, cantidad = %s, marca = %s, total = %s
                    WHERE id = %s
                """
                valores = (
                    data_form['codigo'], data_form['nombre'], data_form['descripcion'], precio_decimal,
                    data_form['estado'], data_form['cantidad'], data_form['marca'],
                    total_decimal, id
                )
                cursor.execute(sql, valores)
                conexion_MySQLdb.commit()
                return cursor.rowcount > 0
    except Exception as e:
        print(f"Error en actualizar_producto: {e}")
        return False

    
# funcion para poder optener los productos por su id    
def obtener_producto_por_id(id):
    try:
        with connectionBD() as conexion_MySQLdb:
            with conexion_MySQLdb.cursor(dictionary=True) as cursor:
                querySQL = "SELECT * FROM producto WHERE id = %s"
                cursor.execute(querySQL, (id,))
                producto = cursor.fetchone()
                if producto:
                    # Convertir decimales a float
                    producto['precio'] = float(producto['precio']) if producto['precio'] is not None else 0.0
                    producto['total'] = float(producto['total']) if producto['total'] is not None else 0.0
                return producto
    except Exception as e:
        print(f"Error en obtener_producto_por_id: {e}")
        return None

# funcion para poder eliminar los productos
def eliminar_producto(id):
    try:
        with connectionBD() as conexion_MySQLdb:
            with conexion_MySQLdb.cursor(dictionary=True) as cursor:
                querySQL = "DELETE FROM producto WHERE id = %s"
                cursor.execute(querySQL, (id,))
                conexion_MySQLdb.commit()
                return cursor.rowcount
    except Exception as e:
        print(f"Error en eliminar_producto: {e}")
        return None
    
def obtener_todos_los_productos():
    try:
        with connectionBD() as conexion_MySQLdb:
            with conexion_MySQLdb.cursor(dictionary=True) as cursor:
                # Consulta SQL para obtener todos los productos (sin filtrar por estado)
                querySQL = "SELECT * FROM producto ORDER BY id DESC"
                cursor.execute(querySQL)
                productos = cursor.fetchall()
                
                # Convertir decimales a float para manipulación en Python
                for producto in productos:
                    if 'precio' in producto:
                        producto['precio'] = float(producto['precio'])
                    if 'total' in producto:
                        producto['total'] = float(producto['total'])
                
                return productos
    except Exception as e:
        print(f"Error en obtener_todos_los_productos: {e}")
        return []