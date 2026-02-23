from core.services.rol_actividad_service import RolActividadService
from flask import jsonify, request

class RolActividadController:

    @staticmethod
    def get_all():
        try:
            return jsonify(
                RolActividadService.get_all()
            ), 200
        except Exception as e:
            return jsonify({"error": str(e)}), 400

    @staticmethod
    def get_by_id(rol_id):
        try:
            return jsonify(
                RolActividadService.get_by_id(rol_id)
            ), 200
        except Exception as e:
            return jsonify({"error": str(e)}), 404
        