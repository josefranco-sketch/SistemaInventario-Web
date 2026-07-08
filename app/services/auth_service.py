# ==========================================================
# Servicio de autenticación.
#
# Contiene la lógica de negocio del login: buscar al usuario,
# validar que esté activo y comparar la contraseña con el hash.
# Las rutas solo llaman a este servicio y deciden a dónde
# redirigir; nunca validan credenciales por su cuenta.
# ==========================================================
from app.models.user import User


def authenticate_user(username, password):
    """Valida credenciales y regresa el usuario si son correctas.

    Regresa None cuando el usuario no existe, está inactivo o la
    contraseña no coincide. La ruta muestra un solo mensaje genérico
    para no revelar cuál de los datos falló.
    """
    user = User.query.filter_by(username=username).first()

    if user is None:
        return None

    if not user.is_active:
        return None

    if not user.check_password(password):
        return None

    return user
