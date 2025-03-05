from flask import Flask

app = Flask(__name__)
application = app
app.secret_key = '97110c78ae51a45af397b6534caef90ebb9b1dcb3380f008f90b23a5d1616bf1bc29098105da20fe'

from routers.router_carrito import carrito_bp
from routers.router_pedido import pedido_bp  # <-- Agregar esta línea

# Luego registra el blueprint así
app.register_blueprint(carrito_bp, url_prefix='/carrito')
app.register_blueprint(pedido_bp, url_prefix='/pedido') 