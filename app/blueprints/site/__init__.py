from flask import Blueprint

# NOTA (Sprint 8.2): esta carpeta se llamaba "public", pero Vercel excluye
# del bundle serverless cualquier directorio con ese nombre (lo reserva
# para archivos estáticos), dejando el deploy sin el módulo público.
# El NOMBRE del blueprint sigue siendo "public", así que los endpoints
# (url_for('public.home'), etc.) no cambian.

public_bp = Blueprint("public", __name__) #Declara el módulo como público.

from app.blueprints.site import routes # Importamos las rutas para asociarlas al Blueprint