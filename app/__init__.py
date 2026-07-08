from flask import Flask #importamos de flask la libreria Flask
from config import Config # Trae la configuración central
from app.extensions import db, login_manager

# Importamos los Blueprints de cada módulo del sistema
from app.blueprints.public import public_bp
from app.blueprints.admin import admin_bp
from app.blueprints.auth import auth_bp
from app.blueprints.quotes import quotes_bp
from app.blueprints.sales import sales_bp

def create_app (): #creamos la def create_app para que run.py pueda leer y ejecutarla
    app = Flask(__name__) #Creamos la aplicación principal que utilizará todo el sitema
    app.config.from_object(Config) # Cargamos la configuración central desde config.py

    db.init_app(app) # Conecta SQLAlchemy con Flask
    login_manager.init_app(app) # Conecta el control de sesión

    @login_manager.user_loader
    def load_user(user_id):
        return None

    # Registramos los Blueprints para que formen parte de la aplicación
    app.register_blueprint(public_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(quotes_bp)
    app.register_blueprint(sales_bp)
    return app


