
from flask import Blueprint
from core.controllers.personal_completo_controller import PersonalCompletoController


# Este Endpoint lista todo el personal (Personal, Becarios, Investigadores) en una sola llamada, simplificando la obtención de datos completos en las cartas del frontend.


personal_completo_bp = Blueprint(
    "personal_completo",
    __name__,
    url_prefix="/personal-all"
)

@personal_completo_bp.route("/", methods=["GET"])
def listar():
    return PersonalCompletoController.listar()
