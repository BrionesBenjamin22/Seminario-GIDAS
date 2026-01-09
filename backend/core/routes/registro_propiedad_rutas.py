from flask import Blueprint
from core.controllers.registro_propiedad_controller import RegistrosPropiedadController

registros_propiedad_bp = Blueprint(
    "registros_propiedad",
    __name__,
    url_prefix="/registros-propiedad"
)


registros_propiedad_bp.route("/", methods=["GET"])(
    RegistrosPropiedadController.get_all
)

registros_propiedad_bp.route("/<int:registro_id>", methods=["GET"])(
    RegistrosPropiedadController.get_by_id
)

registros_propiedad_bp.route("/", methods=["POST"])(
    RegistrosPropiedadController.create
)

registros_propiedad_bp.route("/<int:registro_id>", methods=["PUT"])(
    RegistrosPropiedadController.update
)

registros_propiedad_bp.route("/<int:registro_id>", methods=["DELETE"])(
    RegistrosPropiedadController.delete
)
