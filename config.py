import os # permite leer variables de entorno del sistema

class Config: # Agrupa toda la configuración de la aplicación en un solo lugar
    SECRET_KEY = os.environ.get("SECRET_KEY") or "dev-secret-key" # Flask usa SECRET KEY para proteger sesiones

    # Configuración de la base de datos SQLite.
    # - Local: instance/app.db (como siempre).
    # - Vercel (deploy de demostración): el filesystem es de solo
    #   lectura, así que la base vive en /tmp (escribible pero
    #   temporal); api/index.py copia ahí la base de demo al arrancar.
    # - DATABASE_URL permite apuntar a otra ruta (lo usa
    #   build_demo_db.py para generar la base de demostración).
    if os.environ.get("DATABASE_URL"):
        SQLALCHEMY_DATABASE_URI = os.environ["DATABASE_URL"]
    elif os.environ.get("VERCEL"):
        SQLALCHEMY_DATABASE_URI = "sqlite:////tmp/app.db"
    else:
        SQLALCHEMY_DATABASE_URI = "sqlite:///app.db"

    SQLALCHEMY_TRACK_MODIFICATIONS = False # Desactiva una funcionalidad que no necestiamos y evita advertencias de flask

    # Límite de tamaño para archivos subidos (imágenes de productos): 5 MB
    MAX_CONTENT_LENGTH = 5 * 1024 * 1024