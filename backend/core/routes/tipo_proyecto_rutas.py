from flask import Blueprint
from core.controllers.tipo_proyecto_controller import TipoProyectoController

tipo_proyecto_bp = Blueprint(
    "tipo_proyecto",
    __name__,
    url_prefix="/tipos-proyecto"
)

tipo_proyecto_bp.route("/", methods=["GET"])(
    TipoProyectoController.get_all
)

tipo_proyecto_bp.route("/<int:tipo_id>", methods=["GET"])(
    TipoProyectoController.get_by_id
)

tipo_proyecto_bp.route("/", methods=["POST"])(
    TipoProyectoController.create
)

tipo_proyecto_bp.route("/<int:tipo_id>", methods=["PUT"])(
    TipoProyectoController.update
)

tipo_proyecto_bp.route("/<int:tipo_id>", methods=["DELETE"])(
    TipoProyectoController.delete
)
