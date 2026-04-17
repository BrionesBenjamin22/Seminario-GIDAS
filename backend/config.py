import os
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, ".env"))

class Config:
    # -------------------------
    # -------------------------
    SECRET_KEY = os.getenv("SECRET_KEY") or "gidas-dev-secret-key-do-not-use-in-production-2024"
    FRONTEND_URL = os.getenv("FRONTEND_URL") or "http://localhost:5173"



    # -------------------------
    # Database
    # -------------------------
    SQLALCHEMY_DATABASE_URI = os.getenv(
        "DATABASE_URL",
        "postgresql://postgres:Br4ndsen8.@localhost:5432/gidas_db"
    )


    SQLALCHEMY_TRACK_MODIFICATIONS = os.getenv("SQLALCHEMY_TRACK_MODIFICATIONS", "False") == "True"

    # -------------------------
    # JWT Configuration

    # -------------------------
    JWT_SECRET = os.getenv("JWT_SECRET") or SECRET_KEY
    REFRESH_SECRET = os.getenv("REFRESH_SECRET") or SECRET_KEY
    JWT_ALGORITHM = "HS256"
    JWT_EXPIRATION_MINUTES = int(os.getenv("JWT_EXPIRATION_MINUTES", 60))


class DevelopmentConfig(Config):
    DEBUG = True


class ProductionConfig(Config):
    DEBUG = False
