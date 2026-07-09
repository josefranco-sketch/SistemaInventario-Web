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
# La operación real del negocio es local (ver README).
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

DEMO_DB = os.path.join(ROOT, "deploy", "demo_app.db")
RUNTIME_DB = "/tmp/app.db"

if os.environ.get("VERCEL") and not os.path.exists(RUNTIME_DB):
    shutil.copy(DEMO_DB, RUNTIME_DB)

from app import create_app

app = create_app()
