# ==========================================================
# Rutas del panel administrativo.
#
# Por ahora solo existe la pantalla base protegida, que sirve
# para comprobar que el login y los roles funcionan. El
# dashboard completo (KPIs, accesos rápidos) llega en el
# Sprint 4.2.
# ==========================================================
from flask import render_template
from flask_login import login_required

from app.blueprints.admin import admin_bp
from app.blueprints.auth.decorators import admin_required


@admin_bp.route("/")
@login_required
@admin_required
def dashboard():
    return render_template("admin/dashboard.html")
