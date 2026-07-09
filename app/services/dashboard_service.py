# ==========================================================
# Servicio del dashboard administrativo.
#
# Calcula los indicadores (KPIs) que muestra el panel. La vista
# solo presenta lo que este servicio entrega; ningún cálculo
# vive en el template.
#
# Desde el Sprint 6.2 todos los indicadores son reales (las
# cotizaciones ya se persisten en base de datos).
# ==========================================================
from app.models.product import STATUS_ACTIVE, Product
from app.models.user import User
from app.services.inventory_service import count_low_stock
from app.services.orders_service import count_recent_orders
from app.services.quotes_service import count_pending_quotes


def get_dashboard_summary():
    """Regresa un diccionario con los indicadores del dashboard."""
    summary = {
        # Real desde el Sprint 4.3: la tabla products ya existe
        "total_products": Product.query.count(),
        "active_products": Product.query.filter_by(status=STATUS_ACTIVE).count(),

        # Real desde el Sprint 4.4: productos activos en bajo stock
        "low_stock": count_low_stock(),

        # Real desde el Sprint 6.2: cotizaciones pendientes de atender
        "pending_quotes": count_pending_quotes(),

        # Real desde el Sprint 5.4: pedidos de los últimos 7 días
        "recent_orders": count_recent_orders(days=7),

        # Real: la tabla users ya existe desde el Sprint 4.1
        "total_users": User.query.count(),

        # Todos los indicadores son reales desde el Sprint 6.2
        "demo_data": False,
    }
    return summary
