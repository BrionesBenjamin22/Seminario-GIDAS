from flask import Request, Response, jsonify
from core.models.usuario import Usuario
from core.services.auth_service import AuthService


class AuthController:

    @staticmethod
    def register(req: Request) -> Response:
        data = req.get_json()

        try:
            user = AuthService.register(
                nombre_usuario=data["nombre_usuario"],
                mail=data["mail"],
                password=data["password"]
            )
            return jsonify(user.serialize()), 201

        except Exception as e:
            return jsonify({"error": str(e)}), 400

    @staticmethod
    def login(req: Request) -> Response:
        data = req.get_json()

        try:
            result = AuthService.login(
                nombre_usuario=data["nombre_usuario"],
                password=data["password"]
            )

            response = jsonify({
                "access_token": result["access_token"],
                "user": result["user"]
            })

            response.set_cookie(
                "refresh_token",
                result["refresh_token"],
                httponly=True,
                secure=False,       
                samesite="Lax",
                max_age=7 * 24 * 60 * 60
            )

            return response, 200

        except Exception as e:
            return jsonify({"error": str(e)}), 401

    @staticmethod
    def perfil(req: Request):
        auth_header = req.headers.get("Authorization")
        if not auth_header:
            return jsonify({"error": "Token requerido"}), 401

        token = auth_header.split(" ")[1]

        try:
            payload = AuthService.verify_token(token)
            user_id = int(payload["sub"])

            user = Usuario.query.get(user_id)
            if not user:
                return jsonify({"error": "Usuario no encontrado"}), 404

            return jsonify(user.serialize()), 200

        except Exception as e:
            return jsonify({"error": str(e)}), 401
        
        
    @staticmethod
    def refresh(req: Request) -> Response:
        refresh_token = req.cookies.get("refresh_token")

        if not refresh_token:
            return jsonify({"error": "Refresh token requerido"}), 401

        try:
            new_access_token = AuthService.refresh_access_token(refresh_token)
            return jsonify({"access_token": new_access_token}), 200
        except Exception as e:
            return jsonify({"error": str(e)}), 401

    @staticmethod
    def change_password(req: Request) -> Response:
        auth_header = req.headers.get("Authorization")

        if not auth_header:
            return jsonify({"error": "Token requerido"}), 401

        token = auth_header.split(" ")[1]

        try:
            payload = AuthService.verify_token(token)
            user_id = int(payload["sub"])

            data = req.get_json()
            password_actual = data.get("password_actual")
            password_nueva = data.get("password_nueva")

            if not password_actual or not password_nueva:
                return jsonify({"error": "Datos incompletos"}), 400

            AuthService.change_password(
                user_id=user_id,
                password_actual=password_actual,
                password_nueva=password_nueva
            )

            return jsonify({"message": "Contraseña cambiada correctamente"}), 200

        except Exception as e:
            return jsonify({"error": str(e)}), 400