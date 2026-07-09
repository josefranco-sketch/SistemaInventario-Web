# ==========================================================
# Rutas del módulo de ventas.
#
# Sprint 5.1: panel del vendedor con buscador de productos.
# Sprint 5.2: creación de pedidos (borrador → pendiente de pago).
#
# Acceso: vendedores y administradores (el cliente público no
# entra). Las rutas solo manejan HTTP; la lógica vive en
# app/services/ (sales_service y orders_service).
# ==========================================================
from flask import flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required

from app.blueprints.auth.decorators import seller_required
from app.blueprints.sales import sales_bp
from app.blueprints.sales.forms import ConfirmOrderForm, CsrfOnlyForm
from app.services import orders_service, products_service, sales_service


def _safe_next_url(next_url):
    """Solo acepta rutas internas del sitio para redirecciones."""
    if next_url and next_url.startswith("/") and not next_url.startswith("//"):
        return next_url
    return None


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
        csrf_form=CsrfOnlyForm(),
    )


# ----------------------------------------------------------
# Pedido actual (borrador del vendedor)
# ----------------------------------------------------------

@sales_bp.route("/order")
@login_required
@seller_required
def current_order():
    order = orders_service.get_current_draft(current_user)

    return render_template(
        "sales/order.html",
        order=order,
        csrf_form=CsrfOnlyForm(),
        confirm_form=ConfirmOrderForm(),
        get_minimum=products_service.get_minimum_sale,
    )


@sales_bp.route("/order/add/<int:product_id>", methods=["POST"])
@login_required
@seller_required
def order_add(product_id):
    form = CsrfOnlyForm()
    if not form.validate_on_submit():
        flash("No se pudo agregar el producto.", "danger")
        return redirect(url_for("sales.panel"))

    product = products_service.get_product_or_none(product_id)
    if product is None:
        flash("El producto no existe.", "danger")
        return redirect(url_for("sales.panel"))

    order = orders_service.get_or_create_draft(current_user)
    quantity = request.form.get("quantity", type=int)

    ok, message = orders_service.add_product(order, product, quantity)
    flash(message, "success" if ok else "warning")

    # Regresamos a donde estaba el vendedor (ej. su búsqueda actual)
    next_url = _safe_next_url(request.form.get("next"))
    return redirect(next_url or url_for("sales.panel"))


def _get_own_editable_item(item_id):
    """Renglón del borrador del propio vendedor, o None.

    Evita que alguien manipule renglones de pedidos ajenos o ya
    confirmados enviando ids a mano.
    """
    item = orders_service.get_item_or_none(item_id)
    if item is None:
        return None
    if item.order.seller_id != current_user.id:
        return None
    if not item.order.is_editable:
        return None
    return item


@sales_bp.route("/order/item/<int:item_id>/change", methods=["POST"])
@login_required
@seller_required
def order_item_change(item_id):
    form = CsrfOnlyForm()
    item = _get_own_editable_item(item_id)

    if not form.validate_on_submit() or item is None:
        flash("No se pudo actualizar el renglón.", "danger")
        return redirect(url_for("sales.current_order"))

    delta = request.form.get("delta", type=int)
    if delta not in (1, -1):
        flash("Cambio de cantidad no válido.", "danger")
        return redirect(url_for("sales.current_order"))

    ok, message = orders_service.change_quantity(item.order, item, delta)
    flash(message, "success" if ok else "warning")
    return redirect(url_for("sales.current_order"))


@sales_bp.route("/order/item/<int:item_id>/remove", methods=["POST"])
@login_required
@seller_required
def order_item_remove(item_id):
    form = CsrfOnlyForm()
    item = _get_own_editable_item(item_id)

    if not form.validate_on_submit() or item is None:
        flash("No se pudo quitar el producto.", "danger")
        return redirect(url_for("sales.current_order"))

    ok, message = orders_service.remove_product(item.order, item)
    flash(message, "success" if ok else "warning")
    return redirect(url_for("sales.current_order"))


@sales_bp.route("/order/confirm", methods=["POST"])
@login_required
@seller_required
def order_confirm():
    order = orders_service.get_current_draft(current_user)
    if order is None:
        flash("No tienes un pedido en preparación.", "warning")
        return redirect(url_for("sales.panel"))

    form = ConfirmOrderForm()

    if not form.validate_on_submit():
        # Reconstruimos la vista del pedido mostrando los errores
        return render_template(
            "sales/order.html",
            order=order,
            csrf_form=CsrfOnlyForm(),
            confirm_form=form,
            get_minimum=products_service.get_minimum_sale,
        )

    ok, message = orders_service.confirm_order(
        order,
        customer_name=form.customer_name.data,
        customer_phone=form.customer_phone.data,
    )
    flash(message, "success" if ok else "warning")

    if ok:
        return redirect(url_for("sales.order_detail", order_id=order.id))
    return redirect(url_for("sales.current_order"))


# ----------------------------------------------------------
# Pedidos del vendedor
# ----------------------------------------------------------

@sales_bp.route("/orders")
@login_required
@seller_required
def orders_list():
    orders = orders_service.list_orders_by_seller(current_user)
    return render_template("sales/orders_list.html", orders=orders)


@sales_bp.route("/orders/<int:order_id>")
@login_required
@seller_required
def order_detail(order_id):
    order = orders_service.get_order_or_none(order_id)

    # Cada vendedor ve sus pedidos; el administrador puede ver todos
    if order is None or (
        order.seller_id != current_user.id and not current_user.is_admin()
    ):
        flash("El pedido no existe.", "danger")
        return redirect(url_for("sales.orders_list"))

    # Un borrador propio se edita en la vista de pedido actual
    if order.is_editable and order.seller_id == current_user.id:
        return redirect(url_for("sales.current_order"))

    return render_template("sales/order_detail.html", order=order)
