from core.controllers.grado_academico_controller import GradoAcademicoController
from flask import Blueprint

grado_academico_bp = Blueprint(
    "grado_academico",
    __name__,
    url_prefix="/grado-academico")

grado_academico_bp.route("", methods=["GET"])(
    GradoAcademicoController.get_all
)

grado_academico_bp.route("/<int:grado_id>", methods=["GET"])(
    GradoAcademicoController.get_by_id
)