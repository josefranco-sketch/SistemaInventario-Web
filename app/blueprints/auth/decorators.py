# ==========================================================
# Decoradores de autorización por rol.
#
# @login_required (de Flask-Login) verifica que exista sesión.
# Estos decoradores agregan la segunda capa: verificar el rol.
# ==========================================================
from functools import wraps

from flask import flash, redirect, url_for
from flask_login import current_user


def admin_required(view_func):
    """Permite el acceso únicamente a usuarios con rol administrador.

    Se usa después de @login_required, así que aquí ya existe una
    sesión iniciada; solo falta confirmar el rol.
    """

    @wraps(view_func)
    def wrapper(*args, **kwargs):
        if not current_user.is_authenticated or not current_user.is_admin():
            flash("No tienes permisos para entrar a esta sección.", "warning")
            return redirect(url_for("public.home"))
        return view_func(*args, **kwargs)

    return wrapper
