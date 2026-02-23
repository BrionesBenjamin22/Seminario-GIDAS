from flask import Blueprint
from core.controllers.transferencia_socio_controller import (
    TransferenciaSocioProductivaController
)

transferencia_socio_productiva_bp = Blueprint(
    "transferencia_socio_productiva",
    __name__,
    url_prefix="/transferencias"
)

transferencia_socio_productiva_bp.route("/", methods=["GET"])(
    TransferenciaSocioProductivaController.get_all
)

transferencia_socio_productiva_bp.route("/<int:transferencia_id>", methods=["GET"])(
    TransferenciaSocioProductivaController.get_by_id
)

transferencia_socio_productiva_bp.route("/", methods=["POST"])(
    TransferenciaSocioProductivaController.create
)

transferencia_socio_productiva_bp.route("/<int:transferencia_id>", methods=["PUT"])(
    TransferenciaSocioProductivaController.update
)

transferencia_socio_productiva_bp.route("/<int:transferencia_id>", methods=["DELETE"])(
    TransferenciaSocioProductivaController.delete
)

transferencia_socio_productiva_bp.route("/<int:transferencia_id>/adoptantes", methods=["POST"])(
    TransferenciaSocioProductivaController.add_adoptantes
)

transferencia_socio_productiva_bp.route("/<int:transferencia_id>/adoptantes", methods=["DELETE"])(
    TransferenciaSocioProductivaController.remove_adoptantes
)