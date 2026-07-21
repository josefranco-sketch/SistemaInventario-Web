# ==========================================================
# Script de consola para actualizar la base de datos local
# existente con el campo de departamento del fix de cotizaciones
# públicas persistentes.
#
# db.create_all() solo crea tablas nuevas, no agrega columnas a
# tablas existentes; por eso las bases creadas antes de este fix
# necesitan este script UNA vez:
#
#     python migrate_quote_department.py
#
# Es seguro correrlo varias veces: solo agrega lo que falte. Las
# cotizaciones ya guardadas quedan con departamento vacío ("") —
# no se puede reconstruir un dato que nunca se pidió al cliente.
# (Las instalaciones nuevas no lo necesitan: create_all ya crea
# la tabla quotes completa.)
# ==========================================================
from sqlalchemy import text

from app import create_app
from app.extensions import db

# Columna nueva de la tabla quotes (fix de cotizaciones persistentes)
NEW_COLUMNS = {
    "customer_department": "VARCHAR(50) NOT NULL DEFAULT ''",
}


def get_existing_columns(table_name):
    """Nombres de las columnas actuales de una tabla en SQLite."""
    rows = db.session.execute(text(f"PRAGMA table_info({table_name})"))
    return [row[1] for row in rows]


if __name__ == "__main__":
    app = create_app()

    with app.app_context():
        print("=== Actualizar tabla quotes (departamento del cliente) ===")

        existing = get_existing_columns("quotes")
        added = 0

        for column_name, column_type in NEW_COLUMNS.items():
            if column_name in existing:
                print(f"- {column_name}: ya existe, no se toca.")
            else:
                db.session.execute(text(
                    f"ALTER TABLE quotes ADD COLUMN {column_name} {column_type}"
                ))
                print(f"- {column_name}: agregada.")
                added += 1

        db.session.commit()
        print(f"Listo: {added} columna(s) nueva(s).")
