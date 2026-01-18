from flask import jsonify, request
from core.services.trabajo_reunion_service import (
    TrabajoReunionCientificaService
)


class TrabajoReunionCientificaController:

    @staticmethod
    def get_all():
        try:
            filtros = {
                "investigador_id": request.args.get("investigador_id", type=int),
                "grupo_utn_id": request.args.get("grupo_utn_id", type=int),
                "orden": request.args.get("orden")
            }

            return jsonify(
                TrabajoReunionCientificaService.get_all(filtros)
            ), 200

        except Exception as e:
            return jsonify({"error": str(e)}), 400

    @staticmethod
    def get_by_id(trabajo_id):
        try:
            return jsonify(
                TrabajoReunionCientificaService.get_by_id(trabajo_id)
            ), 200

        except Exception as e:
            return jsonify({"error": str(e)}), 404

    @staticmethod
    def create():
        try:
            data = request.get_json()
            return jsonify(
                TrabajoReunionCientificaService.create(data)
            ), 201

        except Exception as e:
            return jsonify({"error": str(e)}), 400

    @staticmethod
    def update(trabajo_id):
        try:
            data = request.get_json()
            return jsonify(
                TrabajoReunionCientificaService.update(trabajo_id, data)
            ), 200

        except Exception as e:
            return jsonify({"error": str(e)}), 400

    @staticmethod
    def delete(trabajo_id):
        try:
            return jsonify(
                TrabajoReunionCientificaService.delete(trabajo_id)
            ), 200

        except Exception as e:
            return jsonify({"error": str(e)}), 400
