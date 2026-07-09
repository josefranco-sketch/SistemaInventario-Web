# ==========================================================
# Formularios del panel administrativo (Flask-WTF).
# ==========================================================
from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed, FileField
from wtforms import (
    DecimalField,
    HiddenField,
    IntegerField,
    PasswordField,
    SelectField,
    StringField,
    TextAreaField,
)
from wtforms.validators import (
    DataRequired,
    EqualTo,
    Length,
    NumberRange,
    Optional,
)

from app.models.inventory import MANUAL_MOVEMENT_TYPES, MOVEMENT_LABELS
from app.models.product import COMMERCIAL_UNITS
from app.models.user import ROLE_ADMIN, ROLE_SELLER


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

    image_file = FileField(
        "Imagen del producto",
        validators=[
            FileAllowed(
                ["png", "jpg", "jpeg", "webp"],
                message="Solo se permiten imágenes PNG, JPG o WEBP.",
            ),
        ],
    )


class StatusChangeForm(FlaskForm):
    """Formulario mínimo para cambiar el estado de un producto.

    Existe para que el cambio de estado viaje por POST con token
    CSRF, nunca por un enlace GET.
    """

    status = HiddenField(validators=[DataRequired()])


class MovementForm(FlaskForm):
    """Formulario para registrar una entrada o salida de inventario.

    El motivo es obligatorio: cada movimiento debe dejar historial
    con usuario, fecha y motivo (regla ADR, sin excepción).
    """

    movement_type = SelectField(
        "Tipo de movimiento",
        # Solo entrada/salida: el tipo "venta" lo genera el sistema
        # al pagar un pedido, nunca se registra a mano.
        choices=[(value, MOVEMENT_LABELS[value]) for value in MANUAL_MOVEMENT_TYPES],
        validators=[DataRequired(message="Elige el tipo de movimiento.")],
    )

    quantity = IntegerField(
        "Cantidad",
        validators=[
            DataRequired(message="La cantidad es obligatoria."),
            NumberRange(min=1, message="La cantidad debe ser mayor a cero."),
        ],
    )

    reason = StringField(
        "Motivo",
        validators=[
            DataRequired(message="El motivo es obligatorio."),
            Length(max=200, message="Máximo 200 caracteres."),
        ],
    )


class ThresholdsForm(FlaskForm):
    """Formulario vacío: aporta el token CSRF a la pantalla de
    umbrales, cuyos campos se generan dinámicamente por
    subcategoría en el template."""


class ConfirmActionForm(FlaskForm):
    """Formulario vacío: aporta el token CSRF a acciones POST
    simples (ej. activar/inactivar un usuario)."""


class UserBaseForm(FlaskForm):
    """Campos comunes de los formularios de usuario interno."""

    username = StringField(
        "Usuario",
        validators=[
            DataRequired(message="El usuario es obligatorio."),
            Length(min=3, max=50, message="Entre 3 y 50 caracteres."),
        ],
    )

    full_name = StringField(
        "Nombre completo",
        validators=[
            DataRequired(message="El nombre es obligatorio."),
            Length(max=120, message="Máximo 120 caracteres."),
        ],
    )

    role = SelectField(
        "Rol",
        choices=[(ROLE_ADMIN, "Administrador"), (ROLE_SELLER, "Vendedor")],
        validators=[DataRequired(message="Elige un rol.")],
    )


class UserCreateForm(UserBaseForm):
    """Alta de usuario: la contraseña es obligatoria."""

    password = PasswordField(
        "Contraseña",
        validators=[
            DataRequired(message="La contraseña es obligatoria."),
            Length(min=6, message="Mínimo 6 caracteres."),
        ],
    )

    confirm_password = PasswordField(
        "Confirmar contraseña",
        validators=[
            DataRequired(message="Confirma la contraseña."),
            EqualTo("password", message="Las contraseñas no coinciden."),
        ],
    )


class UserEditForm(UserBaseForm):
    """Edición de usuario: la contraseña es opcional (en blanco
    se conserva la actual). Nunca se muestra la existente."""

    password = PasswordField(
        "Nueva contraseña (opcional)",
        validators=[
            Optional(),
            Length(min=6, message="Mínimo 6 caracteres."),
        ],
    )

    confirm_password = PasswordField(
        "Confirmar nueva contraseña",
        validators=[
            EqualTo("password", message="Las contraseñas no coinciden."),
        ],
    )

