from flask import Request, Response, jsonify
from core.services.grupo_service import (
    obtener_grupo_utn,
    actualizar_grupo_utn
)


class GrupoUtnController:

    # -------------------------
    # Obtener grupo UTN
    # -------------------------
    @staticmethod
    def obtener(req: Request) -> Response:
        try:
            grupo = obtener_grupo_utn()
            return jsonify(grupo.serialize()), 200
        except Exception:
            return jsonify({"error": "Error interno del servidor"}), 500

    # -------------------------
    # Actualizar grupo UTN
    # -------------------------
    @staticmethod
    def actualizar(req: Request) -> Response:
        data = req.get_json()

        try:
            grupo = actualizar_grupo_utn(data)
            return jsonify(grupo.serialize()), 200
        except ValueError as ve:
            return jsonify({"error": str(ve)}), 400
        except Exception:
            return jsonify({"error": "Error interno del servidor"}), 500
