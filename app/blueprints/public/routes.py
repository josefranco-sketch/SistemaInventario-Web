# Rutas del módulo público
from flask import render_template, request, url_for

from app.blueprints.public import public_bp

# Página de Inicio

# Cuando el usuario entra a "/", Flask renderiza el Home.
@public_bp.route("/")
def home():
    return render_template("public/home.html")

# Página del Catálogo
# Muestra el catálogo público.
#
# Por el momento enviamos una lista vacía porque el módulo
# de Productos todavía no existe.
#
# En el Sprint de Productos esta lista será reemplazada
# por los datos obtenidos desde la base de datos.
# ==========================================================
@public_bp.route("/catalog")
def catalog():
    # ==========================================================
    # Datos reales de prueba del catálogo.
    # Más adelante esto será reemplazado por ProductService.
    # ==========================================================

    products = [
        {
            "name": "Labial Matte Baolishi",
            "code": "MES3107",
            "brand": "Baolishi",
            "category_name": "Cosméticos",
            "subcategory_name": "Labiales",
            "price": "Q 144.00",
            "commercial_presentation": "Caja x 24 labiales",
            "commercial_unit": "Caja",
            "minimum_sale": 1,
            "availability_level": "disponible",
            "availability_label": "Disponible",
            "description": "Labial en barra matte, gama de colores exclusiva, embase de alta calidad.",
            "image_url": url_for(
                "static",
                filename="img/products/labial-mate-mes3107.png"
            ),
        },
        {
            "name": "Set de Comida Rápida",
            "code": "MES3371",
            "brand": None,
            "category_name": "Juguetes",
            "subcategory_name": "Comida",
            "price": "Q 21.00",
            "commercial_presentation": "Unidad",
            "commercial_unit": "Unidad",
            "minimum_sale": 3,
            "availability_level": "disponible",
            "availability_label": "Disponible",
            "description": "Juguete set de comida rápida armable.",
            "image_url": url_for(
                "static",
                filename="img/products/juguete.png"
            ),
        },
        {
            "name": "Tulipán Rojo",
            "code": "MES2655-2",
            "brand": None,
            "category_name": "Flores",
            "subcategory_name": "Tulipanes",
            "price": "Q 36.00",
            "commercial_presentation": "Ramo de 12 unidades",
            "commercial_unit": "Ramo",
            "minimum_sale": 3,
            "availability_level": "agotado",
            "availability_label": "Agotado",
            "description": "Ramo de tulipanes rojos de 33 cm de alto.",
            "image_url": url_for(
                "static",
                filename="img/products/tulipan-rojo.png"
            ),
        },
    ]

    # ==========================================================
    # Construcción dinámica de categorías y subcategorías
    # a partir de los productos disponibles.
    # ==========================================================

    categories = sorted({product["category_name"] for product in products})

    subcategories = {}
    for category_name in categories:
        subcategories[category_name] = sorted({
            product["subcategory_name"]
            for product in products
            if product["category_name"] == category_name
        })

    # ==========================================================
    # Filtros enviados por la URL
    # ==========================================================
    query = request.args.get("q", "").strip().lower()
    selected_category = request.args.get("category", "").strip()
    selected_subcategory = request.args.get("subcategory", "").strip()
    availability = request.args.get("availability", "").strip().lower()

    filtered_products = products

    if query:
        filtered_products = [
            product for product in filtered_products
            if (
                query in product["name"].lower()
                or query in product["code"].lower()
                or query in product["description"].lower()
            )
        ]

    if selected_category:
        filtered_products = [
            product for product in filtered_products
            if product["category_name"] == selected_category
        ]

    if selected_subcategory:
        filtered_products = [
            product for product in filtered_products
            if product["subcategory_name"] == selected_subcategory
        ]

    if availability:
        filtered_products = [
            product for product in filtered_products
            if product["availability_level"] == availability
        ]

    # Si hay categoría seleccionada, solo mostramos sus subcategorías.
    visible_subcategories = []
    if selected_category and selected_category in subcategories:
        visible_subcategories = subcategories[selected_category]

    return render_template(
        "public/catalog.html",
        products=filtered_products,
        categories=categories,
        subcategories=visible_subcategories,
        selected_category=selected_category,
        selected_subcategory=selected_subcategory
    )