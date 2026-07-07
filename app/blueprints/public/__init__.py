from flask import Blueprint

public_bp = Blueprint("public", __name__) #Declara el módulo como público.

from app.blueprints.public import routes # Importamos las rutas para asociarlas al Blueprint