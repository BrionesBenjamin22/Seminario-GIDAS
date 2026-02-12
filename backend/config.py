import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY")
    FRONTEND_URL = os.getenv("FRONTEND_URL")

    # -------------------------
    # Mail
    # -------------------------
    MAIL_SERVER = os.getenv("MAIL_SERVER")
    MAIL_PORT = int(os.getenv("MAIL_PORT", 587))
    MAIL_USE_TLS = os.getenv("MAIL_USE_TLS", "True") == "True"
    MAIL_USERNAME = os.getenv("MAIL_USERNAME")
    MAIL_PASSWORD = os.getenv("MAIL_PASSWORD")
    MAIL_DEFAULT_SENDER = os.getenv("MAIL_DEFAULT_SENDER")

    # -------------------------
    # Database
    # -------------------------
    SQLALCHEMY_DATABASE_URI = "sqlite:///gidas.db"

    SQLALCHEMY_TRACK_MODIFICATIONS = os.getenv("SQLALCHEMY_TRACK_MODIFICATIONS", "False") == "True"

    # -------------------------
    # JWT (🔴 ESTO FALTABA)
    # -------------------------
    JWT_SECRET = os.getenv("JWT_SECRET", SECRET_KEY)
    REFRESH_SECRET = os.getenv("REFRESH_SECRET", SECRET_KEY)
    JWT_ALGORITHM = "HS256"
    JWT_EXPIRATION_MINUTES = int(os.getenv("JWT_EXPIRATION_MINUTES", 60))


class DevelopmentConfig(Config):
    DEBUG = True


class ProductionConfig(Config):
    DEBUG = False
