from flask import jsonify, request
from core.services.proyecto_investigacion_service import ProyectoInvestigacionService


class ProyectoInvestigacionController:

    # =========================
    # GET ALL
    # =========================
    @staticmethod
    def get_all():
        try:
            filters = request.args.to_dict()
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
    def cerrar(proyecto_id):
        try:
            return jsonify(
                ProyectoInvestigacionService.cerrar_proyecto(proyecto_id)
            ), 200
        except Exception as e:
            return jsonify({"error": str(e)}), 400

    # =========================
    # VINCULAR / DESVINCULAR BECARIOS
    # =========================
    @staticmethod
    def vincular_becarios(proyecto_id):
        try:
            participaciones = request.get_json()

            if not participaciones:
                return jsonify({"error": "El body es obligatorio"}), 400

            return jsonify(
                ProyectoInvestigacionService.vincular_becarios_a_proyecto(
                    proyecto_id,
                    participaciones
                )
            ), 200

        except Exception as e:
            return jsonify({"error": str(e)}), 400


    @staticmethod
    def desvincular_becarios(proyecto_id):
        try:
            participaciones = request.get_json()

            if not participaciones:
                return jsonify({"error": "El body es obligatorio"}), 400

            return jsonify(
                ProyectoInvestigacionService.desvincular_becarios_de_proyecto(
                    proyecto_id,
                    participaciones
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
            participaciones = request.get_json()

            if not participaciones:
                return jsonify({"error": "El body es obligatorio"}), 400

            return jsonify(
                ProyectoInvestigacionService.vincular_investigadores_a_proyecto(
                    proyecto_id,
                    participaciones
                )
            ), 200

        except Exception as e:
            return jsonify({"error": str(e)}), 400


    @staticmethod
    def desvincular_investigadores(proyecto_id):
        try:
            participaciones = request.get_json()

            if not participaciones:
                return jsonify({"error": "El body es obligatorio"}), 400

            return jsonify(
                ProyectoInvestigacionService.desvincular_investigadores_de_proyecto(
                    proyecto_id,
                    participaciones
                )
            ), 200

        except Exception as e:
            return jsonify({"error": str(e)}), 400

