from app import app
from flask import Flask, render_template



@app.route('/pedido')
def pedido():
    return render_template('public/pedido/pedido.html')
                                                                                                                                                     