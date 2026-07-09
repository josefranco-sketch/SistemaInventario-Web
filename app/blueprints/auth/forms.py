# ==========================================================
# Formularios del módulo de autenticación (Flask-WTF).
#
# Flask-WTF agrega automáticamente el token CSRF a cada
# formulario, protegiendo el login contra envíos falsificados.
# ==========================================================
from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField
from wtforms.validators import DataRequired, Length


class LoginForm(FlaskForm):
    username = StringField(
        "Usuario",
        validators=[
            DataRequired(message="Escribe tu usuario."),
            Length(max=50, message="El usuario es demasiado largo."),
        ],
    )

    password = PasswordField(
        "Contraseña",
        validators=[DataRequired(message="Escribe tu contraseña.")],
    )
