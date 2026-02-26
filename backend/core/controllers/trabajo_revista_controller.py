from flask import jsonify, request
from core.services.trabajo_revista_service import (
    TrabajosRevistasReferatoService
)

class TrabajosRevistasReferatoController:

    @staticmethod
    def get_all():
        try:
            args = request.args
            filters = {}

            # -------------------------
            # Filtros directos
            # -------------------------
            if args.get("proyecto_id"):
                filters["proyecto_id"] = int(args.get("proyecto_id"))

            if args.get("grupo_utn_id"):
                filters["grupo_utn_id"] = int(args.get("grupo_utn_id"))

            # -------------------------
            # Filtros semánticos
            # -------------------------
            if args.get("pais"):
                filters["pais"] = args.get("pais")

            if args.get("editorial"):
                filters["editorial"] = args.get("editorial")

            # -------------------------
            # Orden
            # -------------------------
            if args.get("orden") in ("asc", "desc"):
                filters["orden"] = args.get("orden")

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

    @staticmethod
    def add_investigadores(trabajo_id):
        try:
            data = request.get_json()

            if not data:
                return jsonify({"error": "Body requerido"}), 400
            
            investigadores_ids = data.get("investigadores_ids")
            if not investigadores_ids or not isinstance(investigadores_ids, list):
                return jsonify({"error": "investigadores_ids debe ser una lista no vacía"}), 400

            result = TrabajosRevistasReferatoService.vincular_investigadores(trabajo_id, investigadores_ids)
            return jsonify(result), 200
        
        except ValueError as e:
            return jsonify({"error": str(e)}), 400
        
    @staticmethod
    def remove_investigadores(trabajo_id):
        try:
            data = request.get_json()

            if not data:
                return jsonify({"error": "Body requerido"}), 400
            
            investigadores_ids = data.get("investigadores_ids")
            if not investigadores_ids or not isinstance(investigadores_ids, list):
                return jsonify({"error": "investigadores_ids debe ser una lista no vacía"}), 400
            
            result = TrabajosRevistasReferatoService.desvincular_investigadores(trabajo_id, investigadores_ids)
            
            return jsonify(result), 200
           

        except Exception as e:
            return jsonify({"error": str(e)}), 400