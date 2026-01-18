from flask import Blueprint
from core.controllers.equipamiento_controller import EquipamientoController

equipamiento_bp = Blueprint(
    "equipamiento",
    __name__,
    url_prefix="/equipamiento"
)

equipamiento_bp.route("/", methods=["GET"])(
    EquipamientoController.get_all
)

equipamiento_bp.route("/<int:equipamiento_id>", methods=["GET"])(
    EquipamientoController.get_by_id
)

equipamiento_bp.route("/", methods=["POST"])(
    EquipamientoController.create
)

equipamiento_bp.route("/<int:equipamiento_id>", methods=["PUT"])(
    EquipamientoController.update
)

equipamiento_bp.route("/<int:equipamiento_id>", methods=["DELETE"])(
    EquipamientoController.delete
)
