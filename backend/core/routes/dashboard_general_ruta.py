from flask import Blueprint, request
from core.controllers.dashboard_general_controller import DashboardGeneralController
from core.services.middleware import requiere_rol

dashboard_general_bp = Blueprint(
    "dashboard_general_bp",
    __name__,
    url_prefix="/dashboard/general"
)


@dashboard_general_bp.route("/", methods=["GET"])
@requiere_rol("ADMIN", "GESTOR", "LECTURA")
def obtener_dashboard_general():
    return DashboardGeneralController.obtener(request)