from flask import jsonify, request
from core.services.trabajo_revista_service import (
    TrabajosRevistasReferatoService
)

class TrabajosRevistasReferatoController:

    @staticmethod
    def get_all():
        try:
            filters = request.args.to_dict()
            return jsonify(
                TrabajosRevistasReferatoService.get_all(filters)
            ), 200
        except Exception as e:
            return jsonify({"error": str(e)}), 400


    @staticmethod
    def get_by_id(trabajo_id):
        try:
            return jsonify(
                TrabajosRevistasReferatoService.get_by_id(trabajo_id)
            ), 200
        except Exception as e:
            return jsonify({"error": str(e)}), 404


    @staticmethod
    def create():
        try:
            data = request.get_json()
            return jsonify(
                TrabajosRevistasReferatoService.create(data)
            ), 201
        except Exception as e:
            return jsonify({"error": str(e)}), 400


    @staticmethod
    def update(trabajo_id):
        try:
            data = request.get_json()
            return jsonify(
                TrabajosRevistasReferatoService.update(trabajo_id, data)
            ), 200
        except Exception as e:
            return jsonify({"error": str(e)}), 400


    @staticmethod
    def delete(trabajo_id):
        try:
            return jsonify(
                TrabajosRevistasReferatoService.delete(trabajo_id)
            ), 200
        except Exception as e:
            return jsonify({"error": str(e)}), 400
