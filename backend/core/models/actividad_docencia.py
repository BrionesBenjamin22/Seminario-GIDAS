from extension import db


class ActividadDocencia(db.Model):
    __tablename__ = 'actividad_y_catedra_posgrado'
    id = db.Column(db.Integer, primary_key=True)
    curso = db.Column(db.Text, nullable=False)
    institucion = db.Column(db.Text, nullable=False)
    fecha_inicio = db.Column(db.Date, nullable=False)
    fecha_fin = db.Column(db.Date, nullable=False)
    grado_academico = db.Column(db.Text, nullable=False)
    rol_actividad = db.Column(db.Text, nullable=False)

    # --- Clave Foránea y Relación ---
    investigador_id = db.Column(db.Integer, db.ForeignKey('investigador.id'), nullable=False) 
    investigador = db.relationship('Investigador', back_populates='actividades_docencia')
    
    
    
    def serialize(self):
        data = {c.name: getattr(self, c.name) for c in self.__table__.columns}
        data["investigador"] = self.investigador.nombre_apellido if self.investigador else None
        return data 

