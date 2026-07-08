import os # permite leer variables de entorno del sistema

class Config: # Agrupa toda la configuración de la aplicación en un solo lugar
    SECRET_KEY = os.environ.get("SECRET_KEY") or "dev-secret-key" # Flask usa SECRET KEY para proteger sesiones

    # Configuración de la base de datos SQLite para el entorno de desarrollo
    SQLALCHEMY_DATABASE_URI = "sqlite:///app.db" # Le dice a SQLAlchemy que usaremos una base de datos SQLite llama app.db
    SQLALCHEMY_TRACK_MODIFICATIONS = False # Desactiva una funcionalidad que no necestiamos y evita advertencias de flask

    # Límite de tamaño para archivos subidos (imágenes de productos): 5 MB
    MAX_CONTENT_LENGTH = 5 * 1024 * 1024