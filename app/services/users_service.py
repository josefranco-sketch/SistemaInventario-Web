# ==========================================================
# Servicio de usuarios internos.
#
# Lógica de negocio del módulo de usuarios:
# - Crear y editar usuarios validando username único.
# - Contraseña SIEMPRE como hash (nunca texto plano) y nunca
#   se muestra ni se recupera.
# - Activar/inactivar (los usuarios no se eliminan, igual que
#   los productos: así el historial de movimientos y las ventas
#   futuras nunca pierden a su autor).
# - Reglas de seguridad: un admin no puede desactivarse a sí
#   mismo ni quitarse su propio rol (evita quedar fuera del
#   sistema).
# ==========================================================
from app.extensions import db
from app.models.user import ROLE_ADMIN, ROLE_SELLER, User

VALID_ROLES = [ROLE_ADMIN, ROLE_SELLER]

ROLE_LABELS = {
    ROLE_ADMIN: "Administrador",
    ROLE_SELLER: "Vendedor",
}


# ----------------------------------------------------------
# Consultas
# ----------------------------------------------------------

def list_users(search="", role=""):
    """Usuarios internos con filtros para el listado admin."""
    query = User.query

    if search:
        like = f"%{search}%"
        query = query.filter(
            db.or_(User.username.ilike(like), User.full_name.ilike(like))
        )

    if role in VALID_ROLES:
        query = query.filter(User.role == role)

    return query.order_by(User.username).all()


def get_user_or_none(user_id):
    return db.session.get(User, user_id)


def username_already_exists(username, exclude_id=None):
    """Verifica si un username ya está usado por otro usuario."""
    query = User.query.filter(User.username == username)
    if exclude_id is not None:
        query = query.filter(User.id != exclude_id)
    return query.first() is not None


def _normalize_username(username):
    """Los usernames se guardan en minúsculas y sin espacios,
    para que "Admin" y "admin" no puedan coexistir."""
    return username.strip().lower()


# ----------------------------------------------------------
# Crear y editar
# ----------------------------------------------------------

def create_user(form):
    """Crea un usuario interno desde el formulario validado.

    Regresa (usuario, None) o (None, mensaje de error).
    """
    username = _normalize_username(form.username.data)

    if username_already_exists(username):
        return None, f"El usuario '{username}' ya existe."

    if form.role.data not in VALID_ROLES:
        return None, "Rol no válido."

    user = User(
        username=username,
        full_name=form.full_name.data.strip(),
        role=form.role.data,
    )
    user.set_password(form.password.data)  # se guarda el hash, jamás el texto

    db.session.add(user)
    db.session.commit()
    return user, None


def update_user(user, form, acting_user):
    """Actualiza un usuario existente.

    La contraseña solo cambia si se escribió una nueva (en blanco
    se conserva la actual). Un admin no puede cambiarse su propio
    rol. Regresa (usuario, None) o (None, mensaje de error).
    """
    username = _normalize_username(form.username.data)

    if username_already_exists(username, exclude_id=user.id):
        return None, f"El usuario '{username}' ya existe."

    if form.role.data not in VALID_ROLES:
        return None, "Rol no válido."

    if user.id == acting_user.id and form.role.data != user.role:
        return None, "No puedes cambiar tu propio rol."

    user.username = username
    user.full_name = form.full_name.data.strip()
    user.role = form.role.data

    # Contraseña opcional en edición: solo se reemplaza si viene algo
    if form.password.data:
        user.set_password(form.password.data)

    db.session.commit()
    return user, None


# ----------------------------------------------------------
# Activar / inactivar (nunca se elimina)
# ----------------------------------------------------------

def toggle_active(user, acting_user):
    """Activa o inactiva un usuario.

    Un usuario inactivo no puede iniciar sesión (lo valida el
    servicio de autenticación). Nadie puede desactivarse a sí
    mismo. Regresa (True/False, mensaje).
    """
    if user.id == acting_user.id:
        return False, "No puedes desactivar tu propio usuario."

    user.is_active = not user.is_active
    db.session.commit()

    if user.is_active:
        return True, f"Usuario '{user.username}' activado."
    return True, f"Usuario '{user.username}' inactivado; ya no podrá iniciar sesión."
