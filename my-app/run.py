from app import app
from flask import Flask, render_template, redirect, url_for, session

# Importando los Routers (Rutas)
from routers.router_login import *
from routers.router_home import *
from routers.router_page_not_found import *

# Definir la ruta principal
@app.route('/')
def home():
    # Verificar si el usuario está conectado (es decir, si existe una clave 'conectado' en la sesión)
    if 'conectado' in session:
        # Si está conectado, redirigir al panel o dashboard
        return redirect(url_for('dashboard'))  # O tu ruta de panel, por ejemplo 'dashboard'
    else:
        # Si no está conectado, mostrar la página de inicio (index.html)
        return render_template('public/index.html')

# Ejecutando el objeto Flask
if __name__ == '__main__':  # Correcta forma de escribir esta condición
    app.run(debug=True, port=5600)  # Puedes cambiar el puerto si es necesario
