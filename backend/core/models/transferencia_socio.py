from extension import db


adoptante_transferencia = db.Table(
    'adoptante_x_transferencia',
    db.Column('adoptante_id', db.Integer, db.ForeignKey('adoptante.id'), primary_key=True),
    db.Column('transferencia_socio_productiva_id', db.Integer, db.ForeignKey('transferencia_socio_productiva.id'), primary_key=True)
)


class Adoptante(db.Model):
    __tablename__ = 'adoptante'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    nombre = db.Column(db.Text, nullable=False)
    
    transferencias = db.relationship(
        'TransferenciaSocioProductiva',
        secondary=adoptante_transferencia,
        back_populates='adoptantes'
    )

    def serialize(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

class TransferenciaSocioProductiva(db.Model):
    __tablename__ = 'transferencia_socio_productiva'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    demandante = db.Column(db.Text, nullable=False)
    descripcion_actividad = db.Column(db.Text, nullable=False)
    monto = db.Column(db.Float, nullable=True)
    fecha_inicio = db.Column(db.Date, nullable=False)
    fecha_fin = db.Column(db.Date, nullable=True)
    
    adoptantes = db.relationship(
        'Adoptante',
        secondary=adoptante_transferencia,
        back_populates='transferencias'
    )

    tipo_contrato_id = db.Column(db.Integer, db.ForeignKey('tipo_contrato_transferencia.id'))
    tipo_contrato_transferencia = db.relationship('TipoContrato', back_populates='transferencias')

    grupo_utn_id = db.Column(db.Integer, db.ForeignKey('grupo_utn.id'))
    grupo_utn = db.relationship('GrupoInvestigacionUtn', back_populates='transferencias_socio_productivas')

    def serialize(self):
        data = {c.name: getattr(self, c.name) for c in self.__table__.columns}
        data.pop("tipo_contrato_id", None)
        data.pop("grupo_utn_id", None)
        data["tipo_contrato"] = (
            self.tipo_contrato_transferencia.nombre if self.tipo_contrato_transferencia else None
        )
        data["adoptantes"] = [adoptante.serialize() for adoptante in self.adoptantes]
        data["grupo"] = (
            self.grupo_utn.nombre_sigla_grupo if self.grupo_utn else None
        )
        data["fecha_inicio"] = self.fecha_inicio.isoformat()
        data["fecha_fin"] = self.fecha_fin.isoformat() if self.fecha_fin else None

        return data


class TipoContrato(db.Model):
    __tablename__ = 'tipo_contrato_transferencia'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    nombre = db.Column(db.Text, nullable=False)

    transferencias = db.relationship('TransferenciaSocioProductiva', back_populates='tipo_contrato_transferencia')

    def serialize(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}