# ==========================================================
# Script de consola para crear el usuario administrador de prueba.
#
# Se ejecuta desde la terminal (con el entorno virtual activo):
#
#     python seed_admin.py
#
# Pide los datos por consola con input() y, si se deja un campo
# vacío, usa el valor por defecto. La contraseña se guarda como
# hash, nunca en texto plano.
# ==========================================================
from app import create_app
from app.extensions import db
from app.models.user import ROLE_ADMIN, User

# Valores por defecto del usuario de prueba (solo para desarrollo)
DEFAULT_USERNAME = "admin"
DEFAULT_FULL_NAME = "Administrador Los Altos"
DEFAULT_PASSWORD = "admin123"


def ask_value(label, default):
    """Pide un dato por consola; si queda vacío regresa el valor por defecto."""
    value = input(f"{label} [{default}]: ").strip()
    if value == "":
        return default
    return value


def create_admin_user(username, full_name, password):
    """Crea el usuario administrador si el username no existe todavía.

    Regresa el usuario creado, o None si ya existía uno con ese username
    (el username es único en la tabla users).
    """
    existing = User.query.filter_by(username=username).first()
    if existing is not None:
        return None

    user = User(username=username, full_name=full_name, role=ROLE_ADMIN)
    user.set_password(password)  # se guarda el hash, no la contraseña

    db.session.add(user)
    db.session.commit()
    return user


if __name__ == "__main__":
    app = create_app()

    # Necesitamos el contexto de la aplicación para usar la base de datos
    with app.app_context():
        print("=== Crear usuario administrador de prueba ===")

        username = ask_value("Usuario", DEFAULT_USERNAME)
        full_name = ask_value("Nombre completo", DEFAULT_FULL_NAME)
        password = ask_value("Contraseña", DEFAULT_PASSWORD)

        user = create_admin_user(username, full_name, password)

        if user is None:
            print(f"El usuario '{username}' ya existe. No se creó nada.")
        else:
            print(f"Usuario administrador '{user.username}' creado correctamente.")
