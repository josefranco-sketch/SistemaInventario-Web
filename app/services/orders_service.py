# ==========================================================
# Servicio de pedidos.
#
# Toda la lógica de negocio del armado de pedidos vive aquí:
# - Cada vendedor tiene UN borrador activo a la vez (su "pedido
#   actual"); al confirmarlo pasa a Pendiente de pago y el
#   siguiente producto agregado abre un borrador nuevo.
# - Los renglones apuntan a productos existentes y no se
#   duplican: agregar un producto repetido incrementa su renglón.
# - La venta mínima por categoría (ADR) se valida SIEMPRE:
#   la cantidad de un renglón nunca puede quedar debajo de su
#   mínimo (para menos, se quita el producto completo).
# - Subtotales y total se calculan automáticamente (modelo).
#
# REGLA ADR CRÍTICA: nada en este servicio toca el inventario.
# Un borrador o un pedido pendiente de pago JAMÁS descuentan
# stock; el descuento ocurre una sola vez al pagar (Sprint 5.3).
# ==========================================================
from app.extensions import db
from app.models.order import ORDER_DRAFT, ORDER_PENDING, Order, OrderItem
from app.models.product import STATUS_ACTIVE
from app.services import products_service


# ----------------------------------------------------------
# Consultas
# ----------------------------------------------------------

def get_order_or_none(order_id):
    return db.session.get(Order, order_id)


def get_item_or_none(item_id):
    return db.session.get(OrderItem, item_id)


def get_current_draft(seller):
    """El borrador activo del vendedor, o None si no tiene."""
    return Order.query.filter_by(seller_id=seller.id, status=ORDER_DRAFT).first()


def get_or_create_draft(seller):
    """Regresa el borrador del vendedor; si no existe lo crea."""
    order = get_current_draft(seller)
    if order is not None:
        return order

    order = Order(seller_id=seller.id, code="TMP")
    db.session.add(order)
    db.session.flush()  # asigna el id para generar el código

    order.code = f"PED-{order.id:04d}"
    db.session.commit()
    return order


def list_orders_by_seller(seller):
    """Pedidos del vendedor, del más reciente al más antiguo."""
    return (
        Order.query.filter_by(seller_id=seller.id)
        .order_by(Order.created_at.desc())
        .all()
    )


def _find_item(order, product_id):
    """Busca el renglón de un producto dentro del pedido."""
    for item in order.items:
        if item.product_id == product_id:
            return item
    return None


# ----------------------------------------------------------
# Armado del pedido (solo borradores)
# ----------------------------------------------------------

def add_product(order, product, quantity=None):
    """Agrega un producto al borrador (o incrementa su renglón).

    Si no se indica cantidad, se usa la venta mínima de su
    categoría. Regresa (True/False, mensaje).
    """
    if not order.is_editable:
        return False, "Este pedido ya no se puede modificar."

    if product.status != STATUS_ACTIVE:
        return False, f"El producto {product.code} no está activo para venta."

    minimum = products_service.get_minimum_sale(product)

    if quantity is None:
        quantity = minimum

    if quantity < 1:
        return False, "La cantidad debe ser mayor a cero."

    item = _find_item(order, product.id)

    if item is not None:
        # No se duplica el producto: se incrementa su renglón
        item.quantity += quantity
        db.session.commit()
        return True, f"{product.code}: cantidad actualizada a {item.quantity}."

    if quantity < minimum:
        return False, (
            f"La venta mínima de {product.code} es {minimum} "
            f"({product.category.name})."
        )

    item = OrderItem(
        order=order,
        product_id=product.id,
        quantity=quantity,
        unit_price=product.price,  # precio congelado al agregar
    )
    db.session.add(item)
    db.session.commit()
    return True, f"{product.code} agregado al pedido ({quantity})."


def change_quantity(order, item, delta):
    """Incrementa o disminuye la cantidad de un renglón.

    La cantidad nunca puede quedar debajo de la venta mínima de la
    categoría: para menos que eso, se quita el producto completo.
    Regresa (True/False, mensaje).
    """
    if not order.is_editable:
        return False, "Este pedido ya no se puede modificar."

    minimum = products_service.get_minimum_sale(item.product)
    new_quantity = item.quantity + delta

    if new_quantity < minimum:
        return False, (
            f"La venta mínima de {item.product.code} es {minimum}. "
            "Si ya no lo quieres, usa «Quitar»."
        )

    item.quantity = new_quantity
    db.session.commit()
    return True, f"{item.product.code}: cantidad actualizada a {new_quantity}."


def remove_product(order, item):
    """Quita un renglón completo del borrador."""
    if not order.is_editable:
        return False, "Este pedido ya no se puede modificar."

    code = item.product.code
    db.session.delete(item)
    db.session.commit()
    return True, f"{code} quitado del pedido."


# ----------------------------------------------------------
# Confirmación: Borrador → Pendiente de pago
# ----------------------------------------------------------

def confirm_order(order, customer_name, customer_phone=""):
    """Confirma el borrador y lo deja Pendiente de pago.

    Valida que tenga productos, que todos sigan activos, que las
    cantidades respeten los mínimos y que haya nombre de cliente.

    IMPORTANTE: aquí NO se descuenta inventario (regla ADR); el
    descuento ocurre al marcar el pedido como Pagado (Sprint 5.3).
    Regresa (True/False, mensaje).
    """
    if not order.is_editable:
        return False, "Este pedido ya fue confirmado."

    if not order.items:
        return False, "El pedido no tiene productos."

    customer_name = customer_name.strip() if customer_name else ""
    if customer_name == "":
        return False, "El nombre del cliente es obligatorio para confirmar."

    # Revalidamos cada renglón: el catálogo pudo cambiar mientras
    # el borrador estaba abierto.
    for item in order.items:
        if item.product.status != STATUS_ACTIVE:
            return False, (
                f"El producto {item.product.code} ya no está activo; "
                "quítalo del pedido para continuar."
            )

        minimum = products_service.get_minimum_sale(item.product)
        if item.quantity < minimum:
            return False, (
                f"{item.product.code} no cumple la venta mínima de {minimum}."
            )

    order.customer_name = customer_name
    order.customer_phone = customer_phone.strip() or None if customer_phone else None
    order.status = ORDER_PENDING

    db.session.commit()
    return True, (
        f"Pedido {order.code} confirmado: pendiente de pago. "
        "El inventario no cambia hasta registrar el pago."
    )
