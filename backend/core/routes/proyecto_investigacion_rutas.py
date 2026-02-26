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

@proyecto_investigacion_bp.route("/", methods=["GET"])
def get_all():
    return ProyectoInvestigacionController.get_all()

@proyecto_investigacion_bp.route("/<int:proyecto_id>", methods=["GET"])
def get_by_id(proyecto_id):
    return ProyectoInvestigacionController.get_by_id(proyecto_id)

@proyecto_investigacion_bp.route("/", methods=["POST"])
def create():
    return ProyectoInvestigacionController.create()

@proyecto_investigacion_bp.route("/<int:proyecto_id>", methods=["PUT"])
def update(proyecto_id):
    return ProyectoInvestigacionController.update(proyecto_id)

@proyecto_investigacion_bp.route("/<int:proyecto_id>", methods=["DELETE"])
def cerrar(proyecto_id):
    return ProyectoInvestigacionController.cerrar(proyecto_id)

# =========================
# BECARIOS ↔ PROYECTO

@proyecto_investigacion_bp.route("/<int:proyecto_id>/becarios", methods=["POST"])
def vincular_becarios(proyecto_id):
    return ProyectoInvestigacionController.vincular_becarios(proyecto_id)

@proyecto_investigacion_bp.route("/<int:proyecto_id>/becarios", methods=["PUT"])
def desvincular_becarios(proyecto_id):
    return ProyectoInvestigacionController.desvincular_becarios(proyecto_id)

# =========================
# INVESTIGADORES ↔ PROYECTO

@proyecto_investigacion_bp.route("/<int:proyecto_id>/investigadores", methods=["POST"])
def vincular_investigadores(proyecto_id):
    return ProyectoInvestigacionController.vincular_investigadores(proyecto_id)

@proyecto_investigacion_bp.route("/<int:proyecto_id>/investigadores", methods=["PUT"])
def desvincular_investigadores(proyecto_id):
    return ProyectoInvestigacionController.desvincular_investigadores(proyecto_id)
