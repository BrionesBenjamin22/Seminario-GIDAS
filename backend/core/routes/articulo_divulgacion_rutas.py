from flask import Blueprint, request
from core.controllers.articulo_divulgacion_controller import (
    ArticuloDivulgacionController
)
from core.services.middleware import requiere_rol

articulo_divulgacion_bp = Blueprint(
    "articulo_divulgacion_bp",
    __name__,
    url_prefix="/articulos-divulgacion"
)

# -------------------------------------------------
# CREATE (ADMIN o GESTOR)
# -------------------------------------------------
@articulo_divulgacion_bp.route("/", methods=["POST"])
@requiere_rol("ADMIN", "GESTOR")
def crear():
    return ArticuloDivulgacionController.crear(request)


# -------------------------------------------------
# LISTAR (todos pueden leer)
# -------------------------------------------------
@articulo_divulgacion_bp.route("/", methods=["GET"])
@requiere_rol("ADMIN", "GESTOR", "LECTURA")
def listar():
    return ArticuloDivulgacionController.listar(request)


# -------------------------------------------------
# OBTENER POR ID
# -------------------------------------------------
@articulo_divulgacion_bp.route("/<int:articulo_id>", methods=["GET"])
@requiere_rol("ADMIN", "GESTOR", "LECTURA")
def obtener_por_id(articulo_id):
    return ArticuloDivulgacionController.obtener_por_id(request, articulo_id)


# -------------------------------------------------
# ACTUALIZAR (ADMIN o GESTOR)
# -------------------------------------------------
@articulo_divulgacion_bp.route("/<int:articulo_id>", methods=["PUT"])
@requiere_rol("ADMIN", "GESTOR")
def actualizar(articulo_id):
    return ArticuloDivulgacionController.actualizar(request, articulo_id)


# -------------------------------------------------
# ELIMINAR (solo ADMIN)
# -------------------------------------------------
@articulo_divulgacion_bp.route("/<int:articulo_id>", methods=["DELETE"])
@requiere_rol("ADMIN")
def eliminar(articulo_id):
    return ArticuloDivulgacionController.eliminar(request, articulo_id)