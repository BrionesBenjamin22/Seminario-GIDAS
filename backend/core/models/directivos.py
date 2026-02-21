from extension import db



class DirectivoGrupo(db.Model):
    __tablename__ = 'directivo_grupo'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    id_directivo = db.Column(
        db.Integer,
        db.ForeignKey('directivo.id'),
        nullable=False
    )

    id_grupo_utn = db.Column(
        db.Integer,
        db.ForeignKey('grupo_utn.id'),
        nullable=False
    )

    id_cargo = db.Column(
        db.Integer,
        db.ForeignKey('cargo.id'),
        nullable=False
    )

    fecha_inicio = db.Column(db.Date, nullable=False)
    fecha_fin = db.Column(db.Date, nullable=True)

    directivo = db.relationship(
        'Directivo',
        back_populates='participaciones_grupo'
    )

    grupo_utn = db.relationship(
        'GrupoInvestigacionUtn',
        back_populates='participaciones_directivos'
    )

    cargo = db.relationship(
        'Cargo',
        back_populates='participaciones'
    )
    
class Cargo(db.Model):
    __tablename__ = 'cargo'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    nombre = db.Column(db.Text, nullable=False)

    participaciones = db.relationship(
        'DirectivoGrupo',
        back_populates='cargo',
        cascade="all, delete-orphan"
    )

    def serialize(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class Directivo(db.Model):
    __tablename__ = 'directivo'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    nombre_apellido = db.Column(db.Text, nullable=False)

    participaciones_grupo = db.relationship(
        'DirectivoGrupo',
        back_populates='directivo',
        cascade="all, delete-orphan"
    )

    def serialize(self):
        return {
            "id": self.id,
            "nombre_apellido": self.nombre_apellido
        }
    