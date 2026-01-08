from extension import db

investigador_proyecto = db.Table(
    'investigadorxproyecto',
    db.Column('id_investigador', db.Integer, db.ForeignKey('investigador.id'), primary_key=True),
    db.Column('id_proyecto', db.Integer, db.ForeignKey('proyecto_investigacion.id'), primary_key=True)
)

becario_proyecto = db.Table(
    'becarioxproyecto',
    db.Column('id_becario', db.Integer, db.ForeignKey('becario.id'), primary_key=True),
    db.Column('id_proyecto', db.Integer, db.ForeignKey('proyecto_investigacion.id'), primary_key=True)
)


class TipoProyecto(db.Model):
    __tablename__ = 'tipo_proyecto_investigacion'
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
    fecha_fin = db.Column(db.Date, nullable=False)
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
    trabajos_revistas = db.relationship('TrabajosRevistasReferato', back_populates='proyecto_investigacion', cascade="all, delete-orphan")
    distinciones = db.relationship('DistincionRecibida', back_populates='proyecto_investigacion', cascade="all, delete-orphan")

    # --- Relaciones (Muchos-a-Muchos) ---
    investigadores = db.relationship('Investigador', secondary=investigador_proyecto, back_populates='proyectos')
    becarios = db.relationship('Becario', secondary=becario_proyecto, back_populates='proyectos')

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
            {"id": i.id, "nombre": i.nombre_apellido}
            for i in self.investigadores
        ]
        data["becarios"] = [
            {"id": b.id, "nombre": b.nombre_apellido}
            for b in self.becarios
        ]

        data["tipo_proyecto"] = {
            "id": self.tipo_proyecto.id,
            "nombre": self.tipo_proyecto.nombre
        } if self.tipo_proyecto else None

        return data