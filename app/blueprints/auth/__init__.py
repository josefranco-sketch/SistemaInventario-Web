from flask import Blueprint

auth_bp = Blueprint("auth", __name__)

from app.blueprints.auth import routes # Importamos las rutas para asociarlas al Blueprint
