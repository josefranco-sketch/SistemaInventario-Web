# ==========================================================
# Punto de entrada para Vercel (deploy de demostración).
#
# Vercel ejecuta Flask como función serverless y su sistema de
# archivos es de SOLO LECTURA (salvo /tmp). Por eso:
#
# 1. En cada arranque en frío se copia la base de demostración
#    incluida en el repo (deploy/demo_app.db) hacia /tmp/app.db,
#    que sí es escribible.
# 2. La aplicación funciona completa (login, productos, ventas),
#    pero los cambios hechos en línea son TEMPORALES: cuando la
#    función se reinicia, la demo vuelve a su estado inicial.
#
# MODO DIAGNÓSTICO TEMPORAL: si la aplicación truena al arrancar,
# en lugar del error genérico de Vercel se muestra el traceback
# real para poder corregirlo. Se retirará al cerrar el deploy.
# ==========================================================
import os
import shutil
import sys

# Raíz del proyecto (un nivel arriba de api/). Se agrega a sys.path
# para que "from app import create_app" y "from config import Config"
# funcionen también dentro de la función serverless de Vercel.
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

try:
    DEMO_DB = os.path.join(ROOT, "deploy", "demo_app.db")
    RUNTIME_DB = "/tmp/app.db"

    if os.environ.get("VERCEL") and not os.path.exists(RUNTIME_DB):
        shutil.copy(DEMO_DB, RUNTIME_DB)

    from app import create_app

    app = create_app()

except Exception:
    # --- diagnóstico temporal: exponer el error de arranque ---
    import traceback

    startup_error = traceback.format_exc()
    listing = []
    try:
        listing.append("ROOT = " + ROOT)
        listing.append("contenido de ROOT: " + ", ".join(sorted(os.listdir(ROOT))))
        api_dir = os.path.dirname(os.path.abspath(__file__))
        listing.append("contenido de api/: " + ", ".join(sorted(os.listdir(api_dir))))
        listing.append("python: " + sys.version)
    except Exception as info_error:  # noqa: BLE001
        listing.append(f"(no se pudo listar: {info_error})")

    from flask import Flask

    app = Flask(__name__)

    @app.route("/", defaults={"path": ""})
    @app.route("/<path:path>")
    def show_startup_error(path):
        body = startup_error + "\n\n" + "\n".join(listing)
        return f"<h3>Error de arranque (diagnóstico temporal)</h3><pre>{body}</pre>", 500
