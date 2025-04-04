from flask import Flask, session, redirect, url_for, render_template
from dotenv import load_dotenv
from flask_mail import Mail
import os
from config import Config



# Cargar variables de entorno
load_dotenv()

# Crear aplicación Flask
app = Flask(__name__)
application = app  # Para compatibilidad con algunos servidores

# Configuración
app.config.from_object(Config)
app.secret_key = os.getenv('SECRET_KEY')

# Inicializar Flask-Mail
mail = Mail(app)

# Importar y registrar blueprints
from routers.router_carrito import carrito_bp
from routers.router_pedido import pedido_bp
from routers.router_soporte import soporte_bp

app.register_blueprint(carrito_bp, url_prefix='/carrito')
app.register_blueprint(pedido_bp, url_prefix='/pedido')
app.register_blueprint(soporte_bp, url_prefix='/soporte')



if __name__ == '__main__':
    app.run(ssl_context='adhoc')