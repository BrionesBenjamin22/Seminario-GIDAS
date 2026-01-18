from extension import db

class TrabajoReunionCientifica(db.Model):
    __tablename__ = 'trabajo_reunion_cientifica'
    id = db.Column(db.Integer, primary_key=True)
    titulo_trabajo = db.Column(db.Text, nullable=False, unique=True)
    nombre_reunion = db.Column(db.Text, nullable=False)
    ciudad = db.Column(db.Text, nullable=False)
    fecha_inicio = db.Column(db.Date, nullable=False)
    tipo_reunion_cientifica = db.Column(db.Text, nullable=False)
    
    # --- Clave Foránea y Relación ---
    investigador_id = db.Column(db.Integer, db.ForeignKey('investigador.id')) 
    investigador = db.relationship('Investigador', back_populates='trabajos_reunion_cientifica')
	
	# --- Relaciones (Muchos-a-Uno) ---
    grupo_utn_id = db.Column(db.Integer, db.ForeignKey('grupo_utn.id')) 
    grupo_utn = db.relationship('GrupoInvestigacionUtn', back_populates='trabajos_reunion_cientifica')
    
    def serialize(self):
        data = {c.name: getattr(self, c.name) for c in self.__table__.columns}
        data["investigador"] = self.investigador.nombre_apellido if self.investigador else None
        data["grupo_utn"] = self.grupo_utn.nombre_unidad_academica if self.grupo_utn else None
        return data