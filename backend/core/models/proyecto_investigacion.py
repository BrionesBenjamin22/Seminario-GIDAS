from extension import db

class InvestigadorProyecto(db.Model):
    __tablename__ = "investigadorxproyecto"

    id_investigador = db.Column(
        db.Integer,
        db.ForeignKey("investigador.id"),
        primary_key=True
    )

    id_proyecto = db.Column(
        db.Integer,
        db.ForeignKey("proyecto_investigacion.id"),
        primary_key=True
    )

    fecha_inicio = db.Column(db.Date, nullable=False)
    fecha_fin = db.Column(db.Date, nullable=True)

    investigador = db.relationship("Investigador", back_populates="participaciones_proyecto")
    proyecto = db.relationship("ProyectoInvestigacion", back_populates="participaciones_investigador")

class BecarioProyecto(db.Model):
    __tablename__ = "becarioxproyecto"

    id_becario = db.Column(
        db.Integer,
        db.ForeignKey("becario.id"),
        primary_key=True
    )

    id_proyecto = db.Column(
        db.Integer,
        db.ForeignKey("proyecto_investigacion.id"),
        primary_key=True
    )

    fecha_inicio = db.Column(db.Date, nullable=False)
    fecha_fin = db.Column(db.Date, nullable=True)

    becario = db.relationship("Becario", back_populates="participaciones_proyecto")
    proyecto = db.relationship("ProyectoInvestigacion", back_populates="participaciones_becario")



class TipoProyecto(db.Model):
    __tablename__ = 'tipo_proyecto_investigacion'
    __table_args__ = (
        db.UniqueConstraint('nombre', name='uq_tipo_proyecto_nombre'),
    )
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.Text, nullable=False)
    proyectos_investigacion = db.relationship('ProyectoInvestigacion', back_populates='tipo_proyecto')


class ProyectoInvestigacion(db.Model):
    __tablename__ = 'proyecto_investigacion'

    id = db.Column(db.Integer, primary_key=True)
    codigo_proyecto = db.Column(db.Integer, nullable=False)
    nombre_proyecto = db.Column(db.Text, nullable=False)
    descripcion_proyecto = db.Column(db.Text, nullable=False)
    fecha_inicio = db.Column(db.Date, nullable=False)
    fecha_fin = db.Column(db.Date, nullable=True)
    dificultades_proyecto = db.Column(db.Text, nullable=True)

    tipo_proyecto_id = db.Column(db.Integer, db.ForeignKey('tipo_proyecto_investigacion.id'), nullable=False)
    tipo_proyecto = db.relationship('TipoProyecto', back_populates='proyectos_investigacion')

    grupo_utn_id = db.Column(db.Integer, db.ForeignKey('grupo_utn.id'))
    grupo_utn = db.relationship('GrupoInvestigacionUtn', back_populates='proyectos_investigacion')

    fuente_financiamiento_id = db.Column(db.Integer, db.ForeignKey('fuente_financiamiento.id'))
    fuente_financiamiento = db.relationship('FuenteFinanciamiento', back_populates='proyectos_investigacion')

    planificacion_id = db.Column(db.Integer, db.ForeignKey('planificacion_grupo.id'), nullable=True)
    planificacion = db.relationship('PlanificacionGrupo', back_populates='proyectos_investigacion')

    # --- Relaciones (Uno-a-Muchos) ---
    distinciones = db.relationship('DistincionRecibida', back_populates='proyecto_investigacion', cascade="all, delete-orphan")

    participaciones_investigador = db.relationship(
        "InvestigadorProyecto",
        back_populates="proyecto",
        cascade="all, delete-orphan"
    )

    participaciones_becario = db.relationship(
        "BecarioProyecto",
        back_populates="proyecto",
        cascade="all, delete-orphan"
    )
    def serialize(self):
        data = {c.name: getattr(self, c.name) for c in self.__table__.columns}

        data["grupo_utn"] = {
            "id": self.grupo_utn.id,
            "nombre": self.grupo_utn.nombre_sigla_grupo
        } if self.grupo_utn else None

        data["fuente_financiamiento"] = {
            "id": self.fuente_financiamiento.id,
            "nombre": self.fuente_financiamiento.nombre
        } if self.fuente_financiamiento else None

        data["planificacion"] = {
            "id": self.planificacion.id,
            "descripcion": self.planificacion.descripcion
        } if self.planificacion else None

        data["investigadores"] = [
        {
            "id": p.investigador.id,
            "nombre_apellido": p.investigador.nombre_apellido,
            "fecha_inicio": str(p.fecha_inicio),
            "fecha_fin": str(p.fecha_fin) if p.fecha_fin else None
        }
        for p in self.participaciones_investigador
        ]

        data["becarios"] = [
            {
                "id": p.becario.id,
                "nombre_apellido": p.becario.nombre_apellido,
                "fecha_inicio": str(p.fecha_inicio),
                "fecha_fin": str(p.fecha_fin) if p.fecha_fin else None
            }
            for p in self.participaciones_becario
        ]

        data["tipo_proyecto"] = {
            "id": self.tipo_proyecto.id,
            "nombre": self.tipo_proyecto.nombre
        } if self.tipo_proyecto else None

        data["distinciones"] = [
            d.serialize() for d in self.distinciones
        ]
        
        return data