# ==========================================================
# Formularios del panel administrativo (Flask-WTF).
# ==========================================================
from flask_wtf import FlaskForm
from wtforms import (
    DecimalField,
    HiddenField,
    SelectField,
    StringField,
    TextAreaField,
)
from wtforms.validators import DataRequired, Length, NumberRange, Optional

from app.models.product import (
    AVAILABILITY_LABELS,
    COMMERCIAL_UNITS,
)


class ProductForm(FlaskForm):
    """Formulario para crear y editar productos.

    Las opciones de subcategoría se cargan desde la base de datos
    en la ruta (con products_service.get_subcategory_choices),
    porque WTForms necesita las choices en cada request.
    """

    code = StringField(
        "Código",
        validators=[
            DataRequired(message="El código es obligatorio."),
            Length(max=30, message="Máximo 30 caracteres."),
        ],
    )

    name = StringField(
        "Nombre",
        validators=[
            DataRequired(message="El nombre es obligatorio."),
            Length(max=120, message="Máximo 120 caracteres."),
        ],
    )

    description = TextAreaField(
        "Descripción",
        validators=[Optional(), Length(max=600, message="Máximo 600 caracteres.")],
        default="",
    )

    brand = StringField(
        "Marca",
        validators=[Optional(), Length(max=80, message="Máximo 80 caracteres.")],
        default="",
    )

    subcategory_id = SelectField(
        "Subcategoría",
        coerce=int,
        validators=[DataRequired(message="Elige una subcategoría.")],
    )

    price = DecimalField(
        "Precio (Q)",
        places=2,
        validators=[
            DataRequired(message="El precio es obligatorio."),
            NumberRange(min=0.01, message="El precio debe ser mayor a 0."),
        ],
    )

    commercial_presentation = StringField(
        "Presentación comercial",
        validators=[
            DataRequired(message="La presentación es obligatoria."),
            Length(max=120, message="Máximo 120 caracteres."),
        ],
    )

    commercial_unit = SelectField(
        "Unidad de venta",
        choices=[(unit, unit) for unit in COMMERCIAL_UNITS],
        validators=[DataRequired(message="Elige la unidad de venta.")],
    )

    availability = SelectField(
        "Disponibilidad pública",
        choices=[(level, label) for level, label in AVAILABILITY_LABELS.items()],
        validators=[DataRequired(message="Elige la disponibilidad.")],
    )

    image_filename = StringField(
        "Imagen (archivo en static/img/products/)",
        validators=[Optional(), Length(max=120, message="Máximo 120 caracteres.")],
        default="",
    )


class StatusChangeForm(FlaskForm):
    """Formulario mínimo para cambiar el estado de un producto.

    Existe para que el cambio de estado viaje por POST con token
    CSRF, nunca por un enlace GET.
    """

    status = HiddenField(validators=[DataRequired()])
