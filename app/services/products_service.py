# ==========================================================
# Servicio de productos.
#
# Toda la lógica de negocio del módulo de productos vive aquí:
# búsquedas con filtros, creación/edición validando el código
# único, cambios de estado (nunca eliminación física) y la regla
# de venta mínima por categoría (ADR / Documento 6).
# ==========================================================
import os
from decimal import Decimal

from flask import current_app
from werkzeug.utils import secure_filename

from app.extensions import db
from app.models.category import Category, Subcategory
from app.models.product import AVAILABILITY_OUT, PRODUCT_STATUSES, Product

# Extensiones de imagen aceptadas (el formulario también las valida)
ALLOWED_IMAGE_EXTENSIONS = {".png", ".jpg", ".jpeg", ".webp"}


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


def save_product_image(image_file, code):
    """Guarda la imagen subida en static/img/products/ y regresa
    el nombre final del archivo (o None si no hay imagen válida).

    El archivo se nombra con el código único del producto (ej.
    "mes3107.png"): así nunca chocan imágenes de dos productos y
    volver a subir una imagen reemplaza la anterior.
    """
    if image_file is None or not image_file.filename:
        return None

    original = secure_filename(image_file.filename)
    extension = os.path.splitext(original)[1].lower()

    if extension not in ALLOWED_IMAGE_EXTENSIONS:
        return None  # doble seguridad: el formulario ya lo valida

    filename = f"{code.lower()}{extension}"
    folder = os.path.join(current_app.root_path, "static", "img", "products")
    os.makedirs(folder, exist_ok=True)

    image_file.save(os.path.join(folder, filename))
    return filename


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
        # Un producto nuevo nace sin stock, por lo tanto agotado; la
        # disponibilidad la recalcula el inventario con cada movimiento.
        availability=AVAILABILITY_OUT,
        image_filename=save_product_image(form.image_file.data, code),
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

    subcategory_changed = product.subcategory_id != form.subcategory_id.data

    product.code = code
    product.name = form.name.data.strip()
    product.description = _clean_optional(form.description.data)
    product.brand = _clean_optional(form.brand.data)
    product.subcategory_id = form.subcategory_id.data
    product.price = form.price.data
    product.commercial_presentation = form.commercial_presentation.data.strip()
    product.commercial_unit = form.commercial_unit.data
    # La disponibilidad pública ya no se edita a mano: la calcula el
    # inventario según stock y umbral de la subcategoría (Sprint 4.4).

    if subcategory_changed:
        # Cambiar de subcategoría puede cambiar el umbral de bajo
        # stock, así que la disponibilidad pública se recalcula
        # (brecha detectada y corregida en el Sprint 6.3).
        # Se asigna la RELACIÓN (no solo el id) para que el umbral
        # nuevo esté disponible de inmediato en el recálculo.
        from app.services import inventory_service

        product.subcategory = db.session.get(
            Subcategory, form.subcategory_id.data
        )
        inventory_service.refresh_availability(product)

    # Solo se reemplaza la imagen si el admin subió un archivo nuevo;
    # si no sube nada, se conserva la imagen actual.
    new_image = save_product_image(form.image_file.data, code)
    if new_image is not None:
        product.image_filename = new_image

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
