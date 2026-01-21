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
