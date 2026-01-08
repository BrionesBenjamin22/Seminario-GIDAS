from flask import Blueprint, request
from core.controllers.grupo_controller import GrupoUtnController

grupo_utn_bp = Blueprint(
    "grupo_utn",
    __name__,
    url_prefix="/grupo-utn"
)

# -------------------------
# Obtener grupo UTN
# -------------------------
@grupo_utn_bp.route("/", methods=["GET"])
def obtener():
    return GrupoUtnController.obtener(request)


# -------------------------
# Actualizar grupo UTN
# -------------------------
@grupo_utn_bp.route("/", methods=["PUT"])
def actualizar():
    return GrupoUtnController.actualizar(request)
