from flask import Blueprint, render_template

# Define el blueprint
index = Blueprint('index', __name__)

@index.route('/')
def index_page():
    # Renderiza la plantilla
    return render_template('public/index.html')
