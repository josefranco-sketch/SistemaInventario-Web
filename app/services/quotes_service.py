# ==========================================================
# Servicio de cotizaciones.
#
# - Persiste la cotización que el cliente arma en su sesión del
#   sitio público (Sprint 6.2), enlazando cada renglón con el
#   producto existente (fuente única, nunca se duplica).
# - Convierte una cotización en pedido interno Pendiente de pago,
#   manteniendo cantidades y los precios que el cliente vio,
#   validando las reglas de venta mínima por categoría.
#
# REGLAS ADR: una cotización no maneja pagos y JAMÁS descuenta
# inventario; convertirla tampoco (el descuento ocurre solo al
# pagar el pedido, y ese código vive en orders_service).
# ==========================================================
import re

from app.extensions import db
from app.models.order import ORDER_PENDING, Order, OrderItem
from app.models.product import STATUS_ACTIVE, Product
from app.models.quote import (
    QUOTE_CONVERTED,
    QUOTE_DEPARTMENTS,
    QUOTE_PENDING,
    Quote,
    QuoteItem,
)
from app.services import products_service

MIN_PHONE_DIGITS = 8


def validate_customer_data(customer_name, customer_phone, customer_department):
    """Valida los datos obligatorios del cliente antes de guardar.

    Regresa una lista de mensajes de error (vacía si todo es válido).
    Se usa desde la ruta pública, antes de persistir la cotización.
    """
    errors = []

    if not customer_name.strip():
        errors.append("El nombre es obligatorio.")

    digits = re.sub(r"\D", "", customer_phone)
    if not customer_phone.strip():
        errors.append("El teléfono es obligatorio.")
    elif len(digits) < MIN_PHONE_DIGITS:
        errors.append(f"El teléfono debe tener al menos {MIN_PHONE_DIGITS} dígitos.")

    if customer_department not in QUOTE_DEPARTMENTS:
        errors.append("Selecciona un departamento válido.")

    return errors


# ----------------------------------------------------------
# Consultas
# ----------------------------------------------------------

def get_quote_or_none(quote_id):
    return db.session.get(Quote, quote_id)


def list_quotes(status=""):
    """Cotizaciones recibidas, de la más reciente a la más antigua."""
    query = Quote.query

    if status in (QUOTE_PENDING, QUOTE_CONVERTED):
        query = query.filter(Quote.status == status)

    return query.order_by(Quote.created_at.desc()).all()


def count_pending_quotes():
    """Cotizaciones pendientes de atender (para el dashboard)."""
    return Quote.query.filter_by(status=QUOTE_PENDING).count()


# ----------------------------------------------------------
# Persistencia desde la sesión pública
# ----------------------------------------------------------

def create_quote_from_session(quote_state):
    """Guarda en base de datos la cotización armada en la sesión.

    Cada renglón de la sesión (código, cantidad, precio visto) se
    enlaza con el producto real por su código; si algún producto ya
    no existe, ese renglón se omite. Regresa la cotización creada,
    o None si ningún renglón pudo enlazarse.
    """
    valid_items = []
    for item in quote_state.get("items", []):
        product = Product.query.filter_by(code=item["code"]).first()
        if product is not None:
            valid_items.append((product, item))

    if not valid_items:
        return None

    quote = Quote(
        code="TMP",
        customer_name=quote_state.get("customer_name", "").strip(),
        customer_phone=quote_state.get("customer_phone", "").strip(),
        customer_department=quote_state.get("customer_department", "").strip(),
        customer_email=quote_state.get("customer_email", "").strip() or None,
    )
    db.session.add(quote)
    db.session.flush()  # asigna el id para generar el código

    quote.code = f"COT-{quote.id:04d}"

    for product, item in valid_items:
        db.session.add(QuoteItem(
            quote=quote,
            product_id=product.id,
            quantity=item["quantity"],
            unit_price=item["price"],  # el precio que el cliente vio
        ))

    db.session.commit()
    return quote


# ----------------------------------------------------------
# Conversión: Cotización → Pedido (Pendiente de pago)
# ----------------------------------------------------------

def convert_to_order(quote, seller):
    """Convierte la cotización en un pedido Pendiente de pago.

    - Reutiliza los productos existentes (no se duplican) y
      mantiene los precios cotizados.
    - Valida la venta mínima por categoría: una cantidad por debajo
      del mínimo se AJUSTA HACIA ARRIBA al mínimo (el cliente
      público puede cotizar menos, pero no se vende menos) y el
      mensaje detalla cada ajuste.
    - Todos los productos deben seguir activos; si alguno no lo
      está, la conversión completa se rechaza.
    - NO descuenta inventario: el pedido nace pendiente y el
      descuento ocurre solo al pagarlo.

    Regresa (pedido, mensaje) o (None, mensaje de error).
    """
    if quote.status != QUOTE_PENDING:
        return None, (
            f"La cotización {quote.code} ya fue convertida "
            f"(pedido {quote.order.code})."
        )

    if not quote.items:
        return None, "La cotización no tiene productos."

    # Validación previa: todos los productos deben estar activos
    for item in quote.items:
        if item.product.status != STATUS_ACTIVE:
            return None, (
                f"El producto {item.product.code} ya no está activo para "
                "venta; no se puede convertir esta cotización."
            )

    # Pedido interno a nombre del vendedor que atiende la cotización
    order = Order(
        seller_id=seller.id,
        code="TMP",
        status=ORDER_PENDING,
        customer_name=quote.customer_name,
        customer_phone=quote.customer_phone,
    )
    db.session.add(order)
    db.session.flush()
    order.code = f"PED-{order.id:04d}"

    adjustments = []
    for item in quote.items:
        minimum = products_service.get_minimum_sale(item.product)
        quantity = item.quantity

        if quantity < minimum:
            adjustments.append(
                f"{item.product.code}: {quantity} → {minimum} (venta mínima)"
            )
            quantity = minimum

        db.session.add(OrderItem(
            order=order,
            product_id=item.product_id,
            quantity=quantity,
            unit_price=item.unit_price,  # se mantiene el precio cotizado
        ))

    # Trazabilidad: la cotización recuerda su pedido
    quote.status = QUOTE_CONVERTED
    quote.order_id = order.id

    db.session.commit()

    message = (
        f"Cotización {quote.code} convertida en el pedido {order.code} "
        "(pendiente de pago; el inventario no cambia hasta pagar)."
    )
    if adjustments:
        message += " Cantidades ajustadas: " + "; ".join(adjustments) + "."

    return order, message
