from flask import Blueprint, request
from core.controllers.fuente_financiamiento_controller import FuenteFinanciamientoController

fuente_financiamiento_bp = Blueprint(
    "fuente_financiamiento",
    __name__,
    url_prefix="/fuente-financiamiento"
)

@fuente_financiamiento_bp.route("/", methods=["POST"])
def crear():
    return FuenteFinanciamientoController.crear(request)

@fuente_financiamiento_bp.route("/", methods=["GET"])
def listar():
    return FuenteFinanciamientoController.listar(request)

@fuente_financiamiento_bp.route("/<int:id>", methods=["GET"])
def obtener(id):
    return FuenteFinanciamientoController.obtener_por_id(request, id)

@fuente_financiamiento_bp.route("/<int:id>", methods=["PUT"])
def actualizar(id):
    return FuenteFinanciamientoController.actualizar(request, id)

@fuente_financiamiento_bp.route("/<int:id>", methods=["DELETE"])
def eliminar(id):
    return FuenteFinanciamientoController.eliminar(request, id)
