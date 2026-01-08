from flask import Blueprint, request
from core.controllers.personal_controller import PersonalController

personal_bp = Blueprint(
    "personal",
    __name__,
    url_prefix="/personal"
)

@personal_bp.route("/", methods=["POST"])
def crear():
    return PersonalController.crear(request)

@personal_bp.route("/", methods=["GET"])
def listar():
    return PersonalController.listar(request)

@personal_bp.route("/<int:id>", methods=["GET"])
def obtener(id):
    return PersonalController.obtener_por_id(request, id)

@personal_bp.route("/<int:id>", methods=["PUT"])
def actualizar(id):
    return PersonalController.actualizar(request, id)

@personal_bp.route("/<int:id>", methods=["DELETE"])
def eliminar(id):
    return PersonalController.eliminar(request, id)
