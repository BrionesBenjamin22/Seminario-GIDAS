from flask import Blueprint
from core.controllers.tipo_reunion_controller import TipoReunionController

tipo_reunion_bp = Blueprint(
    "tipo_reunion",
    __name__,
    url_prefix="/tipos-reunion-cientifica"
)

tipo_reunion_bp.route(
    "", methods=["GET"]
)(TipoReunionController.get_all)