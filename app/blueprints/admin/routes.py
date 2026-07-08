# ==========================================================
# Rutas del panel administrativo.
#
# Las rutas solo manejan HTTP: leen filtros, piden los datos a
# los servicios y renderizan templates. Los cálculos y reglas
# de negocio viven en app/services/.
# ==========================================================
from flask import flash, redirect, render_template, request, url_for
from flask_login import login_required

from app.blueprints.admin import admin_bp
from app.blueprints.admin.forms import ProductForm, StatusChangeForm
from app.blueprints.auth.decorators import admin_required
from app.services import products_service
from app.services.dashboard_service import get_dashboard_summary


@admin_bp.route("/")
@login_required
@admin_required
def dashboard():
    summary = get_dashboard_summary()
    return render_template("admin/dashboard.html", summary=summary)


# ----------------------------------------------------------
# Productos
# ----------------------------------------------------------

@admin_bp.route("/products")
@login_required
@admin_required
def products_list():
    # Filtros que llegan por la URL (?q=...&category=...&status=...)
    search = request.args.get("q", "").strip()
    category_id = request.args.get("category", type=int)
    status = request.args.get("status", "").strip()

    products = products_service.list_products(
        search=search, category_id=category_id, status=status
    )

    return render_template(
        "admin/products/list.html",
        products=products,
        categories=products_service.get_all_categories(),
        search=search,
        selected_category=category_id,
        selected_status=status,
        status_form=StatusChangeForm(),
    )


@admin_bp.route("/products/new", methods=["GET", "POST"])
@login_required
@admin_required
def product_new():
    form = ProductForm()
    form.subcategory_id.choices = products_service.get_subcategory_choices()

    if form.validate_on_submit():
        product, error = products_service.create_product(form)

        if error:
            form.code.errors.append(error)
        else:
            flash(f"Producto {product.code} creado correctamente.", "success")
            return redirect(url_for("admin.products_list"))

    return render_template(
        "admin/products/form.html",
        form=form,
        product=None,
    )


@admin_bp.route("/products/<int:product_id>/edit", methods=["GET", "POST"])
@login_required
@admin_required
def product_edit(product_id):
    product = products_service.get_product_or_none(product_id)
    if product is None:
        flash("El producto no existe.", "danger")
        return redirect(url_for("admin.products_list"))

    form = ProductForm(obj=product)
    form.subcategory_id.choices = products_service.get_subcategory_choices()

    if form.validate_on_submit():
        updated, error = products_service.update_product(product, form)

        if error:
            form.code.errors.append(error)
        else:
            flash(f"Producto {updated.code} actualizado correctamente.", "success")
            return redirect(url_for("admin.products_list"))

    return render_template(
        "admin/products/form.html",
        form=form,
        product=product,
    )


@admin_bp.route("/products/<int:product_id>/status", methods=["POST"])
@login_required
@admin_required
def product_status(product_id):
    product = products_service.get_product_or_none(product_id)
    if product is None:
        flash("El producto no existe.", "danger")
        return redirect(url_for("admin.products_list"))

    form = StatusChangeForm()

    if form.validate_on_submit():
        ok, message = products_service.change_status(product, form.status.data)
        flash(message, "success" if ok else "warning")
    else:
        flash("No se pudo cambiar el estado del producto.", "danger")

    return redirect(url_for("admin.products_list"))
