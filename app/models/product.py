# ==========================================================
# Modelo de Producto — fuente única de verdad del sistema.
#
# Un solo registro de producto alimenta catálogo público,
# inventario, cotizaciones y ventas (regla ADR: nunca duplicar).
#
# Reglas importantes:
# - El código del producto es ÚNICO.
# - Los productos NUNCA se eliminan físicamente; solo cambian de
#   estado: activo / inactivo / archivado.
# - La disponibilidad pública (disponible / baja / agotado) es lo
#   único que ve el cliente; el stock exacto jamás se muestra.
# ==========================================================
from datetime import datetime

from app.extensions import db

# Estados del producto (regla ADR: no hay eliminación física)
STATUS_ACTIVE = "activo"
STATUS_INACTIVE = "inactivo"
STATUS_ARCHIVED = "archivado"
PRODUCT_STATUSES = [STATUS_ACTIVE, STATUS_INACTIVE, STATUS_ARCHIVED]

STATUS_LABELS = {
    STATUS_ACTIVE: "Activo",
    STATUS_INACTIVE: "Inactivo",
    STATUS_ARCHIVED: "Archivado",
}

# Niveles de disponibilidad pública (el cliente nunca ve stock exacto)
AVAILABILITY_AVAILABLE = "disponible"
AVAILABILITY_LOW = "baja"
AVAILABILITY_OUT = "agotado"
AVAILABILITY_LEVELS = [AVAILABILITY_AVAILABLE, AVAILABILITY_LOW, AVAILABILITY_OUT]

AVAILABILITY_LABELS = {
    AVAILABILITY_AVAILABLE: "Disponible",
    AVAILABILITY_LOW: "Baja disponibilidad",
    AVAILABILITY_OUT: "Agotado",
}

# Presentaciones comerciales con las que se vende
COMMERCIAL_UNITS = ["Caja", "Display", "Unidad", "Ramo"]

# Plurales en español para mostrar cantidades ("3 unidades", "2 cajas")
UNIT_PLURALS = {
    "Caja": "cajas",
    "Display": "displays",
    "Unidad": "unidades",
    "Ramo": "ramos",
}


class Product(db.Model):
    __tablename__ = "products"

    id = db.Column(db.Integer, primary_key=True)

    # Código único del producto (ej. MES3107)
    code = db.Column(db.String(30), unique=True, nullable=False, index=True)

    name = db.Column(db.String(120), nullable=False)
    description = db.Column(db.Text, nullable=True)
    brand = db.Column(db.String(80), nullable=True)

    subcategory_id = db.Column(
        db.Integer, db.ForeignKey("subcategories.id"), nullable=False
    )
    subcategory = db.relationship("Subcategory", back_populates="products")

    # Precio en quetzales, sin impuestos (el sistema no maneja impuestos)
    price = db.Column(db.Numeric(10, 2), nullable=False)

    # Cómo se vende: "Caja x 24 labiales", "Ramo de 12 unidades", etc.
    commercial_presentation = db.Column(db.String(120), nullable=False)
    commercial_unit = db.Column(db.String(20), nullable=False)

    status = db.Column(db.String(20), nullable=False, default=STATUS_ACTIVE)
    availability = db.Column(
        db.String(20), nullable=False, default=AVAILABILITY_AVAILABLE
    )

    # Nombre del archivo de imagen dentro de static/img/products/
    image_filename = db.Column(db.String(120), nullable=True)

    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(
        db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow
    )

    # ----- Ayudas de presentación (etiquetas legibles) -----

    @property
    def category(self):
        """Acceso directo a la categoría a través de la subcategoría."""
        return self.subcategory.category

    @property
    def status_label(self):
        return STATUS_LABELS.get(self.status, self.status)

    @property
    def availability_label(self):
        return AVAILABILITY_LABELS.get(self.availability, self.availability)

    def __repr__(self):
        return f"<Product {self.code} ({self.status})>"
