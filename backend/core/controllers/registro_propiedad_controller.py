from flask import jsonify, request
from core.services.registro_propiedad_service import RegistrosPropiedadService

class RegistrosPropiedadController:

    @staticmethod
    def get_all():
        try:
            return jsonify(RegistrosPropiedadService.get_all()), 200
        except Exception as e:
            return jsonify({"error": str(e)}), 400

    @staticmethod
    def get_by_id(registro_id):
        try:
            return jsonify(
                RegistrosPropiedadService.get_by_id(registro_id)
            ), 200
        except Exception as e:
            return jsonify({"error": str(e)}), 404

    @staticmethod
    def create():
        try:
            data = request.get_json()
            return jsonify(
                RegistrosPropiedadService.create(data)
            ), 201
        except Exception as e:
            return jsonify({"error": str(e)}), 400

    @staticmethod
    def update(registro_id):
        try:
            data = request.get_json()
            return jsonify(
                RegistrosPropiedadService.update(registro_id, data)
            ), 200
        except Exception as e:
            return jsonify({"error": str(e)}), 400

    @staticmethod
    def delete(registro_id):
        try:
            return jsonify(
                RegistrosPropiedadService.delete(registro_id)
            ), 200
        except Exception as e:
            return jsonify({"error": str(e)}), 400
