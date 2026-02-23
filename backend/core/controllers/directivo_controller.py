from flask import jsonify, request
from core.services.directivo_service import DirectivoGrupoService


class DirectivoController:

    # ==========================================
    # CREAR DIRECTIVO
    # ==========================================
    @staticmethod
    def create():
        try:
            data = request.get_json()

            if not data:
                return jsonify({"error": "Body requerido"}), 400

            result = DirectivoGrupoService.crear_directivo(data)

            return jsonify(result), 201

        except ValueError as ve:
            return jsonify({"error": str(ve)}), 400

        except Exception as e:
            return jsonify({"error": str(e)}), 500


    @staticmethod
    def get_all():
        try:
            result = DirectivoGrupoService.get_all_srv()
            return jsonify(result), 200

        except Exception as e:
            return jsonify({"error": str(e)}), 500

    # ==========================================
    # UPDATE PARCIAL DIRECTIVO
    # ==========================================
    @staticmethod
    def update(directivo_id):
        try:
            data = request.get_json()

            if not data:
                return jsonify({"error": "Body requerido"}), 400

            result = DirectivoGrupoService.actualizar_directivo(
                directivo_id,
                data
            )

            return jsonify(result), 200

        except ValueError as e:
            return jsonify({"error": str(e)}), 400

        except Exception:
            return jsonify({"error": "Error interno del servidor"}), 500


    # ==========================================
    # ASIGNAR DIRECTIVO A GRUPO
    # ==========================================
    @staticmethod
    def asignar():
        try:
            data = request.get_json()

            if not data:
                return jsonify({"error": "Body requerido"}), 400

            result = DirectivoGrupoService.asignar_a_grupo(data)

            return jsonify(result), 201

        except ValueError as e:
            return jsonify({"error": str(e)}), 400

        except Exception as e:
            return jsonify({"error": f"Error interno del servidor: {str(e)}"}), 500


    # ==========================================
    # FINALIZAR CARGO
    # ==========================================
    @staticmethod
    def finalizar():
        try:
            data = request.get_json()

            if not data:
                return jsonify({"error": "Body requerido"}), 400

            result = DirectivoGrupoService.finalizar_cargo(data)

            return jsonify(result), 200

        except ValueError as e:
            return jsonify({"error": str(e)}), 400

        except Exception as e:
            return jsonify({"error": f"Error interno del servidor: {str(e)}"}), 500


    # ==========================================
    # OBTENER DIRECTIVOS POR GRUPO
    # ==========================================
    @staticmethod
    def get_por_grupo(grupo_id):
        try:
            result = DirectivoGrupoService.get_por_grupo(grupo_id)

            return jsonify(result), 200

        except ValueError as e:
            return jsonify({"error": str(e)}), 404

        except Exception:
            return jsonify({"error": "Error interno del servidor"}), 500

    @staticmethod
    def get_actuales(grupo_id):
        try:
            result = DirectivoGrupoService.get_actuales_por_grupo(grupo_id)
            return jsonify(result), 200

        except Exception:
            return jsonify({"error": "Error interno del servidor"}), 500