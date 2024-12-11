from app import app
from flask import Flask, render_template, redirect, url_for, session, flash

# Importando los Routers (Rutas)
from routers.router_login import *
from routers.router_home import *
from routers.router_page_not_found import *

# Definir la ruta principal
@app.route('/')
def home():
    # Si el usuario está conectado, podrías mostrar algo adicional (opcional)
    if 'conectado' in session:
        flash('Ya estás conectado.', 'success')
    # Siempre renderiza el index.html
    return render_template('public/index.html')

# Ejecutando el objeto Flask
if __name__ == '__main__':  # Correcta forma de escribir esta condición
    app.run(debug=True, port=5600)  # Puedes cambiar el puerto si es necesario
