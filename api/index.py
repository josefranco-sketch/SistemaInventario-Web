# ==========================================================
# Punto de entrada para Vercel (deploy de demostración).
#
# Vercel ejecuta Flask como función serverless y su sistema de
# archivos es de SOLO LECTURA (salvo /tmp). Por eso, en cada
# arranque en frío se copia la base de demostración incluida en
# el repo (deploy/demo_app.db) hacia /tmp/app.db, que sí es
# escribible. La demo funciona completa, pero los cambios en
# línea son temporales: al reiniciarse la función, la demo
# vuelve a su estado inicial. La operación real es local.
#
# NOTAS aprendidas en este deploy (Sprint 8.2):
# - El builder exige que "app" esté asignada al NIVEL SUPERIOR
#   de este archivo.
# - Vercel excluye del bundle cualquier carpeta llamada "public"
#   (por eso el módulo público vive en app/blueprints/site y
#   app/templates/site, con el blueprint aún llamado "public").
# ==========================================================
import os
import shutil
import sys

# Raíz del proyecto (un nivel arriba de api/), agregada a sys.path
# para que "from app import create_app" resuelva dentro de la función.
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

DEMO_DB = os.path.join(ROOT, "deploy", "demo_app.db")
RUNTIME_DB = "/tmp/app.db"

if os.environ.get("VERCEL") and not os.path.exists(RUNTIME_DB):
    shutil.copy(DEMO_DB, RUNTIME_DB)

from app import create_app

# Asignación al nivel superior: es lo que Vercel busca en este archivo
app = create_app()
