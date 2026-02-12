from core.services.personal_completo_service import obtener_personal_por_tipo
from flask import Request, Response, jsonify
from core.services.personal_service import (
    crear_personal,
    actualizar_personal,
    eliminar_personal,
    listar_personal
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
    def obtener_por_id(req: Request, rol: str, id: int) -> Response:
        try:
            personal = obtener_personal_por_tipo(rol, id)
            if not personal:
                return jsonify({"error": "Personal no encontrado"}), 404
            return jsonify(personal), 200
        except ValueError as ve:
            return jsonify({"error": str(ve)}), 404
        except Exception:
            return jsonify({"error": "Error interno del servidor"}), 500

    @staticmethod
    def actualizar(req: Request, rol: str, id: int) -> Response:
        data = req.get_json()

        print("---- DEBUG ACTUALIZAR ----")
        print("ROL:", rol)
        print("ID:", id)
        print("DATA:", data)

        try:
            personal = actualizar_personal(id, data, rol)
            print("ACTUALIZACIÓN EXITOSA")
            return jsonify(personal.serialize()), 200

        except ValueError as ve:
            print("VALUE ERROR:", ve)
            return jsonify({"error": str(ve)}), 400

        except Exception as e:
            print("EXCEPTION:", e)
            raise e


    @staticmethod
    def eliminar(req: Request, rol: str, id: int) -> Response:
        try:
            eliminar_personal(id)
            return jsonify({"message": "Personal dado de baja correctamente"}), 200
        except ValueError as ve:
            return jsonify({"error": str(ve)}), 400
        except Exception:
            return jsonify({"error": "Error interno del servidor"}), 500
