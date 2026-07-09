# ==========================================================
# Servicio del dashboard administrativo.
#
# Calcula los indicadores (KPIs) que muestra el panel. La vista
# solo presenta lo que este servicio entrega; ningún cálculo
# vive en el template.
#
# NOTA: cotizaciones y ventas todavía no tienen modelos reales
# en la base de datos (llegan en las Fases 5-6). Mientras tanto,
# esos indicadores entregan valores de demostración claramente
# marcados con la bandera "demo_data".
# ==========================================================
from app.models.product import STATUS_ACTIVE, Product
from app.models.user import User
from app.services.inventory_service import count_low_stock


def get_dashboard_summary():
    """Regresa un diccionario con los indicadores del dashboard."""
    summary = {
        # Real desde el Sprint 4.3: la tabla products ya existe
        "total_products": Product.query.count(),
        "active_products": Product.query.filter_by(status=STATUS_ACTIVE).count(),

        # Real desde el Sprint 4.4: productos activos en bajo stock
        "low_stock": count_low_stock(),

        # Demo: las cotizaciones persistidas llegan en la Fase 6
        "pending_quotes": 0,

        # Demo: los pedidos/ventas llegan en la Fase 5
        "recent_orders": 0,

        # Real: la tabla users ya existe desde el Sprint 4.1
        "total_users": User.query.count(),

        # Bandera para que la vista avise que hay datos de demostración
        "demo_data": True,
    }
    return summary
