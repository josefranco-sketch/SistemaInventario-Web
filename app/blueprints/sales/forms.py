# ==========================================================
# Formularios del módulo de ventas (Flask-WTF).
# ==========================================================
from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired, Length, Optional


class CsrfOnlyForm(FlaskForm):
    """Formulario vacío: aporta el token CSRF a las acciones POST
    del pedido (agregar, incrementar, disminuir, quitar)."""


class ConfirmOrderForm(FlaskForm):
    """Datos básicos del cliente para confirmar el pedido.

    El nombre es obligatorio (hay que saber a quién se le vende);
    el teléfono es opcional.
    """

    customer_name = StringField(
        "Nombre del cliente",
        validators=[
            DataRequired(message="El nombre del cliente es obligatorio."),
            Length(max=120, message="Máximo 120 caracteres."),
        ],
    )

    customer_phone = StringField(
        "Teléfono (opcional)",
        validators=[Optional(), Length(max=30, message="Máximo 30 caracteres.")],
    )
