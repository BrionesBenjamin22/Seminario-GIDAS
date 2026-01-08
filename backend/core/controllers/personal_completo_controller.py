from flask import jsonify
from core.services.personal_completo_service import listar_personal_completo


class PersonalCompletoController:

    @staticmethod
    def listar():
        try:
            data = listar_personal_completo()
            return jsonify(data), 200
        except Exception:
            return jsonify({"error": "Error interno del servidor"}), 500
