# ==========================================================
# Script de consola para verificar la integración
# Ventas → Inventario → Disponibilidad Pública (Sprint 6.3).
#
# Se ejecuta desde la terminal (con el entorno virtual activo):
#
#     python verify_integration.py
#
# Crea sus PROPIOS datos de prueba (producto, pedidos y
# cotización), verifica cada regla del ADR y limpia todo al
# terminar — la base queda igual que antes de correrlo, así que
# es seguro repetirlo cuantas veces se quiera.
#
# Reglas que verifica:
#  1. Producto nuevo nace Agotado (sin stock).
#  2. Una entrada de inventario lo vuelve Disponible.
#  3. Un pedido pendiente NO descuenta inventario.
#  4. Pagar el pedido SÍ descuenta, una sola vez, con historial.
#  5. La disponibilidad pública se recalcula al pagar.
#  6. Un doble pago se rechaza y no vuelve a descontar.
#  7. Un pago sin stock suficiente se rechaza sin descontar nada.
#  8. Una cotización (y su conversión a pedido) no descuentan.
# ==========================================================
from app import create_app
from app.extensions import db
from app.models.inventory import Inventory, InventoryMovement
from app.models.order import ORDER_DRAFT, Order
from app.models.product import Product
from app.models.quote import Quote
from app.models.user import User
from app.services import inventory_service, orders_service, quotes_service

CODE = "VERIF-01"  # código exclusivo del producto de esta verificación

results = []  # (nombre de la regla, pasó o no)


def check(name, passed):
    """Registra el resultado de una verificación y lo imprime."""
    results.append((name, passed))
    mark = "OK " if passed else "FALLO"
    print(f"[{mark}] {name}")
    return passed


def build_order(seller, product, quantity):
    """Crea un pedido de prueba directo (sin tocar el borrador real
    del vendedor) y lo confirma como pendiente de pago."""
    order = Order(seller_id=seller.id, code=f"VRF-{Order.query.count() + 1}")
    db.session.add(order)
    db.session.flush()

    ok, message = orders_service.add_product(order, product, quantity)
    if not ok:
        raise RuntimeError(message)

    ok, message = orders_service.confirm_order(order, "Cliente Verificación")
    if not ok:
        raise RuntimeError(message)

    return order


def cleanup(product):
    """Elimina todos los datos creados por esta verificación."""
    quotes = Quote.query.filter_by(customer_name="Cliente Verificación").all()
    for quote in quotes:
        db.session.delete(quote)

    orders = Order.query.filter(Order.code.like("VRF-%")).all()
    for order in orders:
        db.session.delete(order)

    if product is not None:
        InventoryMovement.query.filter_by(product_id=product.id).delete()
        Inventory.query.filter_by(product_id=product.id).delete()
        db.session.delete(product)

    db.session.commit()


if __name__ == "__main__":
    app = create_app()

    with app.app_context():
        print("=== Verificación de integración (Sprint 6.3) ===\n")

        admin = User.query.filter_by(role="admin").first()
        seller = User.query.filter_by(role="vendedor").first() or admin
        rosas = None

        from app.models.category import Subcategory
        rosas = Subcategory.query.filter_by(name="Rosas").first()

        # Por si una corrida anterior quedó a medias
        leftover = Product.query.filter_by(code=CODE).first()
        if leftover is not None:
            cleanup(leftover)
            print("(datos de una corrida anterior limpiados)\n")

        # --- 1. Producto nuevo nace agotado ---
        product = Product(
            code=CODE,
            name="Producto de Verificación",
            subcategory_id=rosas.id,
            price=30.00,
            commercial_presentation="Ramo de 6 unidades",
            commercial_unit="Ramo",
            availability="agotado",
        )
        db.session.add(product)
        db.session.commit()
        check("Producto nuevo nace Agotado", product.availability == "agotado")

        # --- 2. Entrada de inventario -> Disponible ---
        inventory_service.register_movement(
            product, admin, "entrada", 10, "Carga de verificación"
        )
        check(
            "Entrada de 10 lo vuelve Disponible (umbral de Rosas: "
            f"{rosas.low_stock_threshold})",
            product.availability == "disponible"
            and inventory_service.get_stock(product) == 10,
        )

        # --- 3. Pedido pendiente no descuenta ---
        order = build_order(seller, product, 3)
        check(
            "Pedido pendiente NO descuenta inventario",
            inventory_service.get_stock(product) == 10,
        )

        # --- 4. Pagar descuenta una vez, con historial ---
        ok, message = orders_service.mark_as_paid(order, seller)
        movement = (
            InventoryMovement.query.filter_by(
                product_id=product.id, movement_type="venta"
            ).first()
        )
        check(
            "Pagar descuenta una sola vez (10 → 7) y deja movimiento 'venta'",
            ok
            and inventory_service.get_stock(product) == 7
            and movement is not None
            and order.code in movement.reason,
        )

        # --- 5. Disponibilidad recalculada al pagar ---
        check(
            "Disponibilidad pública recalculada tras el pago",
            product.availability == "disponible",  # 7 > umbral 5
        )

        # --- 6. Doble pago rechazado ---
        ok, message = orders_service.mark_as_paid(order, seller)
        check(
            "Doble pago rechazado sin volver a descontar",
            not ok and inventory_service.get_stock(product) == 7,
        )

        # --- 7. Pago sin stock suficiente rechazado ---
        big_order = build_order(seller, product, 99)
        ok, message = orders_service.mark_as_paid(big_order, seller)
        check(
            "Pago sin stock suficiente rechazado sin descontar nada",
            not ok and inventory_service.get_stock(product) == 7,
        )

        # --- 8. Cotización y conversión no descuentan ---
        quote = quotes_service.create_quote_from_session({
            "customer_name": "Cliente Verificación",
            "customer_phone": "0000-0000",
            "customer_email": "",
            "items": [
                {"code": CODE, "name": product.name, "quantity": 3,
                 "price": 30.0, "subtotal": 90.0},
            ],
        })
        converted, message = quotes_service.convert_to_order(quote, seller)
        # el pedido convertido usa código PED-, lo marcamos para limpieza
        converted.code = f"VRF-{converted.id}"
        db.session.commit()
        check(
            "Cotización y su conversión a pedido no descuentan",
            inventory_service.get_stock(product) == 7,
        )

        # --- Limpieza total ---
        cleanup(product)
        still_there = Product.query.filter_by(code=CODE).first()
        check("Limpieza: la base quedó como estaba", still_there is None)

        # --- Resumen ---
        passed = 0
        for name, result in results:
            if result:
                passed += 1

        print(f"\nResultado: {passed}/{len(results)} verificaciones correctas.")
        if passed == len(results):
            print("✅ El ciclo Ventas → Inventario → Disponibilidad funciona.")
        else:
            print("❌ Hay reglas rotas: revisar antes de continuar.")
