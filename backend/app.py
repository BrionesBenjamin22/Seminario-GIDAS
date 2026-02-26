from flask import Flask, request
from extension import db, mail, migrate
from flask_cors import CORS
from config import DevelopmentConfig
import logging
from core.routes import blueprints
from sqlalchemy.orm import with_loader_criteria
from sqlalchemy import event
from core.models.audit_mixin import AuditMixin


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def create_app():
    app = Flask(__name__)
    app.config.from_object(DevelopmentConfig)

    CORS(
        app,
        resources={r"/*": {
            "origins": ["http://localhost:5173", "http://127.0.0.1:5173"],
            "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
            "allow_headers": ["Content-Type", "Authorization"]
        }},
        supports_credentials=True
    )

    db.init_app(app)
    mail.init_app(app)
    migrate.init_app(app, db)


    if not hasattr(db.session, "_soft_delete_filter_registered"):

        @event.listens_for(db.session, "do_orm_execute")
        def _add_filtering_criteria(execute_state):
            if (
                execute_state.is_select
                and not execute_state.execution_options.get("include_deleted", False)
            ):
                execute_state.statement = execute_state.statement.options(
                    with_loader_criteria(
                        AuditMixin,
                        lambda cls: cls.deleted_at.is_(None),
                        include_aliases=True,
                    )
                )

        db.session._soft_delete_filter_registered = True

    # ---- EVENTOS DE AUDITORÍA ----
    from flask import g

    @event.listens_for(db.session, "before_flush")
    def before_flush(session, flush_context, instances):
        user_id = None
        try:
            user_id = g.get("current_user_id")
        except Exception:
            pass

        if not user_id:
            return

        for obj in session.new:
            if isinstance(obj, AuditMixin):
                if hasattr(obj, 'created_by') and obj.created_by is None:
                    obj.created_by = user_id

        # Para actualizaciones, el soft_delete manual ya setea deleted_by,
        # pero podríamos automatizar otros aspectos aquí si fuera necesario.

    for bp in blueprints:
        app.register_blueprint(bp)

    logger.info("Aplicación inicializada. Usa 'flask db upgrade' para crear/migrar tablas.")

    return app


app = create_app()

if __name__ == "__main__":
    app.run(debug=True)