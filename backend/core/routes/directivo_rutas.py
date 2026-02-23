from flask import Blueprint
from core.controllers.directivo_controller import DirectivoController

directivo_bp = Blueprint(
    "directivo",
    __name__,
    url_prefix="/directivos"
)

directivo_bp.route("", methods=["GET"])(DirectivoController.get_all)

directivo_bp.route("/", methods=["POST"])(DirectivoController.create)
directivo_bp.route("/<int:directivo_id>", methods=["PUT"])(DirectivoController.update)

directivo_bp.route("/asignar", methods=["POST"])(DirectivoController.asignar)
directivo_bp.route("/finalizar", methods=["PUT"])(DirectivoController.finalizar)

directivo_bp.route("/grupo/<int:grupo_id>", methods=["GET"])(
    DirectivoController.get_por_grupo
)
directivo_bp.route("/grupo/<int:grupo_id>/actuales",methods=["GET"])(DirectivoController.get_actuales)
