from flask import Blueprint, request
from core.controllers.auth_controller import AuthController
from core.services.middleware import requiere_rol

auth_bp = Blueprint("auth", __name__, url_prefix="/auth")


# -------------------------
# Verificar primer usuario
# -------------------------
@auth_bp.route("/primer-usuario", methods=["GET"])
def primer_usuario():
    return AuthController.primer_usuario()


# -------------------------
# Registro (primer usuario o por admin)
# -------------------------
@auth_bp.route("/register", methods=["POST"])
def register():
    return AuthController.register(request)


# -------------------------
# Login
# -------------------------
@auth_bp.route("/login", methods=["POST"])
def login():
    return AuthController.login(request)


# -------------------------
# Perfil (requiere token)
# -------------------------
@auth_bp.route("/perfil", methods=["GET"])
def perfil():
    return AuthController.perfil(request)


# -------------------------
# Refresh token
# -------------------------
@auth_bp.route("/refresh", methods=["POST"])
def refresh():
    return AuthController.refresh(request)


# -------------------------
# Change password (POST según especificación del frontend)
# -------------------------
@auth_bp.route("/recuperar-password", methods=["POST"])
def recover_password():
    return AuthController.recover_password(request)


@auth_bp.route("/reset-password", methods=["POST"])
def reset_password():
    return AuthController.reset_password(request)


@auth_bp.route("/cambiar-password", methods=["POST"])
def change_password():
    return AuthController.change_password(request)


# -------------------------
# Soft Delete Usuario
# -------------------------
@auth_bp.route("/usuario/<int:user_id>", methods=["DELETE"])
@requiere_rol("ADMIN")
def delete_user(user_id):
    return AuthController.delete_user(request, user_id)


# -------------------------
# CRUD Usuarios (Nuevos endpoints para gestión de usuarios)
# -------------------------

# Listar todos los usuarios (solo ADMIN)
@auth_bp.route("/usuarios", methods=["GET"])
@requiere_rol("ADMIN")
def get_all_users():
    return AuthController.get_all_users(request)

# Crear nuevo usuario (solo ADMIN)
@auth_bp.route("/usuarios", methods=["POST"])
@requiere_rol("ADMIN")
def create_user():
    return AuthController.create_user(request)

# Obtener usuario por ID (ADMIN o el propio usuario)
@auth_bp.route("/usuarios/<int:user_id>", methods=["GET"])
def get_user_by_id(user_id):
    return AuthController.get_user_by_id(request, user_id)

# Actualizar usuario (ADMIN o el propio usuario)
@auth_bp.route("/usuarios/<int:user_id>", methods=["PUT"])
def update_user(user_id):
    return AuthController.update_user(request, user_id)
