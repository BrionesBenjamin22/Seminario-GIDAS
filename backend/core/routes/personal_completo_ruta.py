
from flask import Blueprint
from core.controllers.personal_completo_controller import PersonalCompletoController

personal_completo_bp = Blueprint(
    "personal_completo",
    __name__,
    url_prefix="/personal-completo"
)

@personal_completo_bp.route("/", methods=["GET"])
def listar():
    return PersonalCompletoController.listar()
