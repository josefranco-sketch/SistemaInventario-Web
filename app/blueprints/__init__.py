# Paquete de blueprints de la aplicación.
#
# Este __init__.py es necesario para que app/blueprints sea un paquete
# regular de Python: localmente funcionaba sin él (namespace package),
# pero el empaquetador de Vercel no rastrea paquetes sin __init__.py y
# dejaba fuera los blueprints del deploy (Sprint 8.2).
