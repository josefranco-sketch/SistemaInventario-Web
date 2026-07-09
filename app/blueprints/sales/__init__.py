from flask import Blueprint

# Todas las rutas de este módulo cuelgan de /sales
sales_bp = Blueprint("sales", __name__, url_prefix="/sales")

from app.blueprints.sales import routes # Importamos las rutas para asociarlas al Blueprint
