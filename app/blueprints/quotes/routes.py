import re

from flask import flash, redirect, render_template, request, session, url_for

from app.models.quote import QUOTE_DEPARTMENTS
from app.services import quotes_service

from . import quotes_bp


def _parse_price(raw_price):
    if raw_price is None:
        return 0.0

    cleaned = re.sub(r"[^0-9.,]", "", str(raw_price)).replace(",", ".").strip()

    try:
        return float(cleaned)
    except ValueError:
        return 0.0


def _get_quote_state():
    return session.get(
        "quote",
        {
            "code": "COT-0001",
            "customer_name": "",
            "customer_phone": "",
            "customer_department": "",
            "customer_email": "",
            "items": [],
            "subtotal": 0.0,
            "total": 0.0,
        },
    )


def _recalculate_quote(quote):
    subtotal = sum(item["subtotal"] for item in quote["items"])
    quote["subtotal"] = subtotal
    quote["total"] = subtotal
    return quote


@quotes_bp.route("/cotizacion", methods=["GET", "POST"])
@quotes_bp.route("/cotizaciones", methods=["GET", "POST"])
def quote_home():
    quote = _get_quote_state()

    # Confirmación de una cotización recién guardada (PRG: llega por
    # GET tras el redirect del POST, y se consume una sola vez para
    # que recargar la página no la vuelva a mostrar ni la reenvíe).
    confirmation = session.pop("quote_confirmation", None)
    if confirmation is not None:
        return render_template(
            "quotes/index.html", quote=quote, confirmation=confirmation
        )

    remove_code = request.args.get("remove")

    if remove_code:
        updated_items = []

        for item in quote["items"]:
            if item["code"] == remove_code:
                if item["quantity"] > 1:
                    item["quantity"] -= 1
                    item["subtotal"] = item["price"] * item["quantity"]
                    updated_items.append(item)
                # si quantity == 1, no se agrega y se elimina la línea
            else:
                updated_items.append(item)

        quote["items"] = updated_items
        quote = _recalculate_quote(quote)

        session["quote"] = quote
        session.modified = True

        return redirect(url_for("quotes.quote_home"))

    clear_quote = request.args.get("clear")

    if clear_quote == "1":
        session.pop("quote", None)
        return redirect(url_for("quotes.quote_home"))

    if request.method == "POST":
        quote["customer_name"] = request.form.get("customer_name", "").strip()
        quote["customer_phone"] = request.form.get("customer_phone", "").strip()
        quote["customer_department"] = request.form.get("customer_department", "").strip()
        quote["customer_email"] = request.form.get("customer_email", "").strip()

        if not quote["items"]:
            flash("Agrega al menos un producto a tu cotización antes de enviarla.", "danger")
            session["quote"] = quote
            session.modified = True
            return redirect(url_for("quotes.quote_home"))

        errors = quotes_service.validate_customer_data(
            quote["customer_name"], quote["customer_phone"], quote["customer_department"]
        )

        if errors:
            for error in errors:
                flash(error, "danger")
            session["quote"] = quote
            session.modified = True
            return redirect(url_for("quotes.quote_home"))

        # Desde el Sprint 6.2 la cotización se guarda en base de datos
        # para que un vendedor la atienda (no maneja pagos ni toca
        # inventario — regla ADR).
        saved_quote = quotes_service.create_quote_from_session(quote)
        session.pop("quote", None)

        if saved_quote is None:
            flash(
                "Los productos de tu cotización ya no están disponibles; "
                "por favor arma una nueva desde el catálogo.",
                "warning",
            )
            return redirect(url_for("quotes.quote_home"))

        # Post/Redirect/Get: la confirmación viaja en sesión (se
        # consume una sola vez en el próximo GET) para que recargar
        # la página no reenvíe ni duplique la cotización.
        session["quote_confirmation"] = {
            "code": saved_quote.code,
            "customer_name": saved_quote.customer_name,
            "customer_phone": saved_quote.customer_phone,
            "customer_department": saved_quote.customer_department,
            "items": [
                {
                    "code": item.product.code,
                    "name": item.product.name,
                    "quantity": item.quantity,
                    "price": float(item.unit_price),
                    "subtotal": float(item.subtotal),
                }
                for item in saved_quote.items
            ],
            "total": float(saved_quote.total),
        }
        flash(
            f"✅ Tu cotización {saved_quote.code} fue recibida correctamente. "
            "Nos comunicaremos contigo.",
            "success",
        )
        return redirect(url_for("quotes.quote_home"))

    product_code = request.args.get("product_code", "").strip()
    product_name = request.args.get("product_name", "").strip()
    product_price = _parse_price(request.args.get("product_price"))
    quantity = request.args.get("quantity", type=int) or 1

    if quantity < 1:
        quantity = 1

    if product_code and product_name:
        existing_item = next(
            (item for item in quote["items"] if item["code"] == product_code),
            None,
        )

        if existing_item:
            existing_item["quantity"] += quantity
            existing_item["subtotal"] = existing_item["price"] * existing_item["quantity"]
        else:
            quote["items"].append(
                {
                    "code": product_code,
                    "name": product_name,
                    "quantity": quantity,
                    "price": product_price,
                    "subtotal": product_price * quantity,
                }
            )

        quote = _recalculate_quote(quote)
        session["quote"] = quote
        session.modified = True
        return redirect(url_for("quotes.quote_home"))

    return render_template(
        "quotes/index.html", quote=quote, departments=QUOTE_DEPARTMENTS
    )