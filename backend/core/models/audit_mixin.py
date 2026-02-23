from datetime import datetime
from sqlalchemy.ext.declarative import declared_attr
from extension import db


class AuditMixin:

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        nullable=False
    )

    updated_at = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        nullable=False
    )

    deleted_at = db.Column(db.DateTime, nullable=True)

    activo = db.Column(db.Boolean, default=True, nullable=False)

    @declared_attr
    def created_by(cls):
        return db.Column(db.Integer, db.ForeignKey("usuario.id"), nullable=True)

    @declared_attr
    def updated_by(cls):
        return db.Column(db.Integer, db.ForeignKey("usuario.id"), nullable=True)

    @declared_attr
    def deleted_by(cls):
        return db.Column(db.Integer, db.ForeignKey("usuario.id"), nullable=True)

    def soft_delete(self, user_id: int):
        self.activo = False
        self.deleted_at = datetime.utcnow()
        self.deleted_by = user_id

    def restore(self):
        self.activo = True
        self.deleted_at = None
        self.deleted_by = None