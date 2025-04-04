from flask import Flask
from dotenv import load_dotenv
import os
from migrations.migraciones import MigradorEntregas

def create_app():
    # Cargar variables de entorno
    load_dotenv()
    
    # Crear aplicación Flask
    app = Flask(__name__)
    
    # Configuración básica
    app.secret_key = os.getenv('SECRET_KEY')
    
    # Ejecutar migraciones automáticamente al crear la app
    with app.app_context():
        print("⚙️ Ejecutando migraciones necesarias...")
        resultado = MigradorEntregas.ejecutar_migraciones_iniciales()
        if resultado is not None:
            print(f"✅ Migraciones completadas. Registros afectados: {resultado}")
    
    # Registrar blueprints/routers
    from routers.router_carrito import carrito_bp
    from routers.router_pedido import pedido_bp
    from routers.router_soporte import soporte_bp
    
    app.register_blueprint(carrito_bp, url_prefix='/carrito')
    app.register_blueprint(pedido_bp, url_prefix='/pedido')
    app.register_blueprint(soporte_bp, url_prefix='/soporte')
    
    # Setup background migrations
    from background_migration import setup_background_migrations
    setup_background_migrations(app)
    
    return app
