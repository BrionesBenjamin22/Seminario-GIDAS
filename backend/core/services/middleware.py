from functools import wraps
from flask import request, jsonify, g
from core.services.auth_service import AuthService


def requiere_rol(*roles_permitidos):

    roles_permitidos = [r.upper() for r in roles_permitidos]

    def decorator(func):

        @wraps(func)
        def wrapper(*args, **kwargs):

            auth_header = request.headers.get("Authorization")

            if not auth_header:
                return jsonify({"error": "Token requerido"}), 401

            try:
                
                parts = auth_header.split(" ")

                if len(parts) != 2 or parts[0].lower() != "bearer":
                    return jsonify({"error": "Formato de token inválido"}), 401

                token = parts[1]

                payload = AuthService.verify_token(token)

                # Guardamos usuario actual en el contexto global
                g.current_user_id = int(payload["sub"])
                g.current_user_rol = payload.get("rol")

                if not g.current_user_rol:
                    return jsonify({"error": "Rol no presente en token"}), 403

                if g.current_user_rol.upper() not in roles_permitidos:
                    return jsonify({
                        "error": "No tiene permisos suficientes"
                    }), 403

                return func(*args, **kwargs)

            except Exception as e:
                return jsonify({"error": str(e)}), 401

        return wrapper

    return decorator