from flask import jsonify, request
from core.services.transferencia_service import (
    TransferenciaSocioProductivaService
)


class TransferenciaSocioProductivaController:

    @staticmethod
    def get_all():
        try:
            filtros = {
                "grupo_utn_id": request.args.get("grupo_utn_id", type=int),
                "tipo_contrato_id": request.args.get("tipo_contrato_id", type=int)
            }

            return jsonify(
                TransferenciaSocioProductivaService.get_all(filtros)
            ), 200

        except Exception as e:
            return jsonify({"error": str(e)}), 400

    @staticmethod
    def get_by_id(transferencia_id):
        try:
            return jsonify(
                TransferenciaSocioProductivaService.get_by_id(transferencia_id)
            ), 200

        except Exception as e:
            return jsonify({"error": str(e)}), 404

    @staticmethod
    def create():
        try:
            data = request.get_json()
            return jsonify(
                TransferenciaSocioProductivaService.create(data)
            ), 201

        except Exception as e:
            return jsonify({"error": str(e)}), 400

    @staticmethod
    def update(transferencia_id):
        try:
            data = request.get_json()
            return jsonify(
                TransferenciaSocioProductivaService.update(transferencia_id, data)
            ), 200

        except Exception as e:
            return jsonify({"error": str(e)}), 400

    @staticmethod
    def delete(transferencia_id):
        try:
            return jsonify(
                TransferenciaSocioProductivaService.delete(transferencia_id)
            ), 200

        except Exception as e:
            return jsonify({"error": str(e)}), 400

    @staticmethod
    def add_adoptantes(transferencia_id):
        try:
            data = request.get_json()

            if not data:
                return jsonify({"error": "Body requerido"}), 400

            adoptantes_ids = data.get("adoptantes_ids")

            if not isinstance(adoptantes_ids, list) or not adoptantes_ids:
                return jsonify({
                    "error": "adoptantes_ids debe ser una lista no vacía"
                }), 400

            result = TransferenciaSocioProductivaService.add_adoptantes(
                transferencia_id,
                adoptantes_ids
            )

            return jsonify(result), 200

        except ValueError as e:
            return jsonify({"error": str(e)}), 400

        except Exception:
            return jsonify({"error": "Error interno del servidor"}), 500


    @staticmethod
    def remove_adoptantes(transferencia_id):
        try:
            data = request.get_json()

            if not data:
                return jsonify({"error": "Body requerido"}), 400

            adoptantes_ids = data.get("adoptantes_ids")

            if not isinstance(adoptantes_ids, list) or not adoptantes_ids:
                return jsonify({
                    "error": "adoptantes_ids debe ser una lista no vacía"
                }), 400

            result = TransferenciaSocioProductivaService.remove_adoptantes(
                transferencia_id,
                adoptantes_ids
            )

            return jsonify(result), 200

        except ValueError as e:
            return jsonify({"error": str(e)}), 400

        except Exception:
            return jsonify({"error": "Error interno del servidor"}), 500
