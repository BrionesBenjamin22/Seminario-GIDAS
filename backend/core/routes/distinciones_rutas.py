from flask import Blueprint
from core.controllers.distincion_controller import DistincionRecibidaController

distincion_recibida_bp = Blueprint(
    "distincion_recibida",
    __name__,
    url_prefix="/distinciones"
)

distincion_recibida_bp.route("/", methods=["GET"])(
    DistincionRecibidaController.get_all
)

distincion_recibida_bp.route("/<int:distincion_id>", methods=["GET"])(
    DistincionRecibidaController.get_by_id
)

distincion_recibida_bp.route("/", methods=["POST"])(
    DistincionRecibidaController.create
)

distincion_recibida_bp.route("/<int:distincion_id>", methods=["PUT"])(
    DistincionRecibidaController.update
)

distincion_recibida_bp.route("/<int:distincion_id>", methods=["DELETE"])(
    DistincionRecibidaController.delete
)
