from flask import Flask, request, redirect, url_for, flash, send_from_directory, render_template, session
from flask_mail import Mail, Message
from config import Config  # Importar la configuración
import pymysql

from dotenv import load_dotenv
from datetime import datetime  # Necesario para trabajar con las fechas
import os
import subprocess

# Cargar variables de entorno desde .env
load_dotenv()

# Crear la aplicación Flask
app = Flask(__name__)

# Cargar la configuración desde config.py
app.config.from_object(Config)

# Inicializar Flask-Mail
mail = Mail(app)

# Importando los Routers
from routers.router_login import *
from routers.router_home import *
from routers.router_page_not_found import *
from routers.router_product import *
from routers.router_order import *
from routers.router_user import *
from routers.router_address import *
from routers.router_delivery import *
from routers.router_invoice import *
from routers.router_stock import *
from routers.router_installment import *
from routers.router_pedido import *
from routers.router_principal import *
from routers.router_carrito import *

# Ruta para hacer copias de seguridad
from utils.backup_manager import hacer_copia_de_seguridad

from flask import send_file
from io import BytesIO

@app.route('/hacer_backup', methods=['GET', 'POST'])  # Acepta GET y POST
def hacer_backup():
    if request.method == 'GET':
        # Lógica para mostrar el formulario de selección de tablas
        try:
            conexion = pymysql.connect(
                host=os.getenv('DB_HOST'),
                user=os.getenv('DB_USER'),
                password=os.getenv('DB_PASSWORD'),
                database=os.getenv('DB_NAME')
            )
            with conexion.cursor() as cursor:
                cursor.execute("SHOW TABLES")
                tablas = [tabla[0] for tabla in cursor.fetchall()]
            return render_template('public/backup/backup.html', tablas=tablas)
        except pymysql.Error as e:
            flash(f"Error de MySQL: {str(e)}", 'error')
            return redirect(url_for('home'))
        finally:
            if 'conexion' in locals() and conexion:
                conexion.close()
    elif request.method == 'POST':
        # Lógica para procesar la creación del backup
        tablas_seleccionadas = request.form.getlist('tablas')
        if 'all' in tablas_seleccionadas:
            tablas_seleccionadas = None  # Hacer backup de todas las tablas
        try:
            backup_dir, nombre_archivo = hacer_copia_de_seguridad(tablas_seleccionadas)
            ruta_completa = os.path.join(backup_dir, nombre_archivo)
            return send_file(
                ruta_completa,
                as_attachment=True,
                download_name=nombre_archivo,
                mimetype='application/sql'
            )
        except Exception as e:
            flash(f"Error al crear la copia de seguridad: {str(e)}", 'error')
            return redirect(url_for('hacer_backup'))

@app.route('/restaurar_backup', methods=['GET', 'POST'])
def restaurar_backup():
    if request.method == 'GET':
        # Obtener la lista de backups disponibles
        backup_dir = os.path.join(os.getcwd(), 'backups')
        backups = [f for f in os.listdir(backup_dir) if f.endswith('.sql')]
        return render_template('public/backup/restaurar.html', backups=backups)
    elif request.method == 'POST':
        # Procesar la restauración del backup seleccionado
        backup_seleccionado = request.form['backup']
        ruta_backup = os.path.join(backup_dir, backup_seleccionado)
        try:
            # Conectar a la base de datos
            conexion = pymysql.connect(
                host=os.getenv('DB_HOST'),
                user=os.getenv('DB_USER'),
                password=os.getenv('DB_PASSWORD'),
                database=os.getenv('DB_NAME')
            )
            with conexion.cursor() as cursor:
                # Ejecutar el script SQL del backup
                with open(ruta_backup, 'r', encoding='utf-8') as archivo:
                    sql_script = archivo.read()
                    cursor.execute(sql_script)
                conexion.commit()
            flash(f"Backup {backup_seleccionado} restaurado con éxito", 'success')
        except Exception as e:
            flash(f"Error al restaurar el backup: {str(e)}", 'error')
        finally:
            if 'conexion' in locals() and conexion:
                conexion.close()
        return redirect(url_for('restaurar_backup'))
# Ruta principal
@app.route('/')
def home():
    if 'conectado' in session:
        flash('Ya estás conectado.', 'success')
    return render_template('public/index.html')

# Ruta para probar el envío de correos
@app.route('/enviar-correo')
def enviar_correo():
    msg = Message("Prueba de Correo", recipients=["destinatario@gmail.com"])
    msg.body = "Este es un mensaje de prueba desde Flask-Mail."
    
    try:
        mail.send(msg)
        flash("Correo enviado con éxito", "success")
    except Exception as e:
        flash(f"Error al enviar el correo: {str(e)}", "danger")
    
    return redirect(url_for('home'))

# Registrar el filtro 'date' en el entorno de Jinja2
@app.template_filter('date')
def format_date(value, format='%d/%m/%Y %H:%M:%S'):
    if isinstance(value, datetime):
        return value.strftime(format)
    return value  # En caso de que no sea un objeto datetime

if __name__ == '__main__':
    app.run(debug=True, port=5000)