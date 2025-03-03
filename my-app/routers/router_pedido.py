from flask import Blueprint, render_template, redirect, url_for, flash, session
from controllers.funciones_pedido import obtener_productos

# Crear un Blueprint para los pedidos
pedido_bp = Blueprint('pedido', __name__)

@pedido_bp.route('/pedido')
def pedido():
    if 'conectado' in session:
        # Obtener todos los productos
        productos = obtener_productos()
        print(f"Productos en la ruta /pedido: {productos}")  # Log para depuración
        # Renderizar el template pedido.html con los productos
        return render_template('public/pedido/pedido.html', productos=productos)
    else:
        flash('Primero debes iniciar sesión.', 'error')
        return redirect(url_for('inicio'))