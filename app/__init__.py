from flask import Flask #importamos de flask la libreria Flask
from config import Config # Trae la configuración central
from app.extensions import db, login_manager
from app.models.user import User # Modelo de usuarios internos (admin/vendedor)

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

    # Si alguien intenta entrar a una ruta protegida sin sesión,
    # Flask-Login lo redirige automáticamente a la pantalla de login.
    login_manager.login_view = "auth.login"
    login_manager.login_message = "Inicia sesión para acceder al panel interno."
    login_manager.login_message_category = "warning"

    @login_manager.user_loader
    def load_user(user_id):
        # Flask-Login guarda el id del usuario en la sesión;
        # con ese id recuperamos el usuario desde la base de datos.
        return db.session.get(User, int(user_id))

    # Registramos los Blueprints para que formen parte de la aplicación
    app.register_blueprint(public_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(quotes_bp)
    app.register_blueprint(sales_bp)

    # Crea las tablas en la base de datos si todavía no existen
    with app.app_context():
        db.create_all()

    return app
