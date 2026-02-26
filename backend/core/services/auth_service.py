import jwt
import datetime
from core.models.persona import Persona
from core.models.usuario import Usuario, RolUsuario
from extension import db
from config import Config


class AuthService:

    @staticmethod
    def generate_tokens(user: Usuario) -> dict:
        access_payload = {
            "sub": str(user.id),
            "nombre_usuario": user.nombre_usuario,
            "rol": user.rol.nombre,   
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
    # Verificar si existe primer usuario
    # -------------------------
    @staticmethod
    def existe_primer_usuario() -> bool:
        """Verifica si existe al menos un usuario en el sistema"""
        return Usuario.query.first() is not None

    # -------------------------
    # Login
    # -------------------------
    @staticmethod
    def login(nombre_usuario: str, password: str) -> dict:

        user = Usuario.query.filter_by(
            nombre_usuario=nombre_usuario,
            activo=True   # importante para evitar login de usuarios eliminados
        ).first()

        if not user or not user.verificar_password(password):
            raise Exception("Credenciales inválidas")

        tokens = AuthService.generate_tokens(user)

        return {
            "access_token": tokens["access_token"],
            "refresh_token": tokens["refresh_token"],
            "user": {
                "id": user.id,
                "nombre_usuario": user.nombre_usuario,
                "mail": user.mail,
                "rol": user.rol.nombre,
                "primer_login": user.primer_login
            }
        }

    # -------------------------
    # Registro (primer usuario o por admin)
    # -------------------------
    @staticmethod
    def register(
        nombre_usuario: str,
        mail: str,
        password: str,
        rol_id: int = None,
        nombre_apellido: str = None,
        dni: int = None,
        es_primer_usuario: bool = False
    ) -> Usuario:

        existe = Usuario.query.filter(
            (Usuario.nombre_usuario == nombre_usuario) |
            (Usuario.mail == mail)
        ).first()

        if existe:
            raise Exception("Usuario o mail ya existe")

        # Si es el primer usuario, asignar rol ADMIN automáticamente
        if es_primer_usuario:
            rol = RolUsuario.query.filter_by(nombre="ADMIN").first()
            if not rol:
                raise Exception("Rol ADMIN no encontrado en el sistema")
        else:
            if not rol_id:
                raise Exception("rol_id es obligatorio para crear usuarios")
            rol = RolUsuario.query.get(rol_id)
            if not rol:
                raise Exception("Rol inválido")

        # Crear Persona solo si se proporcionan datos (opcional ahora)
        persona_id = None
        if nombre_apellido and dni:
            persona = Persona(
                nombre_apellido=nombre_apellido,
                dni=dni
            )
            db.session.add(persona)
            db.session.flush()  # importante para obtener persona.id
            persona_id = persona.id

        # Crear Usuario
        nuevo_usuario = Usuario(
            nombre_usuario=nombre_usuario,
            mail=mail,
            id_persona=persona_id,
            id_rol=rol.id,
            primer_login=True  # Siempre true al crear
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
    def change_password(user_id: int, password_actual: str, password_nueva: str, es_primer_cambio: bool = False):
        user = Usuario.query.get(user_id)

        if not user:
            raise Exception("Usuario no encontrado")

        # Si es el primer cambio, no validamos password_actual
        if not es_primer_cambio:
            if not user.verificar_password(password_actual):
                raise Exception("La contraseña actual es incorrecta")
        
        user.set_password(password_nueva)
        
        # Actualizar primer_login a False
        user.primer_login = False

        try:
            db.session.commit()
        except Exception:
            db.session.rollback()
            raise Exception("Error al cambiar la contraseña")
        
    
    
    @staticmethod
    def delete_user(user_id: int, current_user_id: int):

        user = Usuario.query.get(user_id)

        if not user:
            raise Exception("Usuario no encontrado")
        
        # Evitar que un admin se elimine a sí mismo
        if user_id == current_user_id:
            raise Exception("No puede eliminar su propia cuenta")
        
        # Verificar que quede al menos un admin
        if user.rol.nombre == "ADMIN":
            admin_count = Usuario.query.join(RolUsuario).filter(
                RolUsuario.nombre == "ADMIN",
                Usuario.activo == True
            ).count()
            if admin_count <= 1:
                raise Exception("Debe quedar al menos un administrador en el sistema")

        user.soft_delete(current_user_id)

        db.session.commit()

    # -------------------------
    # CRUD Usuarios
    # -------------------------
    
    @staticmethod
    def get_all_users():
        """Obtener todos los usuarios activos"""
        return Usuario.query.filter_by(activo=True).all()
    
    @staticmethod
    def get_user_by_id(user_id: int):
        """Obtener un usuario por ID"""
        user = Usuario.query.get(user_id)
        if not user:
            raise Exception("Usuario no encontrado")
        return user
    
    @staticmethod
    def update_user(user_id: int, data: dict, current_user_id: int):
        """Actualizar datos de un usuario"""
        user = Usuario.query.get(user_id)
        
        if not user:
            raise Exception("Usuario no encontrado")
        
        # Evitar que un admin se desactive a sí mismo
        if user_id == current_user_id and data.get("activo") == False:
            raise Exception("No puede desactivar su propia cuenta")
        
        # Verificar que quede al menos un admin si se desactiva un admin
        if user.rol.nombre == "ADMIN" and data.get("activo") == False:
            admin_count = Usuario.query.join(RolUsuario).filter(
                RolUsuario.nombre == "ADMIN",
                Usuario.activo == True
            ).count()
            if admin_count <= 1:
                raise Exception("Debe quedar al menos un administrador en el sistema")
        
        # Actualizar campos permitidos
        if "rol" in data:
            rol = RolUsuario.query.filter_by(nombre=data["rol"]).first()
            if not rol:
                raise Exception("Rol inválido")
            user.id_rol = rol.id
        
        if "mail" in data:
            # Verificar que el mail no exista
            existing = Usuario.query.filter(
                Usuario.mail == data["mail"],
                Usuario.id != user_id
            ).first()
            if existing:
                raise Exception("El mail ya está en uso")
            user.mail = data["mail"]
        
        if "activo" in data:
            user.activo = data["activo"]
        
        try:
            db.session.commit()
            return user
        except Exception:
            db.session.rollback()
            raise Exception("Error al actualizar usuario")

    @staticmethod
    def get_rol_by_name(nombre: str):
        """Obtener un rol por nombre"""
        return RolUsuario.query.filter_by(nombre=nombre).first()
