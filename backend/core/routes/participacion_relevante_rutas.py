from flask import Blueprint
from core.controllers.participacion_relevante_controller import (
    ParticipacionRelevanteController
)

participacion_relevante_bp = Blueprint(
    "participacion_relevante",
    __name__,
    url_prefix="/participaciones-relevantes"
)

participacion_relevante_bp.route("/", methods=["GET"])(
    ParticipacionRelevanteController.get_all
)

participacion_relevante_bp.route("/<int:participacion_id>", methods=["GET"])(
    ParticipacionRelevanteController.get_by_id
)

participacion_relevante_bp.route("/", methods=["POST"])(
    ParticipacionRelevanteController.create
)

participacion_relevante_bp.route("/<int:participacion_id>", methods=["PUT"])(
    ParticipacionRelevanteController.update
)

participacion_relevante_bp.route("/<int:participacion_id>", methods=["DELETE"])(
    ParticipacionRelevanteController.delete
)
