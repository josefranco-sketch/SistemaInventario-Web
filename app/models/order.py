# ==========================================================
# Modelos de Pedido (venta interna).
#
# Order: pedido que arma el vendedor para un cliente.
#   - Estados: borrador → pendiente (de pago) → pagado / cancelado.
#   - REGLA ADR: un pedido en borrador o pendiente NUNCA descuenta
#     inventario; el descuento ocurre una sola vez al pasar a
#     Pagado (Sprint 5.3).
#
# OrderItem: renglón del pedido.
#   - Apunta SIEMPRE a un producto existente (fuente única, nunca
#     se duplica el producto).
#   - Congela el precio unitario al momento de agregarse, para que
#     un cambio de precio posterior no altere pedidos ya armados.
#   - Subtotales y total se calculan automáticamente.
# ==========================================================
from datetime import datetime
from decimal import Decimal

from app.extensions import db

# Estados del pedido
ORDER_DRAFT = "borrador"
ORDER_PENDING = "pendiente"
ORDER_PAID = "pagado"
ORDER_CANCELLED = "cancelado"
ORDER_STATUSES = [ORDER_DRAFT, ORDER_PENDING, ORDER_PAID, ORDER_CANCELLED]

ORDER_STATUS_LABELS = {
    ORDER_DRAFT: "Borrador",
    ORDER_PENDING: "Pendiente de pago",
    ORDER_PAID: "Pagado",
    ORDER_CANCELLED: "Cancelado",
}


class Order(db.Model):
    __tablename__ = "orders"

    id = db.Column(db.Integer, primary_key=True)

    # Código legible del pedido (ej. PED-0001), único
    code = db.Column(db.String(20), unique=True, nullable=False)

    # Vendedor que arma el pedido (trazabilidad).
    # foreign_keys es necesario porque el pedido tiene dos relaciones
    # hacia users (quien vende y quien cobra).
    seller_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    seller = db.relationship("User", foreign_keys=[seller_id])

    # Datos básicos del cliente (sin cuentas de cliente: venta en tienda)
    customer_name = db.Column(db.String(120), nullable=True)
    customer_phone = db.Column(db.String(30), nullable=True)

    status = db.Column(db.String(20), nullable=False, default=ORDER_DRAFT)

    # Trazabilidad del pago (Sprint 5.3): cuándo se pagó y quién lo cobró
    paid_at = db.Column(db.DateTime, nullable=True)
    paid_by_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=True)
    paid_by = db.relationship("User", foreign_keys=[paid_by_id])

    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(
        db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow
    )

    items = db.relationship(
        "OrderItem",
        back_populates="order",
        order_by="OrderItem.id",
        cascade="all, delete-orphan",
    )

    # Un mismo producto no puede repetirse en el pedido: si se vuelve a
    # agregar, se incrementa la cantidad del renglón existente.

    @property
    def total(self):
        """Total del pedido, calculado siempre desde los renglones."""
        total = Decimal("0.00")
        for item in self.items:
            total += item.subtotal
        return total

    @property
    def total_units(self):
        """Cantidad total de unidades del pedido."""
        units = 0
        for item in self.items:
            units += item.quantity
        return units

    @property
    def status_label(self):
        return ORDER_STATUS_LABELS.get(self.status, self.status)

    @property
    def is_editable(self):
        """Solo un borrador puede modificarse."""
        return self.status == ORDER_DRAFT

    def __repr__(self):
        return f"<Order {self.code} ({self.status})>"


class OrderItem(db.Model):
    __tablename__ = "order_items"

    id = db.Column(db.Integer, primary_key=True)

    order_id = db.Column(db.Integer, db.ForeignKey("orders.id"), nullable=False)
    order = db.relationship("Order", back_populates="items")

    product_id = db.Column(db.Integer, db.ForeignKey("products.id"), nullable=False)
    product = db.relationship("Product")

    quantity = db.Column(db.Integer, nullable=False)

    # Precio congelado al momento de agregar el producto al pedido
    unit_price = db.Column(db.Numeric(10, 2), nullable=False)

    # Un producto solo puede aparecer una vez por pedido
    __table_args__ = (
        db.UniqueConstraint("order_id", "product_id", name="uq_product_per_order"),
    )

    @property
    def subtotal(self):
        """Subtotal del renglón, calculado automáticamente."""
        return self.unit_price * self.quantity

    def __repr__(self):
        return f"<OrderItem {self.product_id} x{self.quantity}>"
