# ==========================================================
# Modelos de Inventario.
#
# Inventory: existencia interna en tienda de cada producto.
#   - Relación 1 a 1 con el producto existente (nunca se
#     duplican productos, regla ADR).
#   - El stock exacto SOLO lo ven admin/vendedor; el cliente
#     público únicamente ve la disponibilidad (badges).
#
# InventoryMovement: historial de movimientos.
#   - Cada ajuste manual deja historial con usuario, fecha y
#     motivo — obligatorio, sin excepción (regla ADR).
#   - El inventario NUNCA baja por cotizaciones ni por pedidos
#     pendientes; el descuento por venta pagada llega en Fase 5.
# ==========================================================
from datetime import datetime

from app.extensions import db

# Tipos de movimiento.
# "venta" solo lo genera el sistema al pagar un pedido (Sprint 5.3);
# nunca se registra a mano desde el formulario de inventario.
MOVEMENT_ENTRY = "entrada"
MOVEMENT_EXIT = "salida"
MOVEMENT_SALE = "venta"
MOVEMENT_TYPES = [MOVEMENT_ENTRY, MOVEMENT_EXIT, MOVEMENT_SALE]

MOVEMENT_LABELS = {
    MOVEMENT_ENTRY: "Entrada",
    MOVEMENT_EXIT: "Salida",
    MOVEMENT_SALE: "Venta",
}

# Tipos que el administrador puede registrar manualmente
MANUAL_MOVEMENT_TYPES = [MOVEMENT_ENTRY, MOVEMENT_EXIT]


class Inventory(db.Model):
    __tablename__ = "inventories"

    id = db.Column(db.Integer, primary_key=True)

    # unique=True garantiza un solo registro de inventario por producto
    product_id = db.Column(
        db.Integer, db.ForeignKey("products.id"), unique=True, nullable=False
    )
    product = db.relationship(
        "Product", backref=db.backref("inventory", uselist=False)
    )

    quantity = db.Column(db.Integer, nullable=False, default=0)

    updated_at = db.Column(
        db.DateTime, nullable=False, default=datetime.now, onupdate=datetime.now
    )

    def __repr__(self):
        return f"<Inventory {self.product_id}: {self.quantity}>"


class InventoryMovement(db.Model):
    __tablename__ = "inventory_movements"

    id = db.Column(db.Integer, primary_key=True)

    product_id = db.Column(db.Integer, db.ForeignKey("products.id"), nullable=False)
    product = db.relationship("Product")

    # Usuario que realizó el movimiento (obligatorio para trazabilidad)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    user = db.relationship("User")

    movement_type = db.Column(db.String(20), nullable=False)

    # Cantidad del movimiento (siempre positiva; el tipo define el signo)
    quantity = db.Column(db.Integer, nullable=False)

    # Stock antes y después, para poder auditar cada movimiento
    quantity_before = db.Column(db.Integer, nullable=False)
    quantity_after = db.Column(db.Integer, nullable=False)

    # Motivo obligatorio (regla ADR: usuario, fecha y motivo siempre)
    reason = db.Column(db.String(200), nullable=False)

    created_at = db.Column(db.DateTime, nullable=False, default=datetime.now)

    @property
    def movement_label(self):
        return MOVEMENT_LABELS.get(self.movement_type, self.movement_type)

    def __repr__(self):
        return f"<Movement {self.movement_type} {self.quantity} p{self.product_id}>"
