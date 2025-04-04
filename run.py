from flask import Flask, request, redirect, url_for, flash, render_template, session
from flask_mail import Mail
from config import Config
from dotenv import load_dotenv
import os
from datetime import datetime

# Cargar variables de entorno desde .env
load_dotenv()

# Crear la aplicación Flask
app = Flask(__name__)

# Cargar configuración
app.config.from_object(Config)

# Inicializar Flask-Mail
mail = Mail(app)

# 🔹 Importar y registrar Blueprints
from routers.router_carrito import carrito_bp
from routers.router_pedido import pedido_bp
from routers.router_soporte import soporte_bp

app.register_blueprint(carrito_bp, url_prefix='/carrito')
app.register_blueprint(pedido_bp, url_prefix='/pedido')
app.register_blueprint(soporte_bp, url_prefix='/soporte')

# 🔹 Importar rutas normales sin Blueprints
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
from routers.router_principal import *

# 🔹 Rutas de backups
from utils.backup_manager import hacer_copia_de_seguridad, ejecutar_restauracion

@app.route('/hacer_backup', methods=['GET'])
def hacer_backup():
    try:
        backup_info = hacer_copia_de_seguridad()
        flash(f"Copia de seguridad creada: {backup_info['nombre']}", "success")
    except Exception as e:
        flash(f"Error al crear la copia de seguridad: {str(e)}", "danger")
    return redirect(url_for('lista_backups'))

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

@app.route('/restaurar_backup/<nombre_archivo>', methods=['GET'])
def restaurar_backup_route(nombre_archivo):
    backup_dir = os.path.join(os.getcwd(), 'backups')
    ruta_backup = os.path.join(backup_dir, nombre_archivo)
    
    if not os.path.exists(ruta_backup):
        flash(f"Archivo de backup no encontrado: {nombre_archivo}", "danger")
        return redirect(url_for('lista_backups'))
    
    resultado = ejecutar_restauracion(ruta_backup)
    
    if resultado['success']:
        flash(resultado['message'], "success")
    else:
        flash(resultado['message'], "danger")
    
    return redirect(url_for('lista_backups'))

@app.route('/eliminar_backup/<nombre_archivo>', methods=['GET'])
def eliminar_backup(nombre_archivo):
    backup_dir = os.path.join(os.getcwd(), 'backups')
    ruta_backup = os.path.join(backup_dir, nombre_archivo)
    try:
        os.remove(ruta_backup)
        flash(f"Backup {nombre_archivo} eliminado con éxito", "success")
    except Exception as e:
        flash(f"Error al eliminar el backup: {str(e)}", "danger")
    return redirect(url_for('lista_backups'))

# 🔹 Configuración para Render o producción
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=True, host='0.0.0.0', port=port)

    
