from flask import Blueprint, request
from core.controllers.becario_controller import BecarioController

becario_bp = Blueprint(
    "becario",
    __name__,
    url_prefix="/becarios"
)

@becario_bp.route("/", methods=["POST"])
def crear():
    return BecarioController.crear(request)

@becario_bp.route("/", methods=["GET"])
def listar():
    return BecarioController.listar(request)

@becario_bp.route("/<int:id>", methods=["GET"])
def obtener(id):
    return BecarioController.obtener_por_id(request, id)

@becario_bp.route("/<int:id>", methods=["PUT"])
def actualizar(id):
    return BecarioController.actualizar(request, id)

@becario_bp.route("/<int:id>", methods=["DELETE"])
def eliminar(id):
    return BecarioController.eliminar(request, id)
