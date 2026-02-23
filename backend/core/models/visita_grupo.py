from extension import db
from core.models.trabajo_revista import TipoReunion

class VisitaAcademica(db.Model): #antes Visita.ahora VisitaAcademica 
    __tablename__ = 'visita_grupo'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    razon = db.Column(db.Text, nullable=False)
    fecha = db.Column(db.Date, nullable=False)
    
    procedencia_visita_id = db.Column(db.Integer, db.ForeignKey('tipo_reunion_cientifica.id'), nullable=False)
    procedencia_visita = db.relationship('TipoReunion', back_populates='visitas')

    tipo_visita_id = db.Column(db.Integer, db.ForeignKey('tipo_visita.id'), nullable=False)
    tipo_visita = db.relationship('TipoVisita', back_populates='visitas')
    
    # --- Clave Foránea y Relación ---
    grupo_utn_id = db.Column(db.Integer, db.ForeignKey('grupo_utn.id')) 
    grupo_utn = db.relationship('GrupoInvestigacionUtn', back_populates='visitas')


    def serialize(self):
        data = {c.name: getattr(self, c.name) for c in self.__table__.columns}
        data["grupo"] = self.grupo_utn.nombre_sigla_grupo if self.grupo_utn else None
        data["visita_procedencia"] = {
            "id": self.procedencia_visita.id,
            "nombre": self.procedencia_visita.nombre
        }
        data["tipo_visita"] = {
            "id": self.tipo_visita.id,
            "nombre": self.tipo_visita.nombre   
        }
        return data
    
    
class TipoVisita(db.Model):
    __tablename__ = 'tipo_visita'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False, unique=True)
    
    visitas = db.relationship(
        'VisitaAcademica',
        back_populates='tipo_visita',
        lazy='select')
    
    def serialize(self):
        return {
            "id": self.id,
            "nombre": self.nombre
        }