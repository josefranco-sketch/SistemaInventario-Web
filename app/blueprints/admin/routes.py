# ==========================================================
# Rutas del panel administrativo.
#
# Las rutas solo manejan HTTP: piden los datos a los servicios
# y renderizan templates. Los cálculos viven en app/services/.
# ==========================================================
from flask import render_template
from flask_login import login_required

from app.blueprints.admin import admin_bp
from app.blueprints.auth.decorators import admin_required
from app.services.dashboard_service import get_dashboard_summary


@admin_bp.route("/")
@login_required
@admin_required
def dashboard():
    summary = get_dashboard_summary()
    return render_template("admin/dashboard.html", summary=summary)
