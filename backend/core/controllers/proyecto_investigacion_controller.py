from flask import jsonify, request
from core.services.proyecto_investigacion_service import ProyectoInvestigacionService


class ProyectoInvestigacionController:

    # =========================
    # GET ALL
    # =========================
    @staticmethod
    def get_all():
        try:
            args = request.args
            filters = {}

            # -------------------------
            # Filtros directos
            # -------------------------
            if args.get("tipo_proyecto_id"):
                filters["tipo_proyecto_id"] = int(args.get("tipo_proyecto_id"))

            if args.get("grupo_utn_id"):
                filters["grupo_utn_id"] = int(args.get("grupo_utn_id"))

            # -------------------------
            # Filtros semánticos
            # -------------------------
            if args.get("filtro") == "distinciones":
                filters["tiene_distinciones"] = True

            # -------------------------
            # Orden
            # -------------------------
            if args.get("orden") in ("asc", "desc"):
                filters["orden"] = args.get("orden")

            return jsonify(
                ProyectoInvestigacionService.get_all(filters)
            ), 200

        except Exception as e:
            return jsonify({"error": str(e)}), 400


    # =========================
    # GET BY ID
    # =========================
    @staticmethod
    def get_by_id(proyecto_id):
        try:
            return jsonify(
                ProyectoInvestigacionService.get_by_id(proyecto_id)
            ), 200
        except Exception as e:
            return jsonify({"error": str(e)}), 404

    # =========================
    # CREATE
    # =========================
    @staticmethod
    def create():
        try:
            data = request.get_json()
            if not data:
                return jsonify({"error": "El body es obligatorio"}), 400

            return jsonify(
                ProyectoInvestigacionService.create(data)
            ), 201
        except Exception as e:
            return jsonify({"error": str(e)}), 400

    # =========================
    # UPDATE
    # =========================
    @staticmethod
    def update(proyecto_id):
        try:
            data = request.get_json()
            if not data:
                return jsonify({"error": "El body es obligatorio"}), 400

            return jsonify(
                ProyectoInvestigacionService.update(proyecto_id, data)
            ), 200
        except Exception as e:
            return jsonify({"error": str(e)}), 400

    # =========================
    # DELETE
    # =========================
    @staticmethod
    def delete(proyecto_id):
        try:
            return jsonify(
                ProyectoInvestigacionService.delete(proyecto_id)
            ), 200
        except Exception as e:
            return jsonify({"error": str(e)}), 400

    # =========================
    # VINCULAR / DESVINCULAR BECARIOS
    # =========================
    @staticmethod
    def vincular_becarios(proyecto_id):
        try:
            data = request.get_json()
            becarios_ids = data.get("becarios_ids") if data else None

            return jsonify(
                ProyectoInvestigacionService.vincular_becarios_a_proyecto(
                    proyecto_id, becarios_ids
                )
            ), 200
        except Exception as e:
            return jsonify({"error": str(e)}), 400

    @staticmethod
    def desvincular_becarios(proyecto_id):
        try:
            data = request.get_json()
            becarios_ids = data.get("becarios_ids") if data else None

            return jsonify(
                ProyectoInvestigacionService.desvincular_becarios_de_proyecto(
                    proyecto_id, becarios_ids
                )
            ), 200
        except Exception as e:
            return jsonify({"error": str(e)}), 400

    # =========================
    # VINCULAR / DESVINCULAR INVESTIGADORES
    # =========================
    @staticmethod
    def vincular_investigadores(proyecto_id):
        try:
            data = request.get_json()
            investigadores_ids = data.get("investigadores_ids") if data else None

            return jsonify(
                ProyectoInvestigacionService.vincular_investigadores_a_proyecto(
                    proyecto_id, investigadores_ids
                )
            ), 200
        except Exception as e:
            return jsonify({"error": str(e)}), 400

    @staticmethod
    def desvincular_investigadores(proyecto_id):
        try:
            data = request.get_json()
            investigadores_ids = data.get("investigadores_ids") if data else None

            return jsonify(
                ProyectoInvestigacionService.desvincular_investigadores_de_proyecto(
                    proyecto_id, investigadores_ids
                )
            ), 200
        except Exception as e:
            return jsonify({"error": str(e)}), 400
