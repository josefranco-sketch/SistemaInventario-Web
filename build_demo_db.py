# ==========================================================
# Script de consola para generar la base de DEMOSTRACIÓN que se
# incluye en el repo (deploy/demo_app.db) y que Vercel copia a
# /tmp en cada arranque en frío.
#
# Se ejecuta desde la terminal (con el entorno virtual activo):
#
#     python build_demo_db.py
#
# Crea desde cero: usuarios de demo (admin y vendedor), el
# catálogo inicial (reutilizando seed_catalog) y stock inicial
# con historial real de movimientos. Si el archivo ya existe,
# lo reemplaza.
# ==========================================================
import os

# La base destino se define ANTES de importar la app, porque
# config.py lee DATABASE_URL al cargarse.
DEMO_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "deploy", "demo_app.db")
os.makedirs(os.path.dirname(DEMO_PATH), exist_ok=True)
if os.path.exists(DEMO_PATH):
    os.remove(DEMO_PATH)
os.environ["DATABASE_URL"] = f"sqlite:///{DEMO_PATH}"

from app import create_app
from app.extensions import db
from app.models.user import ROLE_ADMIN, ROLE_SELLER, User
from app.services import inventory_service
from seed_catalog import seed_categories, seed_products

# Stock inicial de la demo (deja historial de movimientos real)
INITIAL_STOCK = {
    "MES3107": 20,   # labial: disponible
    "MES3371": 15,   # juguete: disponible
    "MES2655-2": 3,  # tulipán: baja disponibilidad (umbral 5)
}


def create_demo_user(username, full_name, role, password):
    """Crea un usuario de demostración con su contraseña hasheada."""
    user = User(username=username, full_name=full_name, role=role)
    user.set_password(password)
    db.session.add(user)
    return user


if __name__ == "__main__":
    app = create_app()

    with app.app_context():
        print("=== Generar base de demostración para el deploy ===")

        admin = create_demo_user("admin", "Administrador Los Altos", ROLE_ADMIN, "admin123")
        create_demo_user("vendedor", "Vendedor Demo", ROLE_SELLER, "venta123")
        db.session.commit()
        print("Usuarios de demo: admin/admin123 y vendedor/venta123")

        print("Categorías/subcategorías nuevas:", seed_categories())
        print("Productos nuevos:", seed_products())

        from app.models.product import Product
        for code, quantity in INITIAL_STOCK.items():
            product = Product.query.filter_by(code=code).first()
            ok, message = inventory_service.register_movement(
                product, admin, "entrada", quantity, "Carga inicial de demostración"
            )
            print("-", message)

        print(f"\nBase de demostración lista: {DEMO_PATH}")
