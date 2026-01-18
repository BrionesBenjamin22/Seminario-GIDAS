from flask import Blueprint, request
from core.controllers.investigador_controller import InvestigadorController

investigador_bp = Blueprint(
    "investigador",
    __name__,
    url_prefix="/investigadores"
)

@investigador_bp.route("", methods=["POST"])
def crear():
    return InvestigadorController.crear(request)

@investigador_bp.route("", methods=["GET"])
def listar():
    return InvestigadorController.listar(request)

@investigador_bp.route("/<int:id>", methods=["GET"])
def obtener(id):
    return InvestigadorController.obtener_por_id(request, id)

@investigador_bp.route("/<int:id>", methods=["PUT"])
def actualizar(id):
    return InvestigadorController.actualizar(request, id)

@investigador_bp.route("/<int:id>", methods=["DELETE"])
def eliminar(id):
    return InvestigadorController.eliminar(request, id)
