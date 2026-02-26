from flask import Blueprint
from core.controllers.distincion_controller import DistincionRecibidaController

distincion_recibida_bp = Blueprint(
    "distincion_recibida",
    __name__,
    url_prefix="/distinciones"
)

@distincion_recibida_bp.route("/", methods=["GET"])
def get_all():
    return DistincionRecibidaController.get_all()

@distincion_recibida_bp.route("/<int:distincion_id>", methods=["GET"])
def get_by_id(distincion_id):
    return DistincionRecibidaController.get_by_id(distincion_id)

@distincion_recibida_bp.route("/", methods=["POST"])
def create():
    return DistincionRecibidaController.create()

@distincion_recibida_bp.route("/<int:distincion_id>", methods=["PUT"])
def update(distincion_id):
    return DistincionRecibidaController.update(distincion_id)

@distincion_recibida_bp.route("/<int:distincion_id>", methods=["DELETE"])
def delete(distincion_id):
    return DistincionRecibidaController.delete(distincion_id)
