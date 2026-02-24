from flask import Blueprint, request
from core.controllers.becas_controller import BecaController

beca_bp = Blueprint("beca", __name__, url_prefix="/becas")


# CRUD
@beca_bp.route("/", methods=["GET"])
def get_all():
    return BecaController.get_all()


@beca_bp.route("/<int:beca_id>", methods=["GET"])
def get_by_id(beca_id):
    return BecaController.get_by_id(beca_id)


@beca_bp.route("/", methods=["POST"])
def create():
    return BecaController.create(request)


@beca_bp.route("/<int:beca_id>", methods=["PUT"])
def update(beca_id):
    return BecaController.update(beca_id, request)


@beca_bp.route("/<int:beca_id>", methods=["DELETE"])
def delete(beca_id):
    return BecaController.delete(beca_id)


# Vincular / Desvincular
@beca_bp.route("/<int:beca_id>/vincular-becario", methods=["POST"])
def vincular_becario(beca_id):
    return BecaController.vincular_becario(beca_id, request)


@beca_bp.route("/<int:beca_id>/becarios/<int:becario_id>", methods=["DELETE"])
def desvincular_becario(beca_id, becario_id):
    return BecaController.desvincular_becario(beca_id, becario_id)


@beca_bp.route("/<int:beca_id>/becarios", methods=["GET"])
def get_becarios(beca_id):
    return BecaController.get_becarios(beca_id)

@beca_bp.route("/activas", methods=["GET"])
def get_activas():
    return BecaController.get_activas(request)

@beca_bp.route("/dashboard", methods=["GET"])
def dashboard():
    return BecaController.dashboard(request)