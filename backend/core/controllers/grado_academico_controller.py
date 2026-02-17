from core.services.grado_academico_service import GradoAcademicoService
from flask import jsonify, request

class GradoAcademicoController:

    @staticmethod
    def get_all():
        try:
            return jsonify(
                GradoAcademicoService.get_all()
            ), 200
        except Exception as e:
            return jsonify({"error": str(e)}), 400

    @staticmethod
    def get_by_id(grado_id):
        try:
            return jsonify(
                GradoAcademicoService.get_by_id(grado_id)
            ), 200
        except Exception as e:
            return jsonify({"error": str(e)}), 404