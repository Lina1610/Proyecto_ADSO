from flask import Flask, request, redirect, url_for, flash, send_from_directory, render_template, session
from flask_mail import Mail, Message
from config import Config  # Importar la configuración
import pymysql
from dotenv import load_dotenv
from datetime import datetime
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

# Ruta para crear una copia de seguridad
@app.route('/hacer_backup', methods=['GET'])
def hacer_backup():
    try:
        backup_info = hacer_copia_de_seguridad()
        flash(f"Copia de seguridad creada: {backup_info['nombre']}", "success")
    except Exception as e:
        flash(f"Error al crear la copia de seguridad: {str(e)}", "danger")
    return redirect(url_for('lista_backups'))

# Ruta para listar copias de seguridad
@app.route('/lista_backups')
def lista_backups():
    backup_dir = os.path.join(os.getcwd(), 'backups')
    backups = []
    for filename in os.listdir(backup_dir):
        if filename.endswith('.sql'):
            ruta = os.path.join(backup_dir, filename)
            backups.append({
                "nombre": filename,
                "fecha_creacion": datetime.fromtimestamp(os.path.getctime(ruta)).strftime('%Y-%m-%d %H:%M:%S'),
                "tamaño": round(os.path.getsize(ruta) / (1024 * 1024), 2)  # Tamaño en MB
            })
    return render_template('public/backup/lista_backup.html', backups=backups)

# Ruta para restaurar una copia de seguridad
@app.route('/restaurar_backup/<nombre_archivo>')
def restaurar_backup(nombre_archivo):
    backup_dir = os.path.join(os.getcwd(), 'backups')
    ruta_backup = os.path.join(backup_dir, nombre_archivo)
    
    try:
        # Leer el contenido del archivo de backup
        with open(ruta_backup, 'r', encoding='utf-8') as archivo:
            sql_script = archivo.read()
        
        # Verificar si el contenido es válido
        if not sql_script.strip():
            flash("El archivo de backup está vacío.", "danger")
            return redirect(url_for('lista_backups'))
        
        # Conectar a la base de datos
        conexion = pymysql.connect(
            host=os.getenv('DB_HOST'),
            user=os.getenv('DB_USER'),
            password=os.getenv('DB_PASSWORD'),
            database=os.getenv('DB_NAME')
        )
        
        with conexion.cursor() as cursor:
            # 1. Desactivar temporalmente las restricciones de clave foránea
            cursor.execute("SET FOREIGN_KEY_CHECKS = 0")
            
            # 2. Obtener todas las tablas de la base de datos
            cursor.execute("SHOW TABLES")
            tablas = [tabla[0] for tabla in cursor.fetchall()]
            
            # 3. Vaciar todas las tablas existentes
            for tabla in tablas:
                try:
                    cursor.execute(f"TRUNCATE TABLE {tabla}")
                    print(f"Tabla {tabla} vaciada correctamente")
                except pymysql.Error as e:
                    print(f"Error al vaciar la tabla {tabla}: {str(e)}")
            
            # 4. Ejecutar sentencias del backup
            for sentencia in sql_script.split(';'):
                sentencia = sentencia.strip()
                if sentencia:
                    try:
                        if sentencia.upper().startswith("CREATE TABLE"):
                            # Ignorar sentencias CREATE TABLE
                            continue
                        else:
                            cursor.execute(sentencia)
                    except pymysql.Error as e:
                        print(f"Error al ejecutar sentencia: {str(e)}")
            
            # 5. Reactivar las restricciones de clave foránea
            cursor.execute("SET FOREIGN_KEY_CHECKS = 1")
            
            conexion.commit()
        
        flash(f"Backup {nombre_archivo} restaurado con éxito. La base de datos ha sido restablecida al estado del backup.", "success")
    
    except Exception as e:
        flash(f"Error al restaurar el backup: {str(e)}", "danger")
    
    finally:
        if 'conexion' in locals() and conexion:
            conexion.close()
    
    return redirect(url_for('lista_backups'))

# Ruta para eliminar una copia de seguridad
@app.route('/eliminar_backup/<nombre_archivo>')
def eliminar_backup(nombre_archivo):
    backup_dir = os.path.join(os.getcwd(), 'backups')
    ruta_backup = os.path.join(backup_dir, nombre_archivo)
    try:
        os.remove(ruta_backup)
        flash(f"Backup {nombre_archivo} eliminado con éxito", "success")
    except Exception as e:
        flash(f"Error al eliminar el backup: {str(e)}", "danger")
    return redirect(url_for('lista_backups'))

# Ruta principal
@app.route('/')
def home():
    if 'conectado' in session:
        flash('Ya estás conectado.', 'success')
    return render_template('public/index.html')

if __name__ == '__main__':
    app.run(debug=True, port=5000)