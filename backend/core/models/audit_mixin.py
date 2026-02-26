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
    
    activo = db.Column(db.Boolean, default=True, nullable=False)


    @declared_attr
    def created_by(cls):
        return db.Column(db.Integer, db.ForeignKey("usuario.id"), nullable=True)


    @declared_attr
    def deleted_by(cls):
        return db.Column(db.Integer, db.ForeignKey("usuario.id"), nullable=True)

    @declared_attr
    def creator(cls):
        return db.relationship("Usuario", foreign_keys=[cls.created_by], primaryjoin=f"Usuario.id == {cls.__name__}.created_by")

    @declared_attr
    def deleter(cls):
        return db.relationship("Usuario", foreign_keys=[cls.deleted_by], primaryjoin=f"Usuario.id == {cls.__name__}.deleted_by")

    def soft_delete(self, user_id: int):
        self.deleted_at = datetime.utcnow()
        self.deleted_by = user_id
        self.activo = False

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

        # Inyectar nombres de auditoría
        try:
            data["creator_name"] = self.creator.nombre_usuario if self.creator else None
            data["deleter_name"] = self.deleter.nombre_usuario if self.deleter else None
        except Exception as e:
            print(f"Error in AuditMixin: {e}")
            import traceback
            traceback.print_exc()
            data["creator_name"] = None
            data["deleter_name"] = None

        return data