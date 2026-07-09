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
    lines = ["DIAGNOSTICO TEMPORAL DE ARRANQUE v2", "=" * 40, startup_error, ""]
    try:
        lines.append("python: " + sys.version)
        lines.append("ROOT = " + ROOT)
        lines.append("sys.path: " + " | ".join(sys.path))
        lines.append("")

        # Árbol completo de app/ tal como quedó en el bundle
        lines.append("--- árbol de app/ en el bundle ---")
        app_dir = os.path.join(ROOT, "app")
        if os.path.isdir(app_dir):
            count = 0
            for dirpath, dirnames, filenames in os.walk(app_dir):
                dirnames.sort()
                rel = os.path.relpath(dirpath, ROOT)
                lines.append(f"{rel}/: " + ", ".join(sorted(filenames)))
                count += 1
                if count > 60:
                    lines.append("(árbol truncado)")
                    break
        else:
            lines.append("¡app/ NO es un directorio en el bundle!")

        lines.append("")
        lines.append("--- resolución de imports ---")
        import importlib.util
        for name in ["app", "app.extensions", "app.blueprints",
                     "app.blueprints.public", "app.models", "app.services"]:
            try:
                spec = importlib.util.find_spec(name)
                origin = spec.origin if spec else "None"
                lines.append(f"find_spec('{name}') -> {origin}")
            except Exception as spec_error:  # noqa: BLE001
                lines.append(f"find_spec('{name}') ERROR: {spec_error}")

        lines.append("")
        lines.append("--- otros ---")
        lines.append("deploy/ existe: " + str(os.path.isdir(os.path.join(ROOT, "deploy"))))
        lines.append("templates/ existe: " + str(os.path.isdir(os.path.join(ROOT, "app", "templates"))))
    except Exception as info_error:  # noqa: BLE001
        lines.append(f"(no se pudo inspeccionar: {info_error})")

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
