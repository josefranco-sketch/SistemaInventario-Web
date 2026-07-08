# Paquete de modelos de la aplicación (capa de datos con SQLAlchemy).
#
# Aquí se importan todos los modelos para que SQLAlchemy los conozca
# al momento de crear las tablas con db.create_all().
from app.models.category import Category, Subcategory
from app.models.product import Product
from app.models.user import User
