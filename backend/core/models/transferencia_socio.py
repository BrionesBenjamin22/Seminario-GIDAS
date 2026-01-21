from extension import db

class TransferenciaSocioProductiva(db.Model):
    __tablename__ = 'transferencia_socio_productiva'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    adoptante = db.Column(db.Text, nullable=False)
    demandante = db.Column(db.Text, nullable=False)
    descripcion_actividad = db.Column(db.Text, nullable=False)
    monto = db.Column(db.Float, nullable=False)

    tipo_contrato_id = db.Column(db.Integer, db.ForeignKey('tipo_contrato_transferencia.id'))
    tipo_contrato_transferencia = db.relationship('TipoContrato', back_populates='transferencias')

    grupo_utn_id = db.Column(db.Integer, db.ForeignKey('grupo_utn.id'))
    grupo_utn = db.relationship('GrupoInvestigacionUtn', back_populates='transferencias_socio_productivas')

    def serialize(self):
        data = {c.name: getattr(self, c.name) for c in self.__table__.columns}
        data.pop("tipo_contrato_id")
        data.pop("grupo_utn_id")
        data["tipo_contrato"] = (
            self.tipo_contrato_transferencia.nombre if self.tipo_contrato_transferencia else None
        )
        data["grupo"] = (
            self.grupo_utn.nombre_sigla_grupo if self.grupo_utn else None
        )
        return data


class TipoContrato(db.Model):
    __tablename__ = 'tipo_contrato_transferencia'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    nombre = db.Column(db.Text, nullable=False)

    transferencias = db.relationship('TransferenciaSocioProductiva', back_populates='tipo_contrato_transferencia')

    def serialize(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}