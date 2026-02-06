from flask import jsonify, request
from core.services.erogacion_service import ErogacionService


class ErogacionController:

    @staticmethod
    def get_all():
        try:
            filters = request.args.to_dict()
            return jsonify(
                ErogacionService.get_all(filters)
            ), 200
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
        data = request.get_json(silent=True)

        if not data:
            return jsonify({"error": "Body JSON requerido"}), 400

        try:
            return jsonify(ErogacionService.create(data)), 201
        except Exception as e:
            print("ERROR REAL:", e)
            return jsonify({"error": str(e)}), 400


    @staticmethod
    def update(erogacion_id):
        try:
            data = request.get_json()
            if not data:
                return jsonify({"error": "El body es obligatorio"}), 400

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
