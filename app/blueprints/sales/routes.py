# ==========================================================
# Rutas del módulo de ventas.
#
# Sprint 5.1: panel del vendedor con buscador de productos.
# Acceso: vendedores y administradores (el cliente público no
# entra). Las rutas solo manejan HTTP; la lógica vive en
# app/services/sales_service.py.
# ==========================================================
from flask import render_template, request
from flask_login import login_required

from app.blueprints.auth.decorators import seller_required
from app.blueprints.sales import sales_bp
from app.services import products_service, sales_service


@sales_bp.route("/")
@login_required
@seller_required
def panel():
    # Filtros del buscador (?q=...&category=...)
    search = request.args.get("q", "").strip()
    category_id = request.args.get("category", type=int)

    # Solo buscamos cuando el vendedor pidió algo, para que el
    # panel inicial invite a buscar en lugar de volcar todo.
    searched = bool(search) or category_id is not None

    results = []
    if searched:
        results = sales_service.search_products_for_sale(
            search=search, category_id=category_id
        )

    return render_template(
        "sales/panel.html",
        results=results,
        searched=searched,
        search=search,
        selected_category=category_id,
        categories=products_service.get_all_categories(),
    )
