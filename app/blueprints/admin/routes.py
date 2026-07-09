# ==========================================================
# Rutas del panel administrativo.
#
# Las rutas solo manejan HTTP: leen filtros, piden los datos a
# los servicios y renderizan templates. Los cálculos y reglas
# de negocio viven en app/services/.
# ==========================================================
from flask import flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required

from app.blueprints.admin import admin_bp
from app.blueprints.admin.forms import (
    ConfirmActionForm,
    MovementForm,
    ProductForm,
    StatusChangeForm,
    ThresholdsForm,
    UserCreateForm,
    UserEditForm,
)
from app.blueprints.auth.decorators import admin_required
from app.services import inventory_service, products_service, users_service
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


# ----------------------------------------------------------
# Inventario
# ----------------------------------------------------------

@admin_bp.route("/inventory")
@login_required
@admin_required
def inventory_list():
    search = request.args.get("q", "").strip()
    category_id = request.args.get("category", type=int)
    only_low = request.args.get("low") == "1"

    products = inventory_service.get_inventory_overview(
        search=search, category_id=category_id, only_low=only_low
    )

    return render_template(
        "admin/inventory/list.html",
        products=products,
        categories=products_service.get_all_categories(),
        search=search,
        selected_category=category_id,
        only_low=only_low,
        get_stock=inventory_service.get_stock,
        get_threshold=inventory_service.get_threshold,
        is_low_stock=inventory_service.is_low_stock,
    )


@admin_bp.route("/inventory/<int:product_id>/movement", methods=["GET", "POST"])
@login_required
@admin_required
def inventory_movement(product_id):
    product = products_service.get_product_or_none(product_id)
    if product is None:
        flash("El producto no existe.", "danger")
        return redirect(url_for("admin.inventory_list"))

    form = MovementForm()

    if form.validate_on_submit():
        ok, message = inventory_service.register_movement(
            product=product,
            user=current_user,
            movement_type=form.movement_type.data,
            quantity=form.quantity.data,
            reason=form.reason.data,
        )
        flash(message, "success" if ok else "danger")

        if ok:
            return redirect(url_for("admin.inventory_list"))

    return render_template(
        "admin/inventory/movement_form.html",
        form=form,
        product=product,
        current_stock=inventory_service.get_stock(product),
        threshold=inventory_service.get_threshold(product),
    )


@admin_bp.route("/inventory/movements")
@login_required
@admin_required
def inventory_movements():
    product_id = request.args.get("product", type=int)
    product = None
    if product_id:
        product = products_service.get_product_or_none(product_id)

    movements = inventory_service.list_movements(product_id=product_id)

    return render_template(
        "admin/inventory/history.html",
        movements=movements,
        product=product,
    )


@admin_bp.route("/inventory/thresholds", methods=["GET", "POST"])
@login_required
@admin_required
def inventory_thresholds():
    form = ThresholdsForm()

    if form.validate_on_submit():
        changed, errors = inventory_service.update_thresholds(request.form)

        for error in errors:
            flash(error, "danger")

        if changed:
            flash(f"{changed} umbral(es) actualizado(s).", "success")
        elif not errors:
            flash("No hubo cambios en los umbrales.", "info")

        if not errors:
            return redirect(url_for("admin.inventory_list"))

    return render_template(
        "admin/inventory/thresholds.html",
        categories=inventory_service.get_subcategories_grouped(),
        form=form,
    )


# ----------------------------------------------------------
# Usuarios internos
# ----------------------------------------------------------

@admin_bp.route("/users")
@login_required
@admin_required
def users_list():
    search = request.args.get("q", "").strip()
    role = request.args.get("role", "").strip()

    users = users_service.list_users(search=search, role=role)

    return render_template(
        "admin/users/list.html",
        users=users,
        search=search,
        selected_role=role,
        role_labels=users_service.ROLE_LABELS,
        toggle_form=ConfirmActionForm(),
    )


@admin_bp.route("/users/new", methods=["GET", "POST"])
@login_required
@admin_required
def user_new():
    form = UserCreateForm()

    if form.validate_on_submit():
        user, error = users_service.create_user(form)

        if error:
            form.username.errors.append(error)
        else:
            flash(f"Usuario '{user.username}' creado correctamente.", "success")
            return redirect(url_for("admin.users_list"))

    return render_template("admin/users/form.html", form=form, user=None)


@admin_bp.route("/users/<int:user_id>/edit", methods=["GET", "POST"])
@login_required
@admin_required
def user_edit(user_id):
    user = users_service.get_user_or_none(user_id)
    if user is None:
        flash("El usuario no existe.", "danger")
        return redirect(url_for("admin.users_list"))

    # obj=user precarga usuario, nombre y rol; los campos de
    # contraseña son PasswordField y nunca se precargan.
    form = UserEditForm(obj=user)

    if form.validate_on_submit():
        updated, error = users_service.update_user(user, form, current_user)

        if error:
            form.username.errors.append(error)
        else:
            flash(f"Usuario '{updated.username}' actualizado.", "success")
            return redirect(url_for("admin.users_list"))

    return render_template("admin/users/form.html", form=form, user=user)


@admin_bp.route("/users/<int:user_id>/toggle", methods=["POST"])
@login_required
@admin_required
def user_toggle(user_id):
    user = users_service.get_user_or_none(user_id)
    if user is None:
        flash("El usuario no existe.", "danger")
        return redirect(url_for("admin.users_list"))

    form = ConfirmActionForm()

    if form.validate_on_submit():
        ok, message = users_service.toggle_active(user, current_user)
        flash(message, "success" if ok else "warning")
    else:
        flash("No se pudo cambiar el estado del usuario.", "danger")

    return redirect(url_for("admin.users_list"))
