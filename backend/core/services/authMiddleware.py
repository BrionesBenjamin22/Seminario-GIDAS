from functools import wraps
from flask import request, jsonify
from core.services.auth_service import AuthService

def require_role(*roles_permitidos):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            auth_header = request.headers.get("Authorization")
            if not auth_header:
                return jsonify({"error": "Token requerido"}), 401

            token = auth_header.split(" ")[1]

            try:
                payload = AuthService.verify_token(token)
                rol_usuario = payload.get("rol")

                if rol_usuario not in roles_permitidos:
                    return jsonify({"error": "No autorizado"}), 403

                return func(*args, **kwargs)

            except Exception as e:
                return jsonify({"error": str(e)}), 401

        return wrapper
    return decorator
