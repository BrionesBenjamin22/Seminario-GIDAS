from flask import Blueprint, request
from core.controllers.grupo_controller import GrupoUtnController

grupo_utn_bp = Blueprint(
    "grupo_utn",
    __name__,
    url_prefix="/grupo-utn"
)

# -------------------------
# Crear grupo UTN
# -------------------------
@grupo_utn_bp.route("/", methods=["POST"], strict_slashes=False)
def crear():
    return GrupoUtnController.crear(request)

# -------------------------
# Obtener grupo UTN
# -------------------------
@grupo_utn_bp.route("/", methods=["GET"], strict_slashes=False)
def obtener():
    return GrupoUtnController.obtener(request)


# -------------------------
# Actualizar grupo UTN
# -------------------------
@grupo_utn_bp.route("/", methods=["PUT"], strict_slashes=False)
def actualizar():
    return GrupoUtnController.actualizar(request)

# -------------------------
# Eliminar grupo UTN
# -------------------------
@grupo_utn_bp.route("/", methods=["DELETE"], strict_slashes=False)
def eliminar():
    return GrupoUtnController.eliminar(request)
