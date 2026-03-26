from flask import Request, Response, jsonify
from core.services.dashboard_general_service import DashboardGeneralService


class DashboardGeneralController:

    @staticmethod
    def obtener(req: Request) -> Response:
        try:
            data = DashboardGeneralService.get_resumen()
            return jsonify(data), 200

        except ValueError as ve:
            return jsonify({"error": str(ve)}), 400

        except Exception as e:
            import traceback
            traceback.print_exc()
            return jsonify({
                "error": "Error interno del servidor",
                "detail": str(e)
            }), 500