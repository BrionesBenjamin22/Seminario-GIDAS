from flask import Blueprint
from core.controllers.tipo_registro_controller import TipoRegistroPropiedadController

tipo_registro_propiedad_bp = Blueprint(
    "tipo_registro_propiedad",
    __name__,
    url_prefix="/tipo-registro-propiedad"
)

@tipo_registro_propiedad_bp.route("/", methods=["GET"])
def get_all():
    return TipoRegistroPropiedadController.get_all()

@tipo_registro_propiedad_bp.route("/<int:tipo_id>", methods=["GET"])
def get_by_id(tipo_id):
    return TipoRegistroPropiedadController.get_by_id(tipo_id)

@tipo_registro_propiedad_bp.route("/", methods=["POST"])
def create():
    return TipoRegistroPropiedadController.create()

@tipo_registro_propiedad_bp.route("/<int:tipo_id>", methods=["PUT"])
def update(tipo_id):
    return TipoRegistroPropiedadController.update(tipo_id)

@tipo_registro_propiedad_bp.route("/<int:tipo_id>", methods=["DELETE"])
def delete(tipo_id):
    return TipoRegistroPropiedadController.delete(tipo_id)
