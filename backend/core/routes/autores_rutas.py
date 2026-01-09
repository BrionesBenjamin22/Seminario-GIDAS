from flask import Blueprint
from core.controllers.autores_controller import AutorController

autor_bp = Blueprint(
    "autor",
    __name__,
    url_prefix="/autores"
)

autor_bp.route("/", methods=["GET"])(
    AutorController.get_all
)

autor_bp.route("/<int:autor_id>", methods=["GET"])(
    AutorController.get_by_id
)

autor_bp.route("/", methods=["POST"])(
    AutorController.create
)

autor_bp.route("/<int:autor_id>", methods=["PUT"])(
    AutorController.update
)

autor_bp.route("/<int:autor_id>", methods=["DELETE"])(
    AutorController.delete
)

# -------- RELACIÓN AUTOR - LIBRO --------

autor_bp.route("/<int:autor_id>/libros", methods=["POST"])(
    AutorController.add_libro
)

autor_bp.route("/<int:autor_id>/libros/<int:libro_id>", methods=["DELETE"])(
    AutorController.remove_libro
)
