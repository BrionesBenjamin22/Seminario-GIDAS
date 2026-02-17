from flask import Blueprint
from core.controllers.proyecto_investigacion_controller import (
    ProyectoInvestigacionController
)

proyecto_investigacion_bp = Blueprint(
    "proyecto_investigacion",
    __name__,
    url_prefix="/proyectos"
)

# =========================
# CRUD 

proyecto_investigacion_bp.route("/", methods=["GET"], strict_slashes=False)(
    ProyectoInvestigacionController.get_all
)

proyecto_investigacion_bp.route("/<int:proyecto_id>", methods=["GET"], strict_slashes=False)(
    ProyectoInvestigacionController.get_by_id
)

proyecto_investigacion_bp.route("/", methods=["POST"], strict_slashes=False)(
    ProyectoInvestigacionController.create
)

proyecto_investigacion_bp.route("/<int:proyecto_id>", methods=["PUT"], strict_slashes=False)(
    ProyectoInvestigacionController.update
)

proyecto_investigacion_bp.route("/<int:proyecto_id>", methods=["DELETE"], strict_slashes=False)(
    ProyectoInvestigacionController.cerrar
)
# =========================
# BECARIOS ↔ PROYECTO

proyecto_investigacion_bp.route("/<int:proyecto_id>/becarios", methods=["POST"], strict_slashes=False)(
    ProyectoInvestigacionController.vincular_becarios
)

proyecto_investigacion_bp.route("/<int:proyecto_id>/becarios", methods=["DELETE"], strict_slashes=False)(
    ProyectoInvestigacionController.desvincular_becarios
)

# =========================
# INVESTIGADORES ↔ PROYECTO


proyecto_investigacion_bp.route("/<int:proyecto_id>/investigadores", methods=["POST"], strict_slashes=False)(
    ProyectoInvestigacionController.vincular_investigadores
)

proyecto_investigacion_bp.route("/<int:proyecto_id>/investigadores", methods=["DELETE"], strict_slashes=False)(
    ProyectoInvestigacionController.desvincular_investigadores
)
