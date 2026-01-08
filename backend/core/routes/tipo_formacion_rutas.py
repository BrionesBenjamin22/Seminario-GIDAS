from flask import Blueprint, request
from core.controllers.tipo_formacion_controller import TipoFormacionController

tipo_formacion_becario_bp = Blueprint(
    "tipo_formacion",
    __name__,
    url_prefix="/tipo-formacion"
)

@tipo_formacion_becario_bp.route("/", methods=["POST"])
def crear():
    return TipoFormacionController.crear(request)

@tipo_formacion_becario_bp.route("/", methods=["GET"])
def listar():
    return TipoFormacionController.listar(request)

@tipo_formacion_becario_bp.route("/<int:id>", methods=["GET"])
def obtener(id):
    return TipoFormacionController.obtener_por_id(request, id)

@tipo_formacion_becario_bp.route("/<int:id>", methods=["PUT"])
def actualizar(id):
    return TipoFormacionController.actualizar(request, id)

@tipo_formacion_becario_bp.route("/<int:id>", methods=["DELETE"])
def eliminar(id):
    return TipoFormacionController.eliminar(request, id)
