from flask import jsonify, request, Response, Request
from core.services.grupo_service import (
    crear_grupo_utn,
    obtener_grupo_utn,
    actualizar_grupo_utn,
    eliminar_grupo_utn
)

class GrupoUtnController:

    @staticmethod
    def crear():
        data = request.get_json()
        try:
            grupo = crear_grupo_utn(data)
            return jsonify(grupo.serialize()), 201
        except ValueError as ve:
            return jsonify({"error": str(ve)}), 400
        except Exception as e:
            print(e)
            return jsonify({"error": "Error interno", "detail": str(e)}), 500

    @staticmethod
    def obtener() -> Response:
        try:
            grupo = obtener_grupo_utn()
            if not grupo:
                return jsonify({"error": "No se ha configurado un grupo de investigación."}), 404
            return jsonify(grupo.serialize()), 200
        except Exception as e:
            print("ERROR REAL:", e)   # 👈 CLAVE
            return jsonify({"error": str(e)}), 500


    @staticmethod
    def actualizar():
        data = request.get_json()
        try:
            grupo = actualizar_grupo_utn(data)
            return jsonify(grupo.serialize()), 200
        except ValueError as ve:
            return jsonify({"error": str(ve)}), 400
        except Exception as e:
            print(e)
            return jsonify({"error": "Error interno", "detail": str(e)}), 500

    @staticmethod
    def eliminar():
        try:
            eliminar_grupo_utn()
            return jsonify({"message": "Grupo eliminado correctamente"}), 200
        except ValueError as ve:
            return jsonify({"error": str(ve)}), 404
        except Exception as e:
            print(e)
            return jsonify({"error": "Error interno", "detail": str(e)}), 500
