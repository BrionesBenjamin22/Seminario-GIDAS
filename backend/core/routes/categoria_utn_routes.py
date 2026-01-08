from flask import Blueprint, request
from core.controllers.categoria_utn_controller import CategoriaUtnController

categoria_utn_bp = Blueprint(
    "categoria_utn",
    __name__,
    url_prefix="/categoria-utn"
)

@categoria_utn_bp.route("/", methods=["POST"])
def crear():
    return CategoriaUtnController.crear(request)


@categoria_utn_bp.route("/", methods=["GET"])
def listar():
    return CategoriaUtnController.listar(request)


@categoria_utn_bp.route("/<int:id>", methods=["GET"])
def obtener_por_id(id):
    return CategoriaUtnController.obtener_por_id(request, id)


@categoria_utn_bp.route("/<int:id>", methods=["PUT"])
def actualizar(id):
    return CategoriaUtnController.actualizar(request, id)


@categoria_utn_bp.route("/<int:id>", methods=["DELETE"])
def eliminar(id):
    return CategoriaUtnController.eliminar(request, id)
