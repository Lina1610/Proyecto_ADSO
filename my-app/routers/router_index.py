# router_home.py
from flask import Blueprint, render_template

# Crear el blueprint para la página principal
home = Blueprint('home', __name__)

# Definir la ruta para la página principal
@home.route('/')
def inicio():
    return render_template('public/index.html')  # Esto renderiza index.html directamente
