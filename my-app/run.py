from app import app
from flask import render_template, redirect, url_for, session, flash
from flask_mail import Mail, Message
from config import Config  # Importar la configuración
from dotenv import load_dotenv
from datetime import datetime  # Necesario para trabajar con las fechas

load_dotenv()  # Cargar variables de entorno desde .env

# Importando los Routers
from routers.router_login import *
from routers.router_home import *
from routers.router_page_not_found import *
from routers.router_product import *
from routers.router_order import *
from routers.router_pass import *
from routers.router_user import *
from routers.router_address import *
from routers.router_delivery import *
from routers.router_invoice import *
from routers.router_inventory import *
from routers.router_installment import *




# Cargar la configuración desde config.py
app.config.from_object(Config)

# Inicializar Flask-Mail
mail = Mail(app)

# Registrar el filtro 'date' en el entorno de Jinja2
@app.template_filter('date')
def format_date(value, format='%d/%m/%Y %H:%M:%S'):
    if isinstance(value, datetime):
        return value.strftime(format)
    return value  # En caso de que no sea un objeto datetime

from routers.router_pedido import *
from routers.router_principal import*
from routers.router_carrito import*


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

if __name__ == '__main__':
    app.run(debug=True, port=5000)
