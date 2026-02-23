from flask import Request, Response, jsonify
from core.services.articulo_divulgacion_service import ArticuloDivulgacionService


class ArticuloDivulgacionController:

    @staticmethod
    def crear(req: Request) -> Response:
        data = req.get_json(force=True, silent=False)

        try:
            articulo = ArticuloDivulgacionService.create(data)
            return jsonify(articulo), 201

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
            filters = {
                "grupo_utn_id": req.args.get("grupo_utn_id", type=int),
                "orden": req.args.get("orden")
            }

            articulos = ArticuloDivulgacionService.get_all(filters)
            return jsonify(articulos), 200

        except ValueError as ve:
            return jsonify({"error": str(ve)}), 400

        except Exception:
            return jsonify({"error": "Error interno del servidor"}), 500

    @staticmethod
    def obtener_por_id(req: Request, articulo_id: int) -> Response:
        try:
            articulo = ArticuloDivulgacionService.get_by_id(articulo_id)
            return jsonify(articulo), 200

        except ValueError as ve:
            return jsonify({"error": str(ve)}), 404

        except Exception:
            return jsonify({"error": "Error interno del servidor"}), 500

    @staticmethod
    def actualizar(req: Request, articulo_id: int) -> Response:
        data = req.get_json(force=True, silent=False)

        try:
            articulo = ArticuloDivulgacionService.update(articulo_id, data)
            return jsonify(articulo), 200

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
    def eliminar(req: Request, articulo_id: int) -> Response:
        try:
            result = ArticuloDivulgacionService.delete(articulo_id)
            return jsonify(result), 200

        except ValueError as ve:
            return jsonify({"error": str(ve)}), 400

        except Exception:
            return jsonify({"error": "Error interno del servidor"}), 500