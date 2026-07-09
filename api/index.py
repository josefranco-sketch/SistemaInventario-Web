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
# IMPORTANTE: el builder de Vercel exige que la variable "app"
# esté asignada al NIVEL SUPERIOR de este archivo (por eso la
# carga vive en funciones y la asignación queda hasta abajo).
#
# Incluye un diagnóstico temporal: si la aplicación truena al
# arrancar, se sirve el traceback real (WSGI puro, sin
# dependencias) en lugar del error genérico de Vercel.
# ==========================================================
import os
import shutil
import sys
import traceback

# Raíz del proyecto (un nivel arriba de api/), agregada a sys.path
# para que "from app import create_app" resuelva dentro de la función.
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)


def _load_real_app():
    """Prepara la base de demostración y construye la aplicación."""
    demo_db = os.path.join(ROOT, "deploy", "demo_app.db")
    runtime_db = "/tmp/app.db"

    if os.environ.get("VERCEL") and not os.path.exists(runtime_db):
        shutil.copy(demo_db, runtime_db)

    from app import create_app

    return create_app()


def _build_diagnostic_app(startup_error):
    """Fallback WSGI puro (sin dependencias) que muestra el error
    de arranque. Diagnóstico temporal; se retirará al cerrar el deploy."""
    lines = ["DIAGNOSTICO TEMPORAL DE ARRANQUE", "=" * 40, startup_error, ""]
    try:
        lines.append("python: " + sys.version)
        lines.append("ROOT = " + ROOT)
        lines.append("contenido de ROOT: " + ", ".join(sorted(os.listdir(ROOT))))
        api_dir = os.path.dirname(os.path.abspath(__file__))
        lines.append("contenido de api/: " + ", ".join(sorted(os.listdir(api_dir))))
        lines.append("sys.path: " + " | ".join(sys.path))
    except Exception as info_error:  # noqa: BLE001
        lines.append(f"(no se pudo listar: {info_error})")

    body = "\n".join(lines).encode("utf-8")

    def diagnostic_app(environ, start_response):
        start_response(
            "500 INTERNAL SERVER ERROR",
            [("Content-Type", "text/plain; charset=utf-8")],
        )
        return [body]

    return diagnostic_app


try:
    _wsgi_app = _load_real_app()
except Exception:  # noqa: BLE001
    _wsgi_app = _build_diagnostic_app(traceback.format_exc())

# Asignación al nivel superior: es lo que Vercel busca en este archivo
app = _wsgi_app
