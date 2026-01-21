from flask import Blueprint
from core.controllers.actividad_docencia_controller import (
    ActividadDocenciaController
)

actividad_docencia_bp = Blueprint(
    "actividad_docencia",
    __name__,
    url_prefix="/actividades-docencia"
)

# -------------------------------------------------
# CRUD ACTIVIDAD DOCENCIA
# -------------------------------------------------

actividad_docencia_bp.route("/", methods=["GET"])(
    ActividadDocenciaController.get_all
)

actividad_docencia_bp.route("/<int:actividad_id>", methods=["GET"])(
    ActividadDocenciaController.get_by_id
)

actividad_docencia_bp.route("/", methods=["POST"])(
    ActividadDocenciaController.create
)

actividad_docencia_bp.route("/<int:actividad_id>", methods=["PUT"])(
    ActividadDocenciaController.update
)

actividad_docencia_bp.route("/<int:actividad_id>", methods=["DELETE"])(
    ActividadDocenciaController.delete
)
