from flask import Blueprint, request
from core.controllers.articulo_divulgacion_controller import (
    ArticuloDivulgacionController
)

articulo_divulgacion_bp = Blueprint(
    "articulo_divulgacion_bp",
    __name__,
    url_prefix="/articulos-divulgacion"
)


# -------------------------------------------------
# CREATE
# -------------------------------------------------
@articulo_divulgacion_bp.route("/", methods=["POST"])
def crear():
    return ArticuloDivulgacionController.crear(request)


# -------------------------------------------------
# LISTAR
# -------------------------------------------------
@articulo_divulgacion_bp.route("/", methods=["GET"])
def listar():
    return ArticuloDivulgacionController.listar(request)


# -------------------------------------------------
# OBTENER POR ID
# -------------------------------------------------
@articulo_divulgacion_bp.route("/<int:articulo_id>", methods=["GET"])
def obtener_por_id(articulo_id):
    return ArticuloDivulgacionController.obtener_por_id(request, articulo_id)


# -------------------------------------------------
# ACTUALIZAR
# -------------------------------------------------
@articulo_divulgacion_bp.route("/<int:articulo_id>", methods=["PUT"])
def actualizar(articulo_id):
    return ArticuloDivulgacionController.actualizar(request, articulo_id)


# -------------------------------------------------
# ELIMINAR
# -------------------------------------------------
@articulo_divulgacion_bp.route("/<int:articulo_id>", methods=["DELETE"])
def eliminar(articulo_id):
    return ArticuloDivulgacionController.eliminar(request, articulo_id)