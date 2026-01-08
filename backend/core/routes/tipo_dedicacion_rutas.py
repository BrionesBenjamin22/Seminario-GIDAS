from flask import Blueprint, request
from core.controllers.tipo_dedicacion_controller import TipoDedicacionController

tipo_dedicacion_bp = Blueprint(
    "tipo_dedicacion",
    __name__,
    url_prefix="/tipo-dedicacion"
)

@tipo_dedicacion_bp.route("/", methods=["POST"])
def crear():
    return TipoDedicacionController.crear(request)

@tipo_dedicacion_bp.route("/", methods=["GET"])
def listar():
    return TipoDedicacionController.listar(request)

@tipo_dedicacion_bp.route("/<int:id>", methods=["GET"])
def obtener(id):
    return TipoDedicacionController.obtener_por_id(request, id)

@tipo_dedicacion_bp.route("/<int:id>", methods=["PUT"])
def actualizar(id):
    return TipoDedicacionController.actualizar(request, id)

@tipo_dedicacion_bp.route("/<int:id>", methods=["DELETE"])
def eliminar(id):
    return TipoDedicacionController.eliminar(request, id)
