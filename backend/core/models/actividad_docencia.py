from extension import db

class ActividadDocencia(db.Model):
    __tablename__ = 'actividad_y_catedra_posgrado'
    id = db.Column(db.Integer, primary_key=True)
    curso = db.Column(db.Text, nullable=False)
    institucion = db.Column(db.Text, nullable=False)
    fecha_inicio = db.Column(db.Date, nullable=False)
    fecha_fin = db.Column(db.Date, nullable=False)
    
    # --- Clave Foránea y Relación ---
    investigador_id = db.Column(db.Integer, db.ForeignKey('investigador.id'))
    investigador = db.relationship('Investigador', back_populates='actividades_docencia')
    grado_academico_id = db.Column(db.Integer, db.ForeignKey('grado_academico.id'))
    grado_academico = db.relationship('GradoAcademico', back_populates='actividades_docencia')
    rol_actividad_id = db.Column(db.Integer, db.ForeignKey('rol_actividad_docencia.id'))
    rol_actividad = db.relationship('RolActividad', back_populates='actividades_docencia')

    
    def serialize(self):
        data = {c.name: getattr(self, c.name) for c in self.__table__.columns}
        data["investigador"] = self.investigador.nombre_apellido if self.investigador else None
        data["grado_academico"] = {
            "id": self.grado_academico.id,
            "nombre": self.grado_academico.nombre
        } if self.grado_academico else None
        
        data["rol_actividad"] = {
            "id": self.rol_actividad.id,
            "nombre": self.rol_actividad.nombre
        } if self.rol_actividad else None
        
        return data 



class RolActividad(db.Model):
    __tablename__ = 'rol_actividad_docencia'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False, unique=True)

    actividades_docencia = db.relationship(
        'ActividadDocencia',
        back_populates='rol_actividad',
        lazy='select'
    )

    def serialize(self):
        return {
            "id": self.id,
            "nombre": self.nombre
        }
        
        
class GradoAcademico(db.Model):
    __tablename__ = 'grado_academico'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False, unique=True)

    actividades_docencia = db.relationship(
        'ActividadDocencia',
        back_populates='grado_academico',
        lazy='select'
    )

    def serialize(self):
        return {
            "id": self.id,
            "nombre": self.nombre
        }