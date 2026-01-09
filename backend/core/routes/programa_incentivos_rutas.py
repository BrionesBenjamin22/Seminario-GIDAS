from flask import Blueprint, request
from core.controllers.programa_incentivos_controller import (
    ProgramaIncentivosController
)

programa_incentivos_bp = Blueprint(
    "programa_incentivos",
    __name__,
    url_prefix="/programas-incentivos"
)

@programa_incentivos_bp.route("/", methods=["POST"])
def crear():
    return ProgramaIncentivosController.crear(request)

@programa_incentivos_bp.route("/", methods=["GET"])
def listar():
    return ProgramaIncentivosController.listar(request)

@programa_incentivos_bp.route("/<int:id>", methods=["GET"])
def obtener(id):
    return ProgramaIncentivosController.obtener_por_id(request, id)

@programa_incentivos_bp.route("/<int:id>", methods=["PUT"])
def actualizar(id):
    return ProgramaIncentivosController.actualizar(request, id)

@programa_incentivos_bp.route("/<int:id>", methods=["DELETE"])
def eliminar(id):
    return ProgramaIncentivosController.eliminar(request, id)
