# ==========================================================
# Modelos de Categoría y Subcategoría.
#
# Las tres categorías del negocio (Cosméticos, Juguetes, Flores)
# son fijas; las subcategorías pueden crecer con el tiempo.
#
# El campo low_stock_threshold vive en la subcategoría porque el
# umbral de "bajo stock" es configurable por subcategoría, no
# global (regla de negocio del ADR). Se usará en el Sprint 4.4.
# ==========================================================
from app.extensions import db


class Category(db.Model):
    __tablename__ = "categories"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)

    # Identificador estable para lógica y estilos (ej. "cosmetics",
    # "toys", "flowers"); el nombre visible puede cambiar, el slug no.
    slug = db.Column(db.String(30), unique=True, nullable=False)

    subcategories = db.relationship(
        "Subcategory", back_populates="category", order_by="Subcategory.name"
    )

    def __repr__(self):
        return f"<Category {self.slug}>"


class Subcategory(db.Model):
    __tablename__ = "subcategories"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey("categories.id"), nullable=False)

    # Umbral de bajo stock configurable por subcategoría (Sprint 4.4)
    low_stock_threshold = db.Column(db.Integer, nullable=False, default=5)

    category = db.relationship("Category", back_populates="subcategories")
    products = db.relationship("Product", back_populates="subcategory")

    # No puede repetirse el nombre de subcategoría dentro de la misma categoría
    __table_args__ = (
        db.UniqueConstraint("category_id", "name", name="uq_subcategory_per_category"),
    )

    def __repr__(self):
        return f"<Subcategory {self.name}>"
