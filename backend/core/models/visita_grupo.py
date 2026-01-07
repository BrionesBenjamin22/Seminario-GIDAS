from extension import db

class VisitaAcademica(db.Model): #antes Visita.ahora VisitaAcademica 
    __tablename__ = 'visita_grupo'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    tipo_visita = db.Column(db.Text, nullable=False)
    razon = db.Column(db.Text, nullable=False)
    procedencia = db.Column(db.Text, nullable=False)
    fecha = db.Column(db.Date, nullable=False)

    # --- Clave Foránea y Relación ---
    grupo_utn_id = db.Column(db.Integer, db.ForeignKey('grupo_utn.id')) 
    grupo_utn = db.relationship('GrupoInvestigacionUtn', back_populates='visitas')


    def serialize(self):
        data = {c.name: getattr(self, c.name) for c in self.__table__.columns}
        data["grupo"] = self.grupo_utn.nombre_sigla_grupo if self.grupo_utn else None
        return data