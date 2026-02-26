from flask import Blueprint
from core.controllers.trabajo_reunion_controller import (
    TrabajoReunionCientificaController
)

trabajo_reunion_cientifica_bp = Blueprint(
    "trabajo_reunion_cientifica",
    __name__,
    url_prefix="/trabajos-reunion-cientifica"
)

@trabajo_reunion_cientifica_bp.route("/", methods=["GET"])
def get_all():
    return TrabajoReunionCientificaController.get_all()

@trabajo_reunion_cientifica_bp.route("/<int:trabajo_id>", methods=["GET"])
def get_by_id(trabajo_id):
    return TrabajoReunionCientificaController.get_by_id(trabajo_id)

@trabajo_reunion_cientifica_bp.route("/", methods=["POST"])
def create():
    return TrabajoReunionCientificaController.create()

@trabajo_reunion_cientifica_bp.route("/<int:trabajo_id>", methods=["PUT"])
def update(trabajo_id):
    return TrabajoReunionCientificaController.update(trabajo_id)

@trabajo_reunion_cientifica_bp.route("/<int:trabajo_id>", methods=["DELETE"])
def delete(trabajo_id):
    return TrabajoReunionCientificaController.delete(trabajo_id)

@trabajo_reunion_cientifica_bp.route("/<int:trabajo_id>/investigadores/", methods=["POST"])
def add_investigadores(trabajo_id):
    return TrabajoReunionCientificaController.add_investigadores(trabajo_id)

@trabajo_reunion_cientifica_bp.route("/<int:trabajo_id>/investigadores/", methods=["DELETE"])
def remove_investigadores(trabajo_id):
    return TrabajoReunionCientificaController.remove_investigadores(trabajo_id)