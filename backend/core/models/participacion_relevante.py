from extension import db

class ParticipacionRelevante(db.Model):
    __tablename__ = 'participacion_relevante'
    id = db.Column(db.Integer, primary_key=True)
    nombre_evento = db.Column(db.Text, nullable=False) 
    forma_participacion = db.Column(db.Text, nullable=False) 
    fecha = db.Column(db.Date, nullable=False) 

    # --- Clave Foránea y Relación ---
    investigador_id = db.Column(db.Integer, db.ForeignKey('investigador.id')) 
    investigador = db.relationship('Investigador', back_populates='participaciones_relevantes')

    def serialize(self):
        data = {c.name: getattr(self, c.name) for c in self.__table__.columns}
        data["investigador"] = self.investigador.nombre_apellido if self.investigador else None
        return data
    
