from flask import Blueprint, request
from core.controllers.auth_controller import AuthController

auth_bp = Blueprint("auth", __name__, url_prefix="/auth")


# -------------------------
# Registro
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
# Change password
# -------------------------
@auth_bp.route("/change-password", methods=["PUT"])
def change_password():
    return AuthController.change_password(request)

