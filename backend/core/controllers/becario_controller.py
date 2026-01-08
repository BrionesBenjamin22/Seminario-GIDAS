from flask import Request, Response, jsonify
from core.services.becario_service import (
    crear_becario,
    actualizar_becario,
    eliminar_becario,
    listar_becarios,
    obtener_becario_por_id
)


class BecarioController:

    @staticmethod
    def crear(req: Request) -> Response:
        data = req.get_json()
        try:
            becario = crear_becario(data)
            return jsonify(becario.serialize()), 201
        except ValueError as ve:
            return jsonify({"error": str(ve)}), 400
        except Exception:
            return jsonify({"error": "Error interno del servidor"}), 500

    @staticmethod
    def listar(req: Request) -> Response:
        try:
            becarios = listar_becarios()
            return jsonify([b.serialize() for b in becarios]), 200
        except Exception:
            return jsonify({"error": "Error interno del servidor"}), 500

    @staticmethod
    def obtener_por_id(req: Request, id: int) -> Response:
        try:
            becario = obtener_becario_por_id(id)
            return jsonify(becario.serialize()), 200
        except ValueError as ve:
            return jsonify({"error": str(ve)}), 404
        except Exception:
            return jsonify({"error": "Error interno del servidor"}), 500

    @staticmethod
    def actualizar(req: Request, id: int) -> Response:
        data = req.get_json()
        try:
            becario = actualizar_becario(id, data)
            return jsonify(becario.serialize()), 200
        except ValueError as ve:
            return jsonify({"error": str(ve)}), 400
        except Exception:
            return jsonify({"error": "Error interno del servidor"}), 500

    @staticmethod
    def eliminar(req, id):
        try:
            eliminar_becario(id)
            return jsonify({"message": "Becario eliminado correctamente"}), 200
        except ValueError as ve:
            return jsonify({"error": str(ve)}), 400
        except Exception:
            return jsonify({"error": "Error interno del servidor"}), 500
