# Rutas del módulo público
from app.blueprints.public import public_bp

@public_bp.route("/") #Le dice a flask, cuando un usuario entre a /, ejecuta esta función
def home(): # Función que responderá a esa petición
    return "<h1>Sistema Integral de Gestión Comercial</h1>" # Devuelve una página HTML simple para comprobar que el BP funciona