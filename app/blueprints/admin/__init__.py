from flask import Blueprint

# Todas las rutas de este módulo cuelgan de /admin
admin_bp = Blueprint("admin", __name__, url_prefix="/admin")

from app.blueprints.admin import routes # Importamos las rutas para asociarlas al Blueprint
