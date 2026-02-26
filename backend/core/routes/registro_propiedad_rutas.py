from flask import Blueprint
from core.controllers.registro_propiedad_controller import RegistrosPropiedadController

registros_propiedad_bp = Blueprint(
    "registros_propiedad",
    __name__,
    url_prefix="/registros-propiedad"
)


@registros_propiedad_bp.route("/", methods=["GET"])
def get_all():
    return RegistrosPropiedadController.get_all()

@registros_propiedad_bp.route("/<int:registro_id>", methods=["GET"])
def get_by_id(registro_id):
    return RegistrosPropiedadController.get_by_id(registro_id)

@registros_propiedad_bp.route("/", methods=["POST"])
def create():
    return RegistrosPropiedadController.create()

@registros_propiedad_bp.route("/<int:registro_id>", methods=["PUT"])
def update(registro_id):
    return RegistrosPropiedadController.update(registro_id)

@registros_propiedad_bp.route("/<int:registro_id>", methods=["DELETE"])
def delete(registro_id):
    return RegistrosPropiedadController.delete(registro_id)
