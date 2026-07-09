# ==========================================================
# Servicio de inventario.
#
# Toda la lógica de existencias vive aquí:
# - Registrar entradas y salidas (con usuario, fecha y motivo
#   obligatorios — regla ADR, sin excepción).
# - Validar que una salida nunca deje stock negativo.
# - Recalcular la disponibilidad pública del producto según su
#   stock y el umbral de bajo stock de su subcategoría.
# - Consultar existencias e historial de movimientos.
#
# IMPORTANTE (ADR): el inventario NUNCA baja por cotizaciones ni
# por pedidos pendientes de pago. El descuento automático por
# venta pagada se implementa en la Fase 5 (usará también este
# servicio para dejar historial).
# ==========================================================
from app.extensions import db
from app.models.category import Subcategory
from app.models.inventory import (
    MOVEMENT_ENTRY,
    MOVEMENT_EXIT,
    MOVEMENT_LABELS,
    MOVEMENT_TYPES,
    Inventory,
    InventoryMovement,
)
from app.models.product import (
    AVAILABILITY_AVAILABLE,
    AVAILABILITY_LOW,
    AVAILABILITY_OUT,
    STATUS_ACTIVE,
    Product,
)


# ----------------------------------------------------------
# Consultas
# ----------------------------------------------------------

def get_stock(product):
    """Stock actual del producto (0 si aún no tiene inventario)."""
    if product.inventory is None:
        return 0
    return product.inventory.quantity


def get_threshold(product):
    """Umbral de bajo stock del producto (viene de su subcategoría)."""
    return product.subcategory.low_stock_threshold


def is_low_stock(product):
    """Bajo stock = hay existencia pero no supera el umbral.

    El stock en cero no cuenta como bajo stock: eso es "agotado",
    que es un estado distinto.
    """
    stock = get_stock(product)
    return 0 < stock <= get_threshold(product)


def get_inventory_overview(search="", category_id=None, only_low=False):
    """Productos con su stock para la vista de inventario admin."""
    query = Product.query

    if search:
        like = f"%{search}%"
        query = query.filter(
            db.or_(Product.code.ilike(like), Product.name.ilike(like))
        )

    if category_id:
        query = query.join(Subcategory).filter(
            Subcategory.category_id == category_id
        )

    products = query.order_by(Product.code).all()

    if only_low:
        products = [p for p in products if is_low_stock(p)]

    return products


def list_movements(product_id=None, limit=100):
    """Historial de movimientos, del más reciente al más antiguo."""
    query = InventoryMovement.query

    if product_id:
        query = query.filter(InventoryMovement.product_id == product_id)

    return query.order_by(InventoryMovement.created_at.desc()).limit(limit).all()


def count_low_stock():
    """Cantidad de productos activos en bajo stock (para el dashboard)."""
    count = 0
    for product in Product.query.filter_by(status=STATUS_ACTIVE).all():
        if is_low_stock(product):
            count += 1
    return count


# ----------------------------------------------------------
# Disponibilidad pública según inventario
# ----------------------------------------------------------

def compute_availability(quantity, threshold):
    """Traduce el stock exacto al nivel público (el cliente solo ve esto).

    - 0                → agotado
    - 1 hasta umbral   → baja disponibilidad
    - mayor al umbral  → disponible
    """
    if quantity <= 0:
        return AVAILABILITY_OUT
    if quantity <= threshold:
        return AVAILABILITY_LOW
    return AVAILABILITY_AVAILABLE


def refresh_availability(product):
    """Recalcula y guarda la disponibilidad pública del producto."""
    product.availability = compute_availability(
        get_stock(product), get_threshold(product)
    )


# ----------------------------------------------------------
# Registro de movimientos
# ----------------------------------------------------------

def register_movement(product, user, movement_type, quantity, reason, commit=True):
    """Registra un movimiento de inventario (entrada, salida o venta).

    Valida el movimiento, actualiza la existencia, deja el
    historial (usuario, fecha, motivo, stock antes/después) y
    recalcula la disponibilidad pública.

    Con commit=False deja los cambios pendientes en la sesión para
    que quien llama confirme todo junto (lo usa el pago de pedidos,
    que descuenta varios productos en una sola transacción).

    Regresa (True, mensaje) o (False, mensaje de error).
    """
    if movement_type not in MOVEMENT_TYPES:
        return False, "Tipo de movimiento no válido."

    if quantity is None or quantity < 1:
        return False, "La cantidad debe ser un número mayor a cero."

    reason = reason.strip() if reason else ""
    if reason == "":
        return False, "El motivo del movimiento es obligatorio."

    # Todas las validaciones ocurren ANTES de tocar la base de datos,
    # para que un movimiento rechazado no deje nada a medias.
    before = get_stock(product)

    if movement_type == MOVEMENT_ENTRY:
        after = before + quantity
    else:  # salida o venta: ambas descuentan
        if quantity > before:
            return False, (
                f"Stock insuficiente: hay {before} y se piden {quantity}."
            )
        after = before - quantity

    # El inventario pertenece al producto existente: si aún no tiene
    # registro, se crea aquí (nunca se duplica el producto). Se asigna
    # por la relación para que product.inventory quede actualizado.
    inventory = product.inventory
    if inventory is None:
        inventory = Inventory(product=product, quantity=0)
        db.session.add(inventory)

    inventory.quantity = after

    movement = InventoryMovement(
        product_id=product.id,
        user_id=user.id,
        movement_type=movement_type,
        quantity=quantity,
        quantity_before=before,
        quantity_after=after,
        reason=reason,
    )
    db.session.add(movement)

    # La disponibilidad pública se deriva del stock: el cliente ve el
    # badge, nunca el número exacto.
    refresh_availability(product)

    if commit:
        db.session.commit()

    label = MOVEMENT_LABELS.get(movement_type, movement_type)
    return True, (
        f"{label} de {quantity} registrada para {product.code}. "
        f"Stock: {before} → {after}."
    )


# ----------------------------------------------------------
# Umbral de bajo stock por subcategoría (regla ADR: configurable)
# ----------------------------------------------------------

def get_subcategories_grouped():
    """Subcategorías agrupadas por categoría para la pantalla de umbrales."""
    from app.models.category import Category

    return Category.query.order_by(Category.name).all()


def update_thresholds(form_data):
    """Guarda los umbrales editados en la pantalla de configuración.

    form_data trae pares "threshold-<id de subcategoría>" → valor.
    Regresa (cuántos cambiaron, lista de errores).
    """
    changed = 0
    errors = []
    changed_subcategories = []

    for subcategory in Subcategory.query.all():
        field_name = f"threshold-{subcategory.id}"
        raw_value = form_data.get(field_name)

        if raw_value is None:
            continue

        try:
            value = int(raw_value)
        except ValueError:
            errors.append(f"Valor no numérico para {subcategory.name}.")
            continue

        if value < 0:
            errors.append(f"El umbral de {subcategory.name} no puede ser negativo.")
            continue

        if value != subcategory.low_stock_threshold:
            subcategory.low_stock_threshold = value
            changed += 1
            changed_subcategories.append(subcategory.id)

    if changed_subcategories:
        # Un umbral nuevo puede cambiar la disponibilidad pública de
        # los productos de esas subcategorías
        affected = Product.query.filter(
            Product.subcategory_id.in_(changed_subcategories)
        ).all()
        for product in affected:
            refresh_availability(product)

    db.session.commit()
    return changed, errors
