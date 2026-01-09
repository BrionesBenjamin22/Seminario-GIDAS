from flask import Blueprint, request
from core.controllers.visita_controller import (
    VisitaAcademicaController
)

visita_academica_bp = Blueprint(
    "visita_academica",
    __name__,
    url_prefix="/visitas-academicas"
)

@visita_academica_bp.route("/", methods=["POST"])
def crear():
    return VisitaAcademicaController.crear(request)

@visita_academica_bp.route("/", methods=["GET"])
def listar():
    return VisitaAcademicaController.listar(request)

@visita_academica_bp.route("/<int:id>", methods=["GET"])
def obtener(id):
    return VisitaAcademicaController.obtener_por_id(request, id)

@visita_academica_bp.route("/<int:id>", methods=["PUT"])
def actualizar(id):
    return VisitaAcademicaController.actualizar(request, id)

@visita_academica_bp.route("/<int:id>", methods=["DELETE"])
def eliminar(id):
    return VisitaAcademicaController.eliminar(request, id)
