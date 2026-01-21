from flask import Blueprint
from core.controllers.proyecto_investigacion_controller import (
    ProyectoInvestigacionController
)

proyecto_investigacion_bp = Blueprint(
    "proyecto_investigacion",
    __name__,
    url_prefix="/proyectos"
)

proyecto_investigacion_bp.route("/", methods=["GET"])(
    ProyectoInvestigacionController.get_all
)

proyecto_investigacion_bp.route("/<int:proyecto_id>", methods=["GET"])(
    ProyectoInvestigacionController.get_by_id
)

proyecto_investigacion_bp.route("/", methods=["POST"])(
    ProyectoInvestigacionController.create
)

proyecto_investigacion_bp.route("/<int:proyecto_id>", methods=["PUT"])(
    ProyectoInvestigacionController.update
)

proyecto_investigacion_bp.route("/<int:proyecto_id>", methods=["DELETE"])(
    ProyectoInvestigacionController.delete
)
