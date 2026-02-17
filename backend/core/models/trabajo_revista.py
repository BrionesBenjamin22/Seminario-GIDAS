import re
from sqlalchemy.orm import validates
from extension import db

# tabla M:M con investigador

class TrabajosRevistasReferato(db.Model):
    __tablename__ = 'trabajos_revista'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    titulo_trabajo = db.Column(db.Text, nullable=False) 
    nombre_revista = db.Column(db.Text, nullable=False) 
    editorial = db.Column(db.Text, nullable=False) 
    issn = db.Column(db.Text, nullable=False) 
    pais = db.Column(db.Text, nullable=False) 

    # --- Clave Foránea y Relación ---
    grupo_utn_id = db.Column(db.Integer, db.ForeignKey('grupo_utn.id')) 
    grupo_utn = db.relationship('GrupoInvestigacionUtn', back_populates='trabajos_revistas') 
    
    
    def serialize(self):
        data = {c.name: getattr(self, c.name) for c in self.__table__.columns}
        data["grupo"] = self.grupo_utn.nombre_sigla_grupo if self.grupo_utn else None
        return data
    
    @validates('issn')
    def validar_issn(self, key, value):
        assert re.match(r'^\d{4}-\d{3}[\dX]$', value), "Formato ISSN inválido"
        return value

