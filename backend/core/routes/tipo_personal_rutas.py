from flask import Blueprint, request
from core.controllers.tipo_personal_controller import TipoPersonalController

tipo_personal_bp = Blueprint(
    "tipo_personal",
    __name__,
    url_prefix="/tipo-personal"
)

# -------------------------
# Crear tipo de personal
# -------------------------

@tipo_personal_bp.route("/", methods=["POST"])
def crear():
    return TipoPersonalController.crear(request)


# -------------------------
# Listar todos
# -------------------------

@tipo_personal_bp.route("/", methods=["GET"])
def listar():
    return TipoPersonalController.listar(request)


# -------------------------
# Obtener por ID
# -------------------------

@tipo_personal_bp.route("/<int:id>", methods=["GET"])
def obtener_por_id(id):
    return TipoPersonalController.obtener_por_id(request, id)


# -------------------------
# Actualizar
# -------------------------

@tipo_personal_bp.route("/<int:id>", methods=["PUT"])
def actualizar(id):
    return TipoPersonalController.actualizar(request, id)


# -------------------------
# Eliminar
# -------------------------
@tipo_personal_bp.route("/<int:id>", methods=["DELETE"])
def eliminar(id):
    return TipoPersonalController.eliminar(request, id)
