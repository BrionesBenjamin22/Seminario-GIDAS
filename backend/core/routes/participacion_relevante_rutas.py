from flask import Blueprint
from core.controllers.participacion_relevante_controller import (
    ParticipacionRelevanteController
)

participacion_relevante_bp = Blueprint(
    "participacion_relevante",
    __name__,
    url_prefix="/participaciones-relevantes"
)

@participacion_relevante_bp.route("/", methods=["GET"])
def get_all():
    return ParticipacionRelevanteController.get_all()

@participacion_relevante_bp.route("/<int:participacion_id>", methods=["GET"])
def get_by_id(participacion_id):
    return ParticipacionRelevanteController.get_by_id(participacion_id)

@participacion_relevante_bp.route("/", methods=["POST"])
def create():
    return ParticipacionRelevanteController.create()

@participacion_relevante_bp.route("/<int:participacion_id>", methods=["PUT"])
def update(participacion_id):
    return ParticipacionRelevanteController.update(participacion_id)

@participacion_relevante_bp.route("/<int:participacion_id>", methods=["DELETE"])
def delete(participacion_id):
    return ParticipacionRelevanteController.delete(participacion_id)
