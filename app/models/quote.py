# ==========================================================
# Modelos de Cotización.
#
# Quote: solicitud de cotización que el cliente público envía
# desde el catálogo. Se persiste para que los vendedores la
# consulten y puedan convertirla en pedido (Sprint 6.2).
#
# Reglas ADR:
# - Una cotización NO maneja pagos y JAMÁS descuenta inventario.
# - Sus renglones apuntan a productos existentes (fuente única)
#   y congelan el precio que el cliente vio al cotizar.
# - Trazabilidad: al convertirse guarda el pedido resultante.
# ==========================================================
from datetime import datetime
from decimal import Decimal

from app.extensions import db

# Estados de la cotización
QUOTE_PENDING = "pendiente"
QUOTE_CONVERTED = "convertida"

QUOTE_STATUS_LABELS = {
    QUOTE_PENDING: "Pendiente",
    QUOTE_CONVERTED: "Convertida en pedido",
}

# Departamentos de Guatemala, para el select obligatorio del
# formulario público de cotización (evita departamentos inventados).
QUOTE_DEPARTMENTS = [
    "Alta Verapaz",
    "Baja Verapaz",
    "Chimaltenango",
    "Chiquimula",
    "El Progreso",
    "Escuintla",
    "Guatemala",
    "Huehuetenango",
    "Izabal",
    "Jalapa",
    "Jutiapa",
    "Petén",
    "Quetzaltenango",
    "Quiché",
    "Retalhuleu",
    "Sacatepéquez",
    "San Marcos",
    "Santa Rosa",
    "Sololá",
    "Suchitepéquez",
    "Totonicapán",
    "Zacapa",
]


class Quote(db.Model):
    __tablename__ = "quotes"

    id = db.Column(db.Integer, primary_key=True)

    # Código legible de la cotización (ej. COT-0001), único
    code = db.Column(db.String(20), unique=True, nullable=False)

    # Datos que el cliente dejó al solicitar la cotización
    customer_name = db.Column(db.String(120), nullable=False)
    customer_phone = db.Column(db.String(30), nullable=False)
    customer_department = db.Column(db.String(50), nullable=False, default="")
    customer_email = db.Column(db.String(120), nullable=True)

    status = db.Column(db.String(20), nullable=False, default=QUOTE_PENDING)

    # Trazabilidad: pedido creado a partir de esta cotización
    order_id = db.Column(db.Integer, db.ForeignKey("orders.id"), nullable=True)
    order = db.relationship("Order")

    created_at = db.Column(db.DateTime, nullable=False, default=datetime.now)

    items = db.relationship(
        "QuoteItem",
        back_populates="quote",
        order_by="QuoteItem.id",
        cascade="all, delete-orphan",
    )

    @property
    def total(self):
        """Total cotizado, calculado siempre desde los renglones."""
        total = Decimal("0.00")
        for item in self.items:
            total += item.subtotal
        return total

    @property
    def status_label(self):
        return QUOTE_STATUS_LABELS.get(self.status, self.status)

    def __repr__(self):
        return f"<Quote {self.code} ({self.status})>"


class QuoteItem(db.Model):
    __tablename__ = "quote_items"

    id = db.Column(db.Integer, primary_key=True)

    quote_id = db.Column(db.Integer, db.ForeignKey("quotes.id"), nullable=False)
    quote = db.relationship("Quote", back_populates="items")

    product_id = db.Column(db.Integer, db.ForeignKey("products.id"), nullable=False)
    product = db.relationship("Product")

    quantity = db.Column(db.Integer, nullable=False)

    # Precio que el cliente vio al cotizar (congelado)
    unit_price = db.Column(db.Numeric(10, 2), nullable=False)

    @property
    def subtotal(self):
        return self.unit_price * self.quantity

    def __repr__(self):
        return f"<QuoteItem {self.product_id} x{self.quantity}>"
