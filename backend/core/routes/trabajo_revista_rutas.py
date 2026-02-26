from flask import Blueprint
from core.controllers.trabajo_revista_controller import (
    TrabajosRevistasReferatoController )

trabajos_revistas_referato_bp = Blueprint(
    "trabajos_revistas_referato",
    __name__,
    url_prefix="/trabajos-revistas"
)

@trabajos_revistas_referato_bp.route("/", methods=["GET"])
def get_all():
    return TrabajosRevistasReferatoController.get_all()

@trabajos_revistas_referato_bp.route("/<int:trabajo_id>", methods=["GET"])
def get_by_id(trabajo_id):
    return TrabajosRevistasReferatoController.get_by_id(trabajo_id)

@trabajos_revistas_referato_bp.route("/", methods=["POST"])
def create():
    return TrabajosRevistasReferatoController.create()

@trabajos_revistas_referato_bp.route("/<int:trabajo_id>", methods=["PUT"])
def update(trabajo_id):
    return TrabajosRevistasReferatoController.update(trabajo_id)

@trabajos_revistas_referato_bp.route("/<int:trabajo_id>", methods=["DELETE"])
def delete(trabajo_id):
    return TrabajosRevistasReferatoController.delete(trabajo_id)

@trabajos_revistas_referato_bp.route("/<int:trabajo_id>/investigadores/", methods=["POST"])
def add_investigadores(trabajo_id):
    return TrabajosRevistasReferatoController.add_investigadores(trabajo_id)

@trabajos_revistas_referato_bp.route("/<int:trabajo_id>/investigadores/", methods=["DELETE"])
def remove_investigadores(trabajo_id):
    return TrabajosRevistasReferatoController.remove_investigadores(trabajo_id)
        