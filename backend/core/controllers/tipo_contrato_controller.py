from flask import jsonify, request
from core.services.tipo_contrato_service import TipoContratoService


class TipoContratoController:

    @staticmethod
    def get_all():
        try:
            return jsonify(
                TipoContratoService.get_all()
            ), 200
        except Exception as e:
            return jsonify({"error": str(e)}), 400

    @staticmethod
    def get_by_id(tipo_contrato_id):
        try:
            return jsonify(
                TipoContratoService.get_by_id(tipo_contrato_id)
            ), 200
        except Exception as e:
            return jsonify({"error": str(e)}), 404

    @staticmethod
    def create():
        try:
            data = request.get_json()
            return jsonify(
                TipoContratoService.create(data)
            ), 201
        except Exception as e:
            return jsonify({"error": str(e)}), 400

    @staticmethod
    def update(tipo_contrato_id):
        try:
            data = request.get_json()
            return jsonify(
                TipoContratoService.update(tipo_contrato_id, data)
            ), 200
        except Exception as e:
            return jsonify({"error": str(e)}), 400

    @staticmethod
    def delete(tipo_contrato_id):
        try:
            return jsonify(
                TipoContratoService.delete(tipo_contrato_id)
            ), 200
        except Exception as e:
            return jsonify({"error": str(e)}), 400
