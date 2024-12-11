# Declarando nombre de la aplicación e inicializando, crear la aplicación Flask
from app import app

# Importando todos mis Routers (Rutas)
from routers.router_login import *
from routers.router_home import *
from routers.router_page_not_found import *
from routers.router_product import *
from routers.router_supplier import *
from routers.router_invoice import *
from routers.router_order import *
from routers.router_pass import *


# Ejecutando el objeto Flask
if __name__ == '__main__':
    app.run(debug=True, port=5600)
