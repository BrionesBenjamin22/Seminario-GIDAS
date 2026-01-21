from flask import Blueprint
from core.controllers.trabajo_revista_controller import (
    TrabajosRevistasReferatoController )

trabajos_revistas_referato_bp = Blueprint(
    "trabajos_revistas_referato",
    __name__,
    url_prefix="/trabajos-revistas"
)

trabajos_revistas_referato_bp.route("/", methods=["GET"])(
    TrabajosRevistasReferatoController.get_all
)

trabajos_revistas_referato_bp.route("/<int:trabajo_id>", methods=["GET"])(
    TrabajosRevistasReferatoController.get_by_id
)

trabajos_revistas_referato_bp.route("/", methods=["POST"])(
    TrabajosRevistasReferatoController.create
)

trabajos_revistas_referato_bp.route("/<int:trabajo_id>", methods=["PUT"])(
    TrabajosRevistasReferatoController.update
)

trabajos_revistas_referato_bp.route("/<int:trabajo_id>", methods=["DELETE"])(
    TrabajosRevistasReferatoController.delete
)
