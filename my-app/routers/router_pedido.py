from flask import Blueprint, render_template, redirect, url_for, flash, session
from controllers.funciones_pedido import obtener_productos

# Crear un Blueprint para los pedidos
pedido_bp = Blueprint('pedido', __name__)

@pedido_bp.route('/pedido')
def pedido():
    # Obtener solo los productos disponibles
    productos = obtener_productos()
    print(f"Productos en la ruta /pedido: {productos}")  # Log para depuración
    return render_template('public/pedido/pedido.html', productos=productos)