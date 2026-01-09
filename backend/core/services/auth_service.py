import jwt
import datetime
from core.models.usuario import Usuario
from extension import db
from config import Config


class AuthService:

    @staticmethod
    def generate_tokens(user: Usuario) -> dict:
        access_payload = {
            "sub": str(user.id),
            "nombre_usuario": user.nombre_usuario,
            "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=15),
            "iss": "auth-service"
        }

        refresh_payload = {
            "sub": str(user.id),
            "exp": datetime.datetime.utcnow() + datetime.timedelta(days=7),
            "iss": "auth-service"
        }

        access_token = jwt.encode(
            access_payload,
            Config.JWT_SECRET,
            algorithm=Config.JWT_ALGORITHM
        )

        refresh_token = jwt.encode(
            refresh_payload,
            Config.REFRESH_SECRET,
            algorithm=Config.JWT_ALGORITHM
        )

        return {
            "access_token": access_token,
            "refresh_token": refresh_token
        }

    # -------------------------
    # Login
    # -------------------------
    @staticmethod
    def login(nombre_usuario: str, password: str) -> dict:
        user = Usuario.query.filter_by(nombre_usuario=nombre_usuario).first()

        if not user or not user.verificar_password(password):
            raise Exception("Credenciales inválidas")

        tokens = AuthService.generate_tokens(user)

        return {
            "access_token": tokens["access_token"],
            "refresh_token": tokens["refresh_token"],
            "user": {
                "id": user.id,
                "nombre_usuario": user.nombre_usuario,
                "mail": user.mail
            }
        }

    # -------------------------
    # Registro
    # -------------------------
    @staticmethod
    def register(nombre_usuario: str, mail: str, password: str) -> Usuario:
        existe = Usuario.query.filter(
            (Usuario.nombre_usuario == nombre_usuario) |
            (Usuario.mail == mail)
        ).first()

        if existe:
            raise Exception("Usuario o mail ya existe")

        nuevo_usuario = Usuario(
            nombre_usuario=nombre_usuario,
            mail=mail
        )

        nuevo_usuario.set_password(password)

        db.session.add(nuevo_usuario)
        try:
            db.session.commit()
            return nuevo_usuario
        except Exception:
            db.session.rollback()
            raise Exception("Error al registrar usuario")

    # -------------------------
    # Refresh token
    # -------------------------
    @staticmethod
    def refresh_access_token(refresh_token: str) -> str:
        try:
            payload = jwt.decode(
                refresh_token,
                Config.REFRESH_SECRET,
                algorithms=[Config.JWT_ALGORITHM]
            )

            user_id = int(payload["sub"])
            user = Usuario.query.get(user_id)

            if not user:
                raise Exception("Usuario no encontrado")

            new_access_payload = {
                "sub": str(user.id),
                "nombre_usuario": user.nombre_usuario,
                "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=15),
                "iss": "auth-service"
            }

            return jwt.encode(
                new_access_payload,
                Config.JWT_SECRET,
                algorithm=Config.JWT_ALGORITHM
            )

        except jwt.ExpiredSignatureError:
            raise Exception("Refresh token expirado")
        except jwt.InvalidTokenError:
            raise Exception("Refresh token inválido")

    # -------------------------
    # Verificar token
    # -------------------------
    @staticmethod
    def verify_token(token: str) -> dict:
        try:
            return jwt.decode(
                token,
                Config.JWT_SECRET,
                algorithms=[Config.JWT_ALGORITHM]
            )
        except jwt.ExpiredSignatureError:
            raise Exception("Token expirado")
        except jwt.InvalidTokenError:
            raise Exception("Token inválido")

    # -------------------------
    # Cambiar contraseña    
    # -------------------------
        
    @staticmethod
    def change_password(user_id: int, password_actual: str, password_nueva: str):
        user = Usuario.query.get(user_id)

        if not user:
            raise Exception("Usuario no encontrado")

        user.cambiar_password(password_actual, password_nueva)

        try:
            db.session.commit()
        except Exception:
            db.session.rollback()
            raise Exception("Error al cambiar la contraseña")