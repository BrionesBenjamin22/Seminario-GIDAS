from flask import Blueprint
from core.controllers.trabajo_reunion_controller import (
    TrabajoReunionCientificaController
)

trabajo_reunion_cientifica_bp = Blueprint(
    "trabajo_reunion_cientifica",
    __name__,
    url_prefix="/trabajos-reunion-cientifica"
)

trabajo_reunion_cientifica_bp.route(
    "", methods=["GET"]
)(TrabajoReunionCientificaController.get_all)

trabajo_reunion_cientifica_bp.route(
    "/<int:trabajo_id>", methods=["GET"]
)(TrabajoReunionCientificaController.get_by_id)

trabajo_reunion_cientifica_bp.route(
    "", methods=["POST"]
)(TrabajoReunionCientificaController.create)

trabajo_reunion_cientifica_bp.route(
    "/<int:trabajo_id>", methods=["PUT"]
)(TrabajoReunionCientificaController.update)

trabajo_reunion_cientifica_bp.route(
    "/<int:trabajo_id>", methods=["DELETE"]
)(TrabajoReunionCientificaController.delete)
