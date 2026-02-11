from flask import Request, Response, jsonify
from core.services.personal_service import (
    crear_personal,
    actualizar_personal,
    eliminar_personal,
    listar_personal,
    obtener_personal_por_id
)


class PersonalController:

    @staticmethod
    def crear(req: Request) -> Response:
        data = req.get_json(force=True, silent=False)
        print("DATA RECIBIDA:", data)

        try:
            personal = crear_personal(data)
            return jsonify(personal.serialize()), 201
        except ValueError as ve:
            return jsonify({"error": str(ve)}), 400
        except Exception as e:
            import traceback
            traceback.print_exc()
            return jsonify({
                "error": "Error interno del servidor",
                "detail": str(e)
            }), 500


    @staticmethod
    def listar(req: Request) -> Response:
        try:
            activos = req.args.get("activos")  # true | false | all | None
            personal = listar_personal(activos)
            return jsonify([p.serialize() for p in personal]), 200
        except ValueError as ve:
            return jsonify({"error": str(ve)}), 400
        except Exception:
            return jsonify({"error": "Error interno del servidor"}), 500

    @staticmethod
    def obtener_por_id(req: Request, id: int) -> Response:
        try:
            personal = obtener_personal_por_id(id)
            return jsonify(personal.serialize()), 200
        except ValueError as ve:
            return jsonify({"error": str(ve)}), 404
        except Exception:
            return jsonify({"error": "Error interno del servidor"}), 500

    @staticmethod
    def actualizar(req: Request, id: int) -> Response:
        data = req.get_json()
        try:
            personal = actualizar_personal(id, data)
            return jsonify(personal.serialize()), 200
        except ValueError as ve:
            return jsonify({"error": str(ve)}), 400
        except Exception:
            return jsonify({"error": "Error interno del servidor"}), 500

    @staticmethod
    def eliminar(req: Request, id: int) -> Response:
        try:
            eliminar_personal(id)
            return jsonify({"message": "Personal dado de baja correctamente"}), 200
        except ValueError as ve:
            return jsonify({"error": str(ve)}), 400
        except Exception:
            return jsonify({"error": "Error interno del servidor"}), 500
