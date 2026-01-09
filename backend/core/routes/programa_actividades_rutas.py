from flask import Blueprint, request
from core.controllers.programa_actividades_controller import (
    PlanificacionGrupoController
)

planificacion_grupo_bp = Blueprint(
    "planificacion_grupo",
    __name__,
    url_prefix="/planificaciones"
)

@planificacion_grupo_bp.route("/", methods=["POST"])
def crear():
    return PlanificacionGrupoController.crear(request)

@planificacion_grupo_bp.route("/", methods=["GET"])
def listar():
    return PlanificacionGrupoController.listar(request)

@planificacion_grupo_bp.route("/<int:id>", methods=["GET"])
def obtener(id):
    return PlanificacionGrupoController.obtener_por_id(request, id)

@planificacion_grupo_bp.route("/<int:id>", methods=["PUT"])
def actualizar(id):
    return PlanificacionGrupoController.actualizar(request, id)

@planificacion_grupo_bp.route("/<int:id>", methods=["DELETE"])
def eliminar(id):
    return PlanificacionGrupoController.eliminar(request, id)
