# ==========================================================
# Script de consola para actualizar la base de datos local
# existente con los campos de pago del Sprint 5.3.
#
# db.create_all() solo crea tablas nuevas, no agrega columnas a
# tablas existentes; por eso las bases creadas antes del 5.3
# necesitan este script UNA vez:
#
#     python migrate_payment_fields.py
#
# Es seguro correrlo varias veces: solo agrega lo que falte.
# (Las instalaciones nuevas no lo necesitan: create_all ya crea
# la tabla orders completa.)
# ==========================================================
from sqlalchemy import text

from app import create_app
from app.extensions import db

# Columnas nuevas de la tabla orders (Sprint 5.3)
NEW_COLUMNS = {
    "paid_at": "DATETIME",
    "paid_by_id": "INTEGER REFERENCES users(id)",
}


def get_existing_columns(table_name):
    """Nombres de las columnas actuales de una tabla en SQLite."""
    rows = db.session.execute(text(f"PRAGMA table_info({table_name})"))
    return [row[1] for row in rows]


if __name__ == "__main__":
    app = create_app()

    with app.app_context():
        print("=== Actualizar tabla orders (campos de pago 5.3) ===")

        existing = get_existing_columns("orders")
        added = 0

        for column_name, column_type in NEW_COLUMNS.items():
            if column_name in existing:
                print(f"- {column_name}: ya existe, no se toca.")
            else:
                db.session.execute(text(
                    f"ALTER TABLE orders ADD COLUMN {column_name} {column_type}"
                ))
                print(f"- {column_name}: agregada.")
                added += 1

        db.session.commit()
        print(f"Listo: {added} columna(s) nueva(s).")
