from flask import jsonify, request
from core.services.proyecto_investigacion_service import ProyectoInvestigacionService

class ProyectoInvestigacionController:

    @staticmethod
    def get_all():
        try:
            filters = request.args.to_dict()
            return jsonify(
                ProyectoInvestigacionService.get_all(filters)
            ), 200
        except Exception as e:
            return jsonify({"error": str(e)}), 400


    @staticmethod
    def get_by_id(proyecto_id):
        try:
            return jsonify(
                ProyectoInvestigacionService.get_by_id(proyecto_id)
            ), 200
        except Exception as e:
            return jsonify({"error": str(e)}), 404


    @staticmethod
    def create():
        try:
            data = request.get_json()
            return jsonify(
                ProyectoInvestigacionService.create(data)
            ), 201
        except Exception as e:
            return jsonify({"error": str(e)}), 400


    @staticmethod
    def update(proyecto_id):
        try:
            data = request.get_json()
            return jsonify(
                ProyectoInvestigacionService.update(proyecto_id, data)
            ), 200
        except Exception as e:
            return jsonify({"error": str(e)}), 400


    @staticmethod
    def delete(proyecto_id):
        try:
            return jsonify(
                ProyectoInvestigacionService.delete(proyecto_id)
            ), 200
        except Exception as e:
            return jsonify({"error": str(e)}), 400
