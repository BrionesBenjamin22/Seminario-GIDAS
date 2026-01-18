from flask import jsonify, request
from core.services.erogacion_service import ErogacionService

class ErogacionController:

    @staticmethod
    def get_all():
        try:
            return jsonify(ErogacionService.get_all()), 200
        except Exception as e:
            return jsonify({"error": str(e)}), 400

    @staticmethod
    def get_by_id(erogacion_id):
        try:
            return jsonify(
                ErogacionService.get_by_id(erogacion_id)
            ), 200
        except Exception as e:
            return jsonify({"error": str(e)}), 404

    @staticmethod
    def create():
        try:
            data = request.get_json()
            return jsonify(
                ErogacionService.create(data)
            ), 201
        except Exception as e:
            return jsonify({"error": str(e)}), 400

    @staticmethod
    def update(erogacion_id):
        try:
            data = request.get_json()
            return jsonify(
                ErogacionService.update(erogacion_id, data)
            ), 200
        except Exception as e:
            return jsonify({"error": str(e)}), 400

    @staticmethod
    def delete(erogacion_id):
        try:
            return jsonify(
                ErogacionService.delete(erogacion_id)
            ), 200
        except Exception as e:
            return jsonify({"error": str(e)}), 400
