from flask import Request, Response, jsonify
from core.services.grupo_service import (
    crear_grupo_utn,
    obtener_grupo_utn,
    actualizar_grupo_utn,
    eliminar_grupo_utn
)


class GrupoUtnController:
    # -------------------------
    # Crear grupo UTN
    # -------------------------
    @staticmethod
    def crear(req: Request) -> Response:
        data = req.get_json()
        try:
            grupo = crear_grupo_utn(data)
            return jsonify(grupo.serialize()), 201
        except ValueError as ve:
            return jsonify({"error": str(ve)}), 400
        except Exception as e:
            # En modo DEBUG, puede ser útil devolver el error real
            # For production, a generic message is better.
            return jsonify({"error": "Error interno del servidor", "detail": str(e)}), 500

    # -------------------------
    # Obtener grupo UTN
    # -------------------------
    @staticmethod
    def obtener(req: Request) -> Response:
        try:
            grupo = obtener_grupo_utn()
            if not grupo:
                return jsonify({"error": "No se ha configurado un grupo de investigación."}), 404
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
            
    # -------------------------
    # Eliminar grupo UTN
    # -------------------------
    @staticmethod
    def eliminar(req: Request) -> Response:
        try:
            eliminar_grupo_utn()
            return jsonify({"message": "Grupo de investigación eliminado correctamente"}), 200
        except ValueError as ve:
            return jsonify({"error": str(ve)}), 404
        except Exception as e:
            return jsonify({"error": "Error interno del servidor", "detail": str(e)}), 500
