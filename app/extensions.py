# Importamos las extensiones principales que utilizará toda la aplicación
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

# Creamos las instancias de SQLAlchemy y LoginManager para que puedan
# inicializarse una sola vez y reutilizarse en toda la aplicación.
db = SQLAlchemy()
login_manager = LoginManager()