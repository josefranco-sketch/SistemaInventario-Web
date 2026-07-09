# ==========================================================
# Servicio del catálogo público.
#
# Es la ÚNICA puerta de los datos reales hacia el cliente:
# - Solo se muestran productos con estado ACTIVO (inactivos y
#   archivados desaparecen del catálogo).
# - El stock exacto JAMÁS sale de aquí (regla ADR): el cliente
#   solo recibe el nivel de disponibilidad y su etiqueta
#   (Disponible / Baja disponibilidad / Agotado).
# - Entrega diccionarios con la forma que los templates públicos
#   ya consumen, reemplazando los datos de prueba de la Fase 3.
# ==========================================================
from flask import url_for

from app.models.category import Category, Subcategory
from app.models.product import AVAILABILITY_LEVELS, STATUS_ACTIVE, Product
from app.services import products_service


def _public_view(product):
    """Convierte un producto real en la vista pública del catálogo.

    IMPORTANTE: aquí no se incluye el stock exacto — solo el nivel
    de disponibilidad con su etiqueta.
    """
    if product.image_filename:
        image_url = url_for(
            "static", filename=f"img/products/{product.image_filename}"
        )
    else:
        image_url = url_for("static", filename="img/products/placeholder.svg")

    return {
        "name": product.name,
        "code": product.code,
        "brand": product.brand,
        "category_name": product.category.name,
        "subcategory_name": product.subcategory.name,
        "price": f"Q {product.price:.2f}",
        "commercial_presentation": product.commercial_presentation,
        "commercial_unit": product.commercial_unit,
        "minimum_sale": products_service.get_minimum_sale(product),
        "availability_level": product.availability,
        "availability_label": product.availability_label,
        "description": product.description or "",
        "image_url": image_url,
    }


def get_public_products(search="", category_name="", subcategory_name="", availability=""):
    """Productos activos del catálogo público, con los filtros que
    viajan en la URL (texto, categoría, subcategoría, disponibilidad)."""
    query = (
        Product.query.filter(Product.status == STATUS_ACTIVE)
        .join(Subcategory)
        .join(Category)
    )

    if search:
        like = f"%{search}%"
        query = query.filter(
            Product.name.ilike(like)
            | Product.code.ilike(like)
            | Product.description.ilike(like)
        )

    if category_name:
        query = query.filter(Category.name == category_name)

    if subcategory_name:
        query = query.filter(Subcategory.name == subcategory_name)

    if availability in AVAILABILITY_LEVELS:
        query = query.filter(Product.availability == availability)

    products = query.order_by(Product.code).all()
    return [_public_view(product) for product in products]


def get_public_product_by_code(code):
    """Ficha pública de un producto activo, o None si no existe o
    no está activo (inactivos y archivados no se muestran)."""
    product = Product.query.filter_by(code=code, status=STATUS_ACTIVE).first()
    if product is None:
        return None
    return _public_view(product)


def get_filter_options():
    """Categorías y subcategorías reales para los filtros del catálogo.

    Regresa (lista de nombres de categoría, diccionario
    {categoría: [subcategorías]}), la misma estructura que el
    catálogo usaba con los datos de prueba.
    """
    categories = []
    subcategories = {}

    for category in Category.query.order_by(Category.name).all():
        categories.append(category.name)
        subcategories[category.name] = [
            subcategory.name for subcategory in category.subcategories
        ]

    return categories, subcategories
