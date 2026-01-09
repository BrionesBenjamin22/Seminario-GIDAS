from flask import Blueprint
from core.controllers.documentacion_controller import (
    DocumentacionBibliograficaController
)

documentacion_bibliografica_bp = Blueprint(
    "documentacion_bibliografica",
    __name__,
    url_prefix="/documentacion-bibliografica"
)

documentacion_bibliografica_bp.route("/", methods=["GET"])(
    DocumentacionBibliograficaController.get_all
)

documentacion_bibliografica_bp.route("/<int:doc_id>", methods=["GET"])(
    DocumentacionBibliograficaController.get_by_id
)

documentacion_bibliografica_bp.route("/", methods=["POST"])(
    DocumentacionBibliograficaController.create
)

documentacion_bibliografica_bp.route("/<int:doc_id>", methods=["PUT"])(
    DocumentacionBibliograficaController.update
)

documentacion_bibliografica_bp.route("/<int:doc_id>", methods=["DELETE"])(
    DocumentacionBibliograficaController.delete
)

# -------- RELACIÓN DOCUMENTO - AUTOR --------

documentacion_bibliografica_bp.route(
    "/<int:doc_id>/autores",
    methods=["POST"]
)(
    DocumentacionBibliograficaController.add_autor
)

documentacion_bibliografica_bp.route(
    "/<int:doc_id>/autores/<int:autor_id>",
    methods=["DELETE"]
)(
    DocumentacionBibliograficaController.remove_autor
)
