from flask import Request, Response, jsonify
from core.services.investigador_service import (
    crear_investigador,
    actualizar_investigador,
    eliminar_investigador,
    listar_investigadores,
    obtener_investigador_por_id
)


class InvestigadorController:

    @staticmethod
    def crear(req: Request) -> Response:
        data = req.get_json()
        try:
            investigador = crear_investigador(data)
            return jsonify(investigador.serialize()), 201
        except ValueError as ve:
            return jsonify({"error": str(ve)}), 400
        except Exception:
            return jsonify({"error": "Error interno del servidor"}), 500

    @staticmethod
    def listar(req: Request) -> Response:
        try:
            activos = req.args.get("activos")  # true | false | all | None
            investigadores = listar_investigadores(activos)
            return jsonify([i.serialize() for i in investigadores]), 200
        except ValueError as ve:
            return jsonify({"error": str(ve)}), 400
        except Exception:
            return jsonify({"error": "Error interno del servidor"}), 500

    @staticmethod
    def obtener_por_id(req: Request, id: int) -> Response:
        try:
            investigador = obtener_investigador_por_id(id)
            return jsonify(investigador.serialize()), 200
        except ValueError as ve:
            return jsonify({"error": str(ve)}), 404
        except Exception:
            return jsonify({"error": "Error interno del servidor"}), 500

    @staticmethod
    def actualizar(req: Request, id: int) -> Response:
        data = req.get_json()
        try:
            investigador = actualizar_investigador(id, data)
            return jsonify(investigador.serialize()), 200
        except ValueError as ve:
            return jsonify({"error": str(ve)}), 400
        except Exception:
            return jsonify({"error": "Error interno del servidor"}), 500

    @staticmethod
    def eliminar(req: Request, id: int) -> Response:
        try:
            eliminar_investigador(id)
            return jsonify({"message": "Investigador dado de baja correctamente"}), 200
        except ValueError as ve:
            return jsonify({"error": str(ve)}), 400
        except Exception:
            return jsonify({"error": "Error interno del servidor"}), 500
