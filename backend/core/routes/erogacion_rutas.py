from flask import Blueprint, make_response
from core.controllers.erogacion_controller import ErogacionController

erogacion_bp = Blueprint(
    "erogacion",
    __name__,
    url_prefix="/erogaciones"
)

# ---- OPTIONS GLOBAL ----
@erogacion_bp.route("/", methods=["OPTIONS"], strict_slashes=False)
def erogaciones_options():
    return make_response("", 200)

@erogacion_bp.route("/<int:erogacion_id>", methods=["OPTIONS"], strict_slashes=False)
def erogaciones_id_options(erogacion_id):
    return make_response("", 200)

# ---- CRUD ----
@erogacion_bp.route("/", methods=["GET"], strict_slashes=False)
def get_all():
    return ErogacionController.get_all()

@erogacion_bp.route("/", methods=["POST"], strict_slashes=False)
def create():
    return ErogacionController.create()

@erogacion_bp.route("/<int:erogacion_id>", methods=["GET"], strict_slashes=False)
def get_by_id(erogacion_id):
    return ErogacionController.get_by_id(erogacion_id)

@erogacion_bp.route("/<int:erogacion_id>", methods=["PUT"], strict_slashes=False)
def update(erogacion_id):
    return ErogacionController.update(erogacion_id)

@erogacion_bp.route("/<int:erogacion_id>", methods=["DELETE"], strict_slashes=False)
def delete(erogacion_id):
    return ErogacionController.delete(erogacion_id)
