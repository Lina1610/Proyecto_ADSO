# app.py
from flask import Flask
from dotenv import load_dotenv
from flask_mail import Mail
import os
from config import Config  # Import the config class

load_dotenv()

app = Flask(__name__)
application = app

# Load configuration from Config class
app.config.from_object(Config)

# Initialize Flask-Mail
mail = Mail(app)

# Secret key and other configs
app.secret_key = os.getenv('SECRET_KEY')
# ... resto de configuraciones ...

# Registra todos los blueprints
from routers.router_carrito import carrito_bp
from routers.router_pedido import pedido_bp
from routers.router_soporte import soporte_bp

app.register_blueprint(carrito_bp, url_prefix='/carrito')
app.register_blueprint(pedido_bp, url_prefix='/pedido')
app.register_blueprint(soporte_bp, url_prefix='/soporte')

if __name__ == '__main__':
    app.run(ssl_context='adhoc')