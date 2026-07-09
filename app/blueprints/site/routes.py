# ==========================================================
# Rutas del módulo público.
#
# Desde el Sprint 6.1 el catálogo lee los productos REALES de la
# base de datos a través de catalog_service (los datos de prueba
# de la Fase 3 fueron eliminados). El cliente público solo ve
# productos activos y nunca el stock exacto.
# ==========================================================
from flask import abort, render_template, request

from app.blueprints.site import public_bp
from app.services import catalog_service


# Página de Inicio
# Cuando el usuario entra a "/", Flask renderiza el Home.
@public_bp.route("/")
def home():
    return render_template("site/home.html")


# Página del Catálogo
# Muestra los productos reales (solo activos) con filtros por
# texto, categoría, subcategoría y disponibilidad.
@public_bp.route("/catalog")
def catalog():
    # Filtros enviados por la URL
    query = request.args.get("q", "").strip()
    selected_category = request.args.get("category", "").strip()
    selected_subcategory = request.args.get("subcategory", "").strip()
    availability = request.args.get("availability", "").strip().lower()

    products = catalog_service.get_public_products(
        search=query,
        category_name=selected_category,
        subcategory_name=selected_subcategory,
        availability=availability,
    )

    categories, subcategories = catalog_service.get_filter_options()

    # Si hay categoría seleccionada, solo mostramos sus subcategorías.
    visible_subcategories = []
    if selected_category and selected_category in subcategories:
        visible_subcategories = subcategories[selected_category]

    return render_template(
        "site/catalog.html",
        products=products,
        categories=categories,
        subcategories=visible_subcategories,
        selected_category=selected_category,
        selected_subcategory=selected_subcategory,
        selected_availability=availability,
        query=query,
    )


# Página de Detalle del Producto
# Muestra la ficha pública de un producto activo por su código.
@public_bp.route("/catalog/<string:product_code>")
def product_detail(product_code):
    product = catalog_service.get_public_product_by_code(product_code)

    if product is None:
        abort(404)

    return render_template(
        "site/product_detail.html",
        product=product,
        return_url=request.args.get("next"),
    )
