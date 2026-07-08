# ==========================================================
# Servicio de productos.
#
# Toda la lógica de negocio del módulo de productos vive aquí:
# búsquedas con filtros, creación/edición validando el código
# único, cambios de estado (nunca eliminación física) y la regla
# de venta mínima por categoría (ADR / Documento 6).
# ==========================================================
from decimal import Decimal

from app.extensions import db
from app.models.category import Category, Subcategory
from app.models.product import PRODUCT_STATUSES, Product


# ----------------------------------------------------------
# Consultas
# ----------------------------------------------------------

def list_products(search="", category_id=None, status=""):
    """Regresa los productos aplicando los filtros del listado admin."""
    query = Product.query

    if search:
        like = f"%{search}%"
        query = query.filter(
            db.or_(
                Product.code.ilike(like),
                Product.name.ilike(like),
                Product.description.ilike(like),
            )
        )

    if category_id:
        query = query.join(Subcategory).filter(
            Subcategory.category_id == category_id
        )

    if status in PRODUCT_STATUSES:
        query = query.filter(Product.status == status)

    return query.order_by(Product.code).all()


def get_product_or_none(product_id):
    return db.session.get(Product, product_id)


def code_already_exists(code, exclude_id=None):
    """Verifica si un código ya está usado por otro producto."""
    query = Product.query.filter(Product.code == code)
    if exclude_id is not None:
        query = query.filter(Product.id != exclude_id)
    return query.first() is not None


def get_all_categories():
    return Category.query.order_by(Category.name).all()


def get_subcategory_choices():
    """Choices agrupados por categoría para el SelectField del formulario.

    Formato de WTForms para <optgroup>:
        {"Cosméticos": [(1, "Labiales"), ...], "Juguetes": [...]}
    """
    choices = {}
    for category in get_all_categories():
        options = []
        for subcategory in category.subcategories:
            options.append((subcategory.id, subcategory.name))
        if options:
            choices[category.name] = options
    return choices


# ----------------------------------------------------------
# Crear y editar
# ----------------------------------------------------------

def _normalize_code(code):
    """Los códigos se guardan sin espacios y en mayúsculas (ej. MES3107)."""
    return code.strip().upper()


def _clean_optional(value):
    """Limpia un campo de texto opcional.

    Regresa None si el campo viene vacío o no viene en el
    formulario, para guardar NULL en lugar de cadenas vacías.
    """
    if value is None:
        return None
    value = value.strip()
    if value == "":
        return None
    return value


def create_product(form):
    """Crea un producto desde el formulario validado.

    Regresa (producto, None) si se creó, o (None, mensaje de error)
    si el código ya existe (el código del producto es único).
    """
    code = _normalize_code(form.code.data)

    if code_already_exists(code):
        return None, f"El código {code} ya está usado por otro producto."

    product = Product(
        code=code,
        name=form.name.data.strip(),
        description=_clean_optional(form.description.data),
        brand=_clean_optional(form.brand.data),
        subcategory_id=form.subcategory_id.data,
        price=form.price.data,
        commercial_presentation=form.commercial_presentation.data.strip(),
        commercial_unit=form.commercial_unit.data,
        availability=form.availability.data,
        image_filename=_clean_optional(form.image_filename.data),
    )

    db.session.add(product)
    db.session.commit()
    return product, None


def update_product(product, form):
    """Actualiza un producto existente desde el formulario validado.

    Regresa (producto, None) si se guardó, o (None, mensaje de error)
    si el nuevo código chocaría con otro producto.
    """
    code = _normalize_code(form.code.data)

    if code_already_exists(code, exclude_id=product.id):
        return None, f"El código {code} ya está usado por otro producto."

    product.code = code
    product.name = form.name.data.strip()
    product.description = _clean_optional(form.description.data)
    product.brand = _clean_optional(form.brand.data)
    product.subcategory_id = form.subcategory_id.data
    product.price = form.price.data
    product.commercial_presentation = form.commercial_presentation.data.strip()
    product.commercial_unit = form.commercial_unit.data
    product.availability = form.availability.data
    product.image_filename = _clean_optional(form.image_filename.data)

    db.session.commit()
    return product, None


# ----------------------------------------------------------
# Cambio de estado (NUNCA eliminación física)
# ----------------------------------------------------------

def change_status(product, new_status):
    """Cambia el estado del producto entre activo/inactivo/archivado.

    Los productos jamás se eliminan de la base de datos (regla ADR);
    esta función es la única forma de "quitarlos" del sistema.
    Regresa (True, mensaje) o (False, mensaje de error).
    """
    if new_status not in PRODUCT_STATUSES:
        return False, "Estado de producto no válido."

    if product.status == new_status:
        return False, f"El producto ya está {product.status_label.lower()}."

    product.status = new_status
    db.session.commit()
    return True, f"Producto {product.code} ahora está {product.status_label.lower()}."


# ----------------------------------------------------------
# Regla de venta mínima por categoría (ADR / Documento 6)
# ----------------------------------------------------------

def get_minimum_sale(product):
    """Unidades mínimas de venta según la categoría del producto.

    - Cosméticos: se venden por caja o display completo (mínimo 1).
    - Juguetes: precio mayor a Q20 → 3 unidades; Q20 o menos → 6
      unidades (media docena, que cubre también los menores a Q15).
    - Flores: mínimo 3 ramos por código.
    """
    slug = product.category.slug

    if slug == "cosmetics":
        return 1

    if slug == "toys":
        if product.price > Decimal("20"):
            return 3
        return 6

    if slug == "flowers":
        return 3

    return 1
