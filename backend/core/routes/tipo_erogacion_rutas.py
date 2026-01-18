from flask import Blueprint
from core.controllers.tipo_erogacion_controller import TipoErogacionController

tipo_erogacion_bp = Blueprint(
    "tipo_erogacion",
    __name__,
    url_prefix="/tipo-erogacion"
)

tipo_erogacion_bp.route("/", methods=["GET"])(
    TipoErogacionController.get_all
)

tipo_erogacion_bp.route("/<int:tipo_id>", methods=["GET"])(
    TipoErogacionController.get_by_id
)

tipo_erogacion_bp.route("/", methods=["POST"])(
    TipoErogacionController.create
)

tipo_erogacion_bp.route("/<int:tipo_id>", methods=["PUT"])(
    TipoErogacionController.update
)

tipo_erogacion_bp.route("/<int:tipo_id>", methods=["DELETE"])(
    TipoErogacionController.delete
)
