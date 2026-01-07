from extension import db


class PlanificacionGrupo(db.Model): #antes Planificacion. ahora PlanificacionGrupo
    __tablename__ = 'planificacion_grupo'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    descripcion = db.Column(db.Text, nullable=False)
    anio = db.Column(db.Integer, nullable=False)

    # --- Clave Foránea y Relación ---
    grupo_id = db.Column(db.Integer, db.ForeignKey('grupo_utn.id')) 
    grupo_utn = db.relationship('GrupoInvestigacionUtn', back_populates='planificaciones')

    proyectos_investigacion = db.relationship('ProyectoInvestigacion', back_populates='planificaciones')
    
    def serialize(self):
        data = {c.name: getattr(self, c.name) for c in self.__table__.columns}
        data["grupo"] = self.grupo_utn.nombre_sigla_grupo if self.grupo_utn else None
        return data