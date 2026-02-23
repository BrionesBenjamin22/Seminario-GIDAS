from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm.exc import NoResultFound
from extension import db

class GrupoInvestigacionUtn(db.Model):
    __tablename__ = 'grupo_utn'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    mail = db.Column(db.Text, nullable=False)
    nombre_unidad_academica = db.Column(db.Text, nullable=False)
    objetivo_desarrollo = db.Column(db.Text, nullable=False)
    nombre_sigla_grupo = db.Column(db.Text, nullable=False)

    # --- Relaciones ---
    participaciones_directivos = db.relationship('DirectivoGrupo', back_populates='grupo_utn', cascade="all, delete-orphan")
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
        """
        Serialización liviana del grupo.
        NO carga colecciones grandes.
        """
        return {
            "id": self.id,
            "mail": self.mail,
            "nombre_unidad_academica": self.nombre_unidad_academica,
            "objetivo_desarrollo": self.objetivo_desarrollo,
            "nombre_sigla_grupo": self.nombre_sigla_grupo,
            "directivos": [
                {
                    "id": p.directivo.id,
                    "nombre_apellido": p.directivo.nombre_apellido,
                    "cargo": p.cargo.nombre if p.cargo else None,
                    "fecha_inicio": str(p.fecha_inicio)
                    } for p in self.participaciones_directivos if p.fecha_fin is None  # solo directivos activos
            ],


            # métricas resumidas, para evitar devolver listas completas
            "cant_investigadores": len(self.investigadores),
            "cant_becarios": len(self.becarios),
            "cant_personal": len(self.personal),
            "cant_proyectos": len(self.proyectos_investigacion),
            "cant_documentacion": len(self.documentacion),
            "cant_equipamiento": len(self.equipamiento),
            "cant_erogaciones": len(self.erogaciones),
            "cant_patentes": len(self.registros_propiedad)
        }


    @classmethod
    def load(cls):
        return db.session.query(cls).first()