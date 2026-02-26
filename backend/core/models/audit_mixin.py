from datetime import date, datetime
from sqlalchemy.ext.declarative import declared_attr
from extension import db


class AuditMixin:

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        nullable=False
    )

    deleted_at = db.Column(db.DateTime, nullable=True)


    @declared_attr
    def created_by(cls):
        return db.Column(db.Integer, db.ForeignKey("usuario.id"), nullable=True)


    @declared_attr
    def deleted_by(cls):
        return db.Column(db.Integer, db.ForeignKey("usuario.id"), nullable=True)

    def soft_delete(self, user_id: int):
        self.deleted_at = datetime.utcnow()
        self.deleted_by = user_id

    def restore(self):
        self.deleted_at = None
        self.deleted_by = None
        
    def to_dict(self):
        data = {}

        for column in self.__table__.columns:
            value = getattr(self, column.name)

            if isinstance(value, (datetime, date)):
                value = value.isoformat()

            data[column.name] = value

        return data