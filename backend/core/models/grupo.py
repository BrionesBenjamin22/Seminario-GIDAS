from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm.exc import NoResultFound
from extension import db

class GrupoInvestigacionUtn(db.Model):  # antes GrupoUtn, ahora GrupoInvestigacionUtn
    __tablename__ = 'grupo_utn'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    mail = db.Column(db.Text, nullable=False)
    nombre_unidad_academica = db.Column(db.Text, nullable=False)
    objetivo_desarrollo = db.Column(db.Text, nullable=False)
    nombre_sigla_grupo = db.Column(db.Text, nullable=False)

    # --- Relaciones (Uno-a-Muchos) ---
    investigadores = db.relationship('Investigador', back_populates='grupo_utn', cascade="all, delete-orphan")
    becarios = db.relationship('Becario', back_populates="grupo_utn", cascade="all, delete-orphan")
    personal = db.relationship('Personal', back_populates="grupo_utn", cascade="all, delete-orphan")
    documentacion = db.relationship('DocumentacionBibliografica', back_populates='grupo_utn', cascade="all, delete-orphan")
    equipamiento = db.relationship('Equipamiento', back_populates='grupo_utn', cascade="all, delete-orphan")
    proyectos_investigacion = db.relationship('ProyectoInvestigacion', back_populates='grupo_utn', cascade="all, delete-orphan")
    planificaciones = db.relationship('PlanificacionGrupo', back_populates='grupo_utn', cascade="all, delete-orphan")
    visitas = db.relationship('VisitaAcademica', back_populates='grupo_utn', cascade="all, delete-orphan")
    registros_propiedad = db.relationship('RegistrosPropiedad', back_populates='grupo_utn', cascade="all, delete-orphan")
    trabajos_revistas = db.relationship('TrabajosRevistasReferato', back_populates='grupo_utn', cascade="all, delete-orphan")
    trabajos_reunion_cientifica = db.relationship('TrabajoReunionCientifica', back_populates='grupo_utn', cascade="all, delete-orphan")
    erogaciones = db.relationship('Erogacion', back_populates='grupo_utn', cascade="all, delete-orphan")
    transferencias_socio_productivas = db.relationship('TransferenciaSocioProductiva', back_populates='grupo_utn', cascade="all, delete-orphan")
    articulos_divulgacion = db.relationship('ArticuloDivulgacion', back_populates='grupo_utn', cascade="all, delete-orphan")

    def serialize(self):
        data = {c.name: getattr(self, c.name) for c in self.__table__.columns}
        data["investigadores"] = [i.nombre_apellido for i in self.investigadores]
        data["proyectos"] = [p.codigo_proyecto for p in self.proyectos_investigacion]
        data["documentacion"] = [d.titulo for d in self.documentacion]
        data["equipamiento"] = [e.descripcion for e in self.equipamiento]
        data["planificaciones"] = [p.descripcion for p in self.planificaciones]
        data["visitas"] = [v.institucion for v in self.visitas]
        data["registros_propiedad"] = [r.titulo for r in self.registros_propiedad]
        data["trabajos_revistas"] = [t.titulo for t in self.trabajos_revistas]
        data["trabajos_reunion_cientifica"] = [t.titulo for t in self.trabajos_reunion_cientifica]
        data["erogaciones"] = [e.monto for e in self.erogaciones]
        data["transferencias_socio_productivas"] = [t.descripcion for t in self.transferencias_socio_productivas]
        return data

    @classmethod
    def load(cls) -> "GrupoInvestigacionUtn":
        try:
            return db.session.query(cls).filter_by(id=1).one()
        except NoResultFound:
            try:
                with db.session.begin_nested():
                    instancia = cls(
                        id=1,
                        mail="grupo@frlp.utn.edu.ar",
                        nombre_unidad_academica="Grupo Innovación y Desarrollo Aplicado a Sistemas de Información",
                        objetivo_desarrollo="Desarrollar investigaciones en el área de sistemas de potencia",
                        nombre_sigla_grupo="GIDAS"
                    )
                    db.session.add(instancia)
                    db.session.commit()
                    return instancia
            except IntegrityError:
                db.session.rollback()
                return cls.query.get(1)