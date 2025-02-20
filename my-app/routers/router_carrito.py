from app import app
from flask import Flask, render_template, redirect, url_for

@app.route('/public/carrito')
def carritoCompras():
    return render_template('public/carrito/carrito.html')

@app.route('/confirmar-pedido', methods=['POST'])
def confirmar_pedido():
    return redirect(url_for('carritoCompras'))

if __name__ == '__main__':
    app.run(debug=True)