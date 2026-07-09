# ==========================================================
# Servicio de ventas.
#
# Sprint 5.1: búsqueda de productos para el vendedor.
# Los productos vienen SIEMPRE de la fuente única (modelo
# Product); aquí solo se decide qué puede ver el vendedor:
# - Únicamente productos con estado "activo" (inactivos y
#   archivados no se venden).
# - El vendedor sí ve el stock exacto (regla ADR: solo el
#   cliente público tiene el stock oculto).
# - Se muestra la venta mínima por categoría, que el vendedor
#   necesita para armar pedidos (Sprint 5.2).
# ==========================================================
from app.models.product import STATUS_ACTIVE, UNIT_PLURALS
from app.services import inventory_service, products_service


def minimum_sale_label(product, minimum):
    """Etiqueta legible de la venta mínima ("1 caja", "3 unidades")."""
    unit = product.commercial_unit
    if minimum == 1:
        return f"1 {unit.lower()}"
    plural = UNIT_PLURALS.get(unit, unit.lower() + "s")
    return f"{minimum} {plural}"


def search_products_for_sale(search="", category_id=None):
    """Productos activos que el vendedor puede ofrecer.

    Reutiliza el buscador del servicio de productos (código,
    nombre y descripción) fijando el estado en "activo", y le
    agrega los datos operativos que el vendedor necesita.
    """
    products = products_service.list_products(
        search=search,
        category_id=category_id,
        status=STATUS_ACTIVE,
    )

    results = []
    for product in products:
        minimum = products_service.get_minimum_sale(product)
        results.append({
            "product": product,
            "stock": inventory_service.get_stock(product),
            "minimum_sale": minimum,
            "minimum_label": minimum_sale_label(product, minimum),
        })

    return results
