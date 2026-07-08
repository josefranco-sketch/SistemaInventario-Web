# ==========================================================
# Script de consola para sembrar el catálogo inicial:
# categorías, subcategorías y los productos de demostración
# que ya se usaban en el catálogo público.
#
# Se ejecuta desde la terminal (con el entorno virtual activo):
#
#     python seed_catalog.py
#
# Es seguro correrlo varias veces: no duplica registros, solo
# crea lo que falte (el producto es fuente única — regla ADR).
# ==========================================================
from app import create_app
from app.extensions import db
from app.models.category import Category, Subcategory
from app.models.product import Product

# Categorías fijas del negocio con sus subcategorías iniciales.
# El umbral de bajo stock por subcategoría se afinará en el 4.4.
CATALOG = {
    "Cosméticos": {
        "slug": "cosmetics",
        "subcategories": ["Labiales", "Uñas", "Maquillaje"],
    },
    "Juguetes": {
        "slug": "toys",
        "subcategories": ["Comida", "Muñecas", "Carros"],
    },
    "Flores": {
        "slug": "flowers",
        "subcategories": ["Tulipanes", "Rosas", "Girasoles"],
    },
}

# Productos iniciales (los mismos que mostraba el catálogo público)
PRODUCTS = [
    {
        "code": "MES3107",
        "name": "Labial Matte Baolishi",
        "brand": "Baolishi",
        "category": "Cosméticos",
        "subcategory": "Labiales",
        "price": 144.00,
        "commercial_presentation": "Caja x 24 labiales",
        "commercial_unit": "Caja",
        "availability": "disponible",
        "description": "Labial en barra matte, gama de colores exclusiva, embase de alta calidad.",
        "image_filename": "labial-mate-mes3107.png",
    },
    {
        "code": "MES3371",
        "name": "Set de Comida Rápida",
        "brand": None,
        "category": "Juguetes",
        "subcategory": "Comida",
        "price": 21.00,
        "commercial_presentation": "Unidad",
        "commercial_unit": "Unidad",
        "availability": "disponible",
        "description": "Juguete set de comida rápida armable.",
        "image_filename": "juguete.png",
    },
    {
        "code": "MES2655-2",
        "name": "Tulipán Rojo",
        "brand": None,
        "category": "Flores",
        "subcategory": "Tulipanes",
        "price": 36.00,
        "commercial_presentation": "Ramo de 12 unidades",
        "commercial_unit": "Ramo",
        "availability": "agotado",
        "description": "Ramo de tulipanes rojos de 33 cm de alto.",
        "image_filename": "tulipan-rojo.png",
    },
]


def seed_categories():
    """Crea las categorías y subcategorías que falten.

    Regresa cuántos registros nuevos se crearon.
    """
    created = 0

    for name, data in CATALOG.items():
        category = Category.query.filter_by(slug=data["slug"]).first()
        if category is None:
            category = Category(name=name, slug=data["slug"])
            db.session.add(category)
            db.session.flush()  # asigna el id sin cerrar la transacción
            created += 1

        for sub_name in data["subcategories"]:
            exists = Subcategory.query.filter_by(
                category_id=category.id, name=sub_name
            ).first()
            if exists is None:
                db.session.add(Subcategory(name=sub_name, category_id=category.id))
                created += 1

    db.session.commit()
    return created


def seed_products():
    """Crea los productos iniciales que falten (el código es único).

    Regresa cuántos productos nuevos se crearon.
    """
    created = 0

    for data in PRODUCTS:
        if Product.query.filter_by(code=data["code"]).first() is not None:
            continue  # ya existe, no se duplica

        category = Category.query.filter_by(name=data["category"]).first()
        subcategory = Subcategory.query.filter_by(
            category_id=category.id, name=data["subcategory"]
        ).first()

        product = Product(
            code=data["code"],
            name=data["name"],
            brand=data["brand"],
            description=data["description"],
            subcategory_id=subcategory.id,
            price=data["price"],
            commercial_presentation=data["commercial_presentation"],
            commercial_unit=data["commercial_unit"],
            availability=data["availability"],
            image_filename=data["image_filename"],
        )
        db.session.add(product)
        created += 1

    db.session.commit()
    return created


if __name__ == "__main__":
    app = create_app()

    with app.app_context():
        print("=== Sembrar catálogo inicial ===")

        new_catalog = seed_categories()
        print(f"Categorías/subcategorías nuevas: {new_catalog}")

        new_products = seed_products()
        print(f"Productos nuevos: {new_products}")

        print(f"Total de productos en la base: {Product.query.count()}")
