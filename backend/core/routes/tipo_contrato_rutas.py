from flask import Blueprint
from core.controllers.tipo_contrato_controller import TipoContratoController

tipo_contrato_bp = Blueprint(
    "tipo_contrato",
    __name__,
    url_prefix="/tipo-contrato"
)

tipo_contrato_bp.route("/", methods=["GET"])(
    TipoContratoController.get_all
)

tipo_contrato_bp.route("/<int:tipo_contrato_id>", methods=["GET"])(
    TipoContratoController.get_by_id
)

tipo_contrato_bp.route("/", methods=["POST"])(
    TipoContratoController.create
)

tipo_contrato_bp.route("/<int:tipo_contrato_id>", methods=["PUT"])(
    TipoContratoController.update
)

tipo_contrato_bp.route("/<int:tipo_contrato_id>", methods=["DELETE"])(
    TipoContratoController.delete
)
