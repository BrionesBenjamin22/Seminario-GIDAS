from flask import Blueprint
from core.controllers.adoptante_controller import AdoptanteController

adoptante_bp = Blueprint(
    "adoptante",
    __name__,
    url_prefix="/adoptantes"
)

adoptante_bp.route("", methods=["GET"])(AdoptanteController.get_all)
adoptante_bp.route("/<int:adoptante_id>", methods=["GET"])(AdoptanteController.get_by_id)
adoptante_bp.route("", methods=["POST"])(AdoptanteController.create)
adoptante_bp.route("/<int:adoptante_id>", methods=["PUT"])(AdoptanteController.update)
