from core.controllers.rol_actividad_controller import RolActividadController
from flask import Blueprint

rol_actividad_bp = Blueprint('rol_actividad', __name__)

@rol_actividad_bp.route('/rol-actividad', methods=['GET'])
def get_all_rol_actividad():
    return RolActividadController.get_all()

@rol_actividad_bp.route('/rol-actividad/<int:rol_id>', methods=['GET'])
def get_rol_actividad_by_id(rol_id):
    return RolActividadController.get_by_id(rol_id)

@rol_actividad_bp.route('/rol-actividad', methods=['POST'])
def create_rol_actividad():
    return RolActividadController.create()

@rol_actividad_bp.route('/rol-actividad/<int:rol_id>', methods=['PUT'])
def update_rol_actividad(rol_id):
    return RolActividadController.update(rol_id)

@rol_actividad_bp.route('/rol-actividad/<int:rol_id>', methods=['DELETE'])
def delete_rol_actividad(rol_id):
    return RolActividadController.delete(rol_id)

