# ==========================================================
# Rutas del módulo de autenticación: login y logout.
#
# Las rutas solo manejan HTTP (formulario, redirecciones y
# mensajes). La validación de credenciales vive en
# app/services/auth_service.py.
# ==========================================================
from flask import flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required, login_user, logout_user

from app.blueprints.auth import auth_bp
from app.blueprints.auth.forms import LoginForm
from app.services.auth_service import authenticate_user


def _safe_next_url(next_url):
    """Solo acepta rutas internas del sitio (que empiezan con "/").

    Evita que alguien use el parámetro ?next= para redirigir
    la sesión hacia un sitio externo.
    """
    if next_url and next_url.startswith("/") and not next_url.startswith("//"):
        return next_url
    return None


def _redirect_after_login(user):
    """Decide a dónde enviar al usuario según su rol."""
    if user.is_admin():
        return redirect(url_for("admin.dashboard"))

    # Los vendedores van a su panel de ventas (Fase 5)
    return redirect(url_for("sales.panel"))


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    # Si ya hay sesión iniciada, no tiene sentido mostrar el login.
    if current_user.is_authenticated:
        return _redirect_after_login(current_user)

    form = LoginForm()

    if form.validate_on_submit():
        user = authenticate_user(form.username.data.strip(), form.password.data)

        if user is None:
            # Mensaje genérico: no revelamos si falló el usuario o la contraseña.
            flash("Usuario o contraseña incorrectos.", "danger")
        else:
            login_user(user)
            flash(f"Bienvenido, {user.full_name}.", "success")

            # Si venía de una ruta protegida, lo regresamos ahí.
            next_url = _safe_next_url(request.args.get("next"))
            if next_url:
                return redirect(next_url)

            return _redirect_after_login(user)

    return render_template("auth/login.html", form=form)


@auth_bp.route("/logout")
@login_required
def logout():
    logout_user()
    flash("Sesión cerrada correctamente.", "info")
    return redirect(url_for("auth.login"))
