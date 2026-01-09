from flask import Blueprint
from core.controllers.tipo_registro_controller import TipoRegistroPropiedadController

tipo_registro_propiedad_bp = Blueprint(
    "tipo_registro_propiedad",
    __name__,
    url_prefix="/tipo-registro-propiedad"
)

tipo_registro_propiedad_bp.route("/", methods=["GET"])(
    TipoRegistroPropiedadController.get_all
)

tipo_registro_propiedad_bp.route("/<int:tipo_id>", methods=["GET"])(
    TipoRegistroPropiedadController.get_by_id
)

tipo_registro_propiedad_bp.route("/", methods=["POST"])(
    TipoRegistroPropiedadController.create
)

tipo_registro_propiedad_bp.route("/<int:tipo_id>", methods=["PUT"])(
    TipoRegistroPropiedadController.update
)

tipo_registro_propiedad_bp.route("/<int:tipo_id>", methods=["DELETE"])(
    TipoRegistroPropiedadController.delete
)
