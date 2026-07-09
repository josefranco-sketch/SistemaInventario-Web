# ==========================================================
# Modelo de Usuario interno del sistema.
#
# Representa a las personas que pueden iniciar sesión en el
# panel interno: administradores y vendedores.
#
# Reglas importantes:
# - La contraseña NUNCA se guarda en texto plano, solo su hash.
# - Los usuarios no se eliminan: se activan o inactivan.
# ==========================================================
from flask_login import UserMixin
from werkzeug.security import check_password_hash, generate_password_hash

from app.extensions import db

# Roles internos permitidos en el sistema.
ROLE_ADMIN = "admin"
ROLE_SELLER = "vendedor"


class User(UserMixin, db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    full_name = db.Column(db.String(120), nullable=False)
    role = db.Column(db.String(20), nullable=False, default=ROLE_SELLER)

    # Un usuario inactivo no puede iniciar sesión (Flask-Login
    # también revisa este campo automáticamente).
    is_active = db.Column(db.Boolean, nullable=False, default=True)

    password_hash = db.Column(db.String(255), nullable=False)

    def set_password(self, password):
        """Convierte la contraseña en hash antes de guardarla."""
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        """Compara una contraseña escrita con el hash guardado."""
        return check_password_hash(self.password_hash, password)

    def is_admin(self):
        """Indica si el usuario tiene rol de administrador."""
        return self.role == ROLE_ADMIN

    def __repr__(self):
        return f"<User {self.username} ({self.role})>"
