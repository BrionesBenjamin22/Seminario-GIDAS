from flask import Blueprint
from core.controllers.erogacion_controller import ErogacionController

erogacion_bp = Blueprint(
    "erogacion",
    __name__,
    url_prefix="/erogaciones"
)

erogacion_bp.route("", methods=["GET"])(
    ErogacionController.get_all
)

erogacion_bp.route("/<int:erogacion_id>", methods=["GET"])(
    ErogacionController.get_by_id
)

erogacion_bp.route("", methods=["POST"])(
    ErogacionController.create
)

erogacion_bp.route("/<int:erogacion_id>", methods=["PUT"])(
    ErogacionController.update
)

erogacion_bp.route("/<int:erogacion_id>", methods=["DELETE"])(
    ErogacionController.delete
)
