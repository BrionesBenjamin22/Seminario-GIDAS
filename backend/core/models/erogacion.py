from extension import db

class TipoErogacion(db.Model):
    __tablename__ = 'tipo_erogacion'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    nombre = db.Column(db.Text, nullable=False)

    erogaciones = db.relationship('Erogacion', back_populates='tipo_erogacion', cascade="all, delete-orphan")

    def serialize(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class Erogacion(db.Model):
    __tablename__ = 'erogacion'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    numero_erogacion = db.Column(db.Integer, nullable=True)  # nuevo campo para el número de erogación
    egresos = db.Column(db.Float, nullable=False)   # mejor Float para montos
    ingresos = db.Column(db.Float, nullable=False)

    tipo_erogacion_id = db.Column(db.Integer, db.ForeignKey('tipo_erogacion.id'))
    tipo_erogacion = db.relationship('TipoErogacion', back_populates='erogaciones')

    fuente_financiamiento_id = db.Column(db.Integer, db.ForeignKey('fuente_financiamiento.id'))
    fuente_financiamiento = db.relationship('FuenteFinanciamiento', back_populates='erogaciones')

    grupo_utn_id = db.Column(db.Integer, db.ForeignKey('grupo_utn.id'))
    grupo_utn = db.relationship('GrupoInvestigacionUtn', back_populates='erogaciones')

    def serialize(self):
        data = {c.name: getattr(self, c.name) for c in self.__table__.columns}

        data["numeroErogacion"] = self.numero_erogacion

        data.pop("tipo_erogacion_id", None)
        data.pop("fuente_financiamiento_id", None)
        data.pop("grupo_utn_id", None)

        data["grupo"] = {
            "id": self.grupo_utn.id,
            "nombre": self.grupo_utn.nombre_sigla_grupo
        } if self.grupo_utn else None

        data["fuente"] = {
            "id": self.fuente_financiamiento.id,
            "nombre": self.fuente_financiamiento.nombre
        } if self.fuente_financiamiento else None

        data["tipo_erogacion"] = {
            "id": self.tipo_erogacion.id,
            "nombre": self.tipo_erogacion.nombre
        } if self.tipo_erogacion else None

        return data
