from core.models.audit_mixin import AuditMixin
from extension import db

class Beca(db.Model, AuditMixin):
    __tablename__ = "beca"

    id = db.Column(db.Integer, primary_key=True)
    nombre_beca = db.Column(db.String(100), nullable=False)
    descripcion = db.Column(db.Text, nullable=True)

    becarios = db.relationship(
        "Beca_Becario",
        back_populates="beca"
    )

    def serialize(self):
        data = self.to_dict()

        data["becarios"] = [
            {
                "id": b.becario.id,
                "nombre_apellido": b.becario.nombre_apellido,
                "fecha_inicio": b.fecha_inicio.isoformat(),
                "fecha_fin": b.fecha_fin.isoformat() if b.fecha_fin else None,
                "monto_percibido": b.monto_percibido
            }
            for b in self.becarios
            if b.deleted_at is None
        ]

        return data


class Beca_Becario(db.Model, AuditMixin):
    __tablename__ = "beca_becario"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    id_beca = db.Column(
        db.Integer,
        db.ForeignKey("beca.id"),
        nullable=False
    )

    id_becario = db.Column(
        db.Integer,
        db.ForeignKey("becario.id"),
        nullable=False
    )

    fecha_inicio = db.Column(db.Date, nullable=False)
    fecha_fin = db.Column(db.Date, nullable=True)
    monto_percibido = db.Column(db.Float, nullable=True)

    __table_args__ = (
        db.UniqueConstraint(
            "id_beca",
            "id_becario",
            "deleted_at",
            name="uq_beca_becario_activo"
        ),
    )

    beca = db.relationship("Beca", back_populates="becarios")
    becario = db.relationship("Becario", back_populates="becas")