from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail
from flask_migrate import Migrate

# Instancia de SQLAlchemy compartida
mail = Mail()
db = SQLAlchemy()
migrate = Migrate()