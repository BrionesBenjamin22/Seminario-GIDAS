from flask import Request, Response, jsonify
from core.models.usuario import Usuario
from core.services.auth_service import AuthService


class AuthController:

    @staticmethod
    def primer_usuario():
        """Verificar si existe al menos un usuario en el sistema"""
        try:
            existe = AuthService.existe_primer_usuario()
            return jsonify({"existe": existe}), 200
        except Exception as e:
            return jsonify({"error": str(e)}), 500

    @staticmethod
    def register(req: Request) -> Response:
        data = req.get_json()

        try:
            # Verificar si es el primer usuario
            es_primer_usuario = not AuthService.existe_primer_usuario()
            
            # Si ya existen usuarios, verificar que venga de un admin
            if not es_primer_usuario:
                auth_header = req.headers.get("Authorization")
                if not auth_header:
                    return jsonify({"error": "Token requerido. El sistema ya tiene usuarios registrados."}), 403
                
                token = auth_header.split(" ")[1]
                payload = AuthService.verify_token(token)
                if payload.get("rol") != "ADMIN":
                    return jsonify({"error": "Acceso denegado. Se requiere rol de administrador."}), 403
            
            user = AuthService.register(
                nombre_usuario=data["nombre_usuario"],
                mail=data["mail"],
                password=data["password"],
                rol_id=data.get("rol_id"),
                nombre_apellido=data.get("nombre_apellido"),
                dni=data.get("dni"),
                es_primer_usuario=es_primer_usuario
            )

            # Generar tokens para el nuevo usuario
            tokens = AuthService.generate_tokens(user)

            return jsonify({
                "mensaje": "Usuario creado exitosamente",
                "usuario": {
                    "id": user.id,
                    "nombre_usuario": user.nombre_usuario,
                    "mail": user.mail,
                    "rol": user.rol.nombre,
                    "primer_login": user.primer_login
                },
                "access_token": tokens["access_token"],
                "refresh_token": tokens["refresh_token"]
            }), 201

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
                "refresh_token": result["refresh_token"],
                "user": result["user"]
            })

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
            if not user or not user.activo:
                return jsonify({"error": "Usuario no encontrado"}), 404

            return jsonify(user.serialize()), 200

        except Exception as e:
            return jsonify({"error": str(e)}), 401


    @staticmethod
    def refresh(req: Request) -> Response:

        refresh_token = req.cookies.get("refresh_token")
        
        # También permitir refresh token en el body o header
        if not refresh_token:
            data = req.get_json()
            if data and data.get("refresh_token"):
                refresh_token = data["refresh_token"]

        if not refresh_token:
            return jsonify({"error": "Refresh token requerido"}), 401

        try:
            new_access_token = AuthService.refresh_access_token(refresh_token)
            return jsonify({"access_token": new_access_token}), 200

        except Exception as e:
            return jsonify({"error": str(e)}), 401


    @staticmethod
    def recover_password(req: Request) -> Response:
        data = req.get_json() or {}
        mail_usuario = data.get("mail")

        if not mail_usuario:
            return jsonify({"error": "mail es requerido"}), 400

        try:
            resultado = AuthService.recover_password_by_mail(mail_usuario)
            return jsonify(resultado), 200
        except Exception as e:
            return jsonify({"error": str(e)}), 400


    @staticmethod
    def reset_password(req: Request) -> Response:
        data = req.get_json() or {}
        token = data.get("token")
        password_nueva = data.get("password_nueva")
        password_confirmacion = data.get("password_confirmacion")

        if not token:
            return jsonify({"error": "token es requerido"}), 400

        if not password_nueva or not password_confirmacion:
            return jsonify({"error": "password_nueva y password_confirmacion son requeridos"}), 400

        if password_nueva != password_confirmacion:
            return jsonify({"error": "La nueva contraseña y la confirmación no coinciden"}), 400

        if len(password_nueva) < 6:
            return jsonify({"error": "La contraseña debe tener al menos 6 caracteres"}), 400

        try:
            AuthService.reset_password_with_token(token, password_nueva)
            return jsonify({"mensaje": "Contraseña restablecida exitosamente"}), 200
        except Exception as e:
            return jsonify({"error": str(e)}), 400


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
            password_confirmacion = data.get("password_confirmacion")
            
            # Validar que venga confirmación
            if not password_nueva or not password_confirmacion:
                return jsonify({"error": "password_nueva y password_confirmacion son requeridos"}), 400
            
            # Validar que coincidan
            if password_nueva != password_confirmacion:
                return jsonify({"error": "La nueva contraseña y la confirmación no coinciden"}), 400
            
            # Validar longitud mínima
            if len(password_nueva) < 6:
                return jsonify({"error": "La contraseña debe tener al menos 6 caracteres"}), 400

            # Verificar si es el primer cambio
            user = Usuario.query.get(user_id)
            es_primer_cambio = user.primer_login if user else False
            
            # Si no es primer cambio, requerir password_actual
            if not es_primer_cambio and not password_actual:
                return jsonify({"error": "password_actual es requerido"}), 400

            AuthService.change_password(
                user_id=user_id,
                password_actual=password_actual,
                password_nueva=password_nueva,
                es_primer_cambio=es_primer_cambio
            )

            return jsonify({"mensaje": "Contraseña actualizada exitosamente"}), 200

        except Exception as e:
            return jsonify({"error": str(e)}), 400


    @staticmethod
    def delete_user(req: Request, user_id: int):

        auth_header = req.headers.get("Authorization")
        if not auth_header:
            return jsonify({"error": "Token requerido"}), 401

        token = auth_header.split(" ")[1]

        try:
            payload = AuthService.verify_token(token)
            current_user_id = int(payload["sub"])

            AuthService.delete_user(
                user_id=user_id,
                current_user_id=current_user_id
            )

            return jsonify({"mensaje": "Usuario eliminado exitosamente"}), 200

        except Exception as e:
            return jsonify({"error": str(e)}), 400

    # -------------------------
    # CRUD Usuarios
    # -------------------------
    
    @staticmethod
    def get_all_users(req: Request):
        """Obtener todos los usuarios"""
        auth_header = req.headers.get("Authorization")
        if not auth_header:
            return jsonify({"error": "Token requerido"}), 401

        token = auth_header.split(" ")[1]

        try:
            payload = AuthService.verify_token(token)
            if payload.get("rol") != "ADMIN":
                return jsonify({"error": "Acceso denegado. Se requiere rol de administrador."}), 403

            users = AuthService.get_all_users()
            return jsonify([user.serialize() for user in users]), 200

        except Exception as e:
            return jsonify({"error": str(e)}), 400
    
    @staticmethod
    def get_user_by_id(req: Request, user_id: int):
        """Obtener un usuario por ID"""
        auth_header = req.headers.get("Authorization")
        if not auth_header:
            return jsonify({"error": "Token requerido"}), 401

        token = auth_header.split(" ")[1]

        try:
            payload = AuthService.verify_token(token)
            # Permitir que un usuario vea su propio perfil o un admin vea cualquiera
            if payload.get("rol") != "ADMIN" and int(payload["sub"]) != user_id:
                return jsonify({"error": "Acceso denegado. Se requiere rol de administrador."}), 403

            user = AuthService.get_user_by_id(user_id)
            return jsonify(user.serialize()), 200

        except Exception as e:
            return jsonify({"error": str(e)}), 404
    
    @staticmethod
    def update_user(req: Request, user_id: int):
        """Actualizar un usuario"""
        auth_header = req.headers.get("Authorization")
        if not auth_header:
            return jsonify({"error": "Token requerido"}), 401

        token = auth_header.split(" ")[1]

        try:
            payload = AuthService.verify_token(token)
            current_user_id = int(payload["sub"])
            
            # Solo admin puede actualizar otros usuarios
            if payload.get("rol") != "ADMIN" and current_user_id != user_id:
                return jsonify({"error": "Acceso denegado. Se requiere rol de administrador."}), 403
            
            # Si no es admin, solo puede actualizar ciertos campos de sí mismo
            if payload.get("rol") != "ADMIN":
                data = req.get_json()
                # No-admin no puede cambiar rol ni activo
                if "rol" in data or "activo" in data:
                    return jsonify({"error": "No tiene permisos para cambiar rol o estado activo"}), 403

            data = req.get_json()
            user = AuthService.update_user(user_id, data, current_user_id)
            
            return jsonify({
                "mensaje": "Usuario actualizado exitosamente",
                "usuario": user.serialize()
            }), 200

        except Exception as e:
            return jsonify({"error": str(e)}), 400
    
    @staticmethod
    def create_user(req: Request):
        """Crear un nuevo usuario (solo admin)"""
        auth_header = req.headers.get("Authorization")
        if not auth_header:
            return jsonify({"error": "Token requerido"}), 401

        token = auth_header.split(" ")[1]

        try:
            payload = AuthService.verify_token(token)
            if payload.get("rol") != "ADMIN":
                return jsonify({"error": "Acceso denegado. Se requiere rol de administrador."}), 403

            data = req.get_json()
            
            # Validaciones
            if not data.get("nombre_usuario") or not data.get("mail") or not data.get("password"):
                return jsonify({"error": "nombre_usuario, mail y password son requeridos"}), 400
            
            if not data.get("rol"):
                return jsonify({"error": "rol es requerido"}), 400
            
            if data.get("rol") not in ["ADMIN", "GESTOR"]:
                return jsonify({"error": "rol solo puede ser ADMIN o GESTOR"}), 400
            
            if len(data.get("password", "")) < 6:
                return jsonify({"error": "La contraseña debe tener al menos 6 caracteres"}), 400
            
            # Obtener rol_id
            rol = AuthService.get_rol_by_name(data["rol"])
            if not rol:
                return jsonify({"error": "Rol no encontrado"}), 400
            
            user = AuthService.register(
                nombre_usuario=data["nombre_usuario"],
                mail=data["mail"],
                password=data["password"],
                rol_id=rol.id,
                nombre_apellido=data.get("nombre_apellido", data["nombre_usuario"]),
                dni=data.get("dni", 0),
                es_primer_usuario=False
            )
            
            return jsonify({
                "mensaje": "Usuario creado exitosamente",
                "usuario": user.serialize()
            }), 201

        except Exception as e:
            return jsonify({"error": str(e)}), 400
