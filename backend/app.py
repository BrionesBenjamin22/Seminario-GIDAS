from flask import Flask
from extension import db, mail, migrate
from flask_cors import CORS
from config import DevelopmentConfig
import logging
from core.routes import blueprints
import core.models

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def create_app():
    app = Flask(__name__)
    app.config.from_object(DevelopmentConfig)

    CORS(
    app,
    resources={r"/*": {"origins": "http://localhost:5173"}},
    supports_credentials=True
)

    db.init_app(app)
    mail.init_app(app)
    migrate.init_app(app, db)
    
    for bp in blueprints:
        app.register_blueprint(bp)

    logger.info("Aplicación inicializada. Usa 'flask db upgrade' para crear/migrar tablas.")

    return app

app = create_app()

if __name__ == "__main__":
    app.run(debug=True)