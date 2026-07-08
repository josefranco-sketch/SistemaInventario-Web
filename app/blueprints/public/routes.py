# Rutas del módulo público
from flask import render_template
from app.blueprints.public import public_bp

@public_bp.route("/") #Le dice a flask, cuando un usuario entre a /, ejecuta esta función
def home(): # Función que responderá a esa petición
    return render_template("public/home.html") 