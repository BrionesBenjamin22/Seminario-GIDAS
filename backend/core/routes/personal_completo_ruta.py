
from flask import Blueprint
from core.controllers.personal_completo_controller import PersonalCompletoController
from core.services.personal_completo_service import obtener_personal_por_tipo





personal_completo_bp = Blueprint(
    "personal_completo",
    __name__,
    url_prefix="/personal-all"
)

@personal_completo_bp.route("/", methods=["GET"])
def listar():
    return PersonalCompletoController.listar()

@personal_completo_bp.route("/<string:rol>/<int:id>", methods=["GET"])
def obtener_por_id(rol, id):

    data = obtener_personal_por_tipo(rol, id)

    if not data:
        return {"error": "No encontrado"}, 404

    return data, 200
