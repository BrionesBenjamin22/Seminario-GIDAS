from backend.extension import db

class RegistrosPropiedad(db.Model):
    __tablename__ = 'registros_patente_grupo'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    nombre_articulo = db.Column(db.Text, nullable=False)
    organismo_registrante = db.Column(db.Text, nullable=False)
    
    # --- Clave Foránea y Relación ---
    tipo_registro_id = db.Column(db.Integer, db.ForeignKey('tipo_registro_propiedad.id'), nullable=False)
    tipo_registro = db.relationship('TipoRegistroPropiedad', back_populates='registros_propiedad')
    grupo_utn_id = db.Column(db.Integer, db.ForeignKey('grupo_utn.id'), nullable=False) 
    grupo_utn = db.relationship('GrupoInvestigacionUtn', back_populates='registros_propiedad')
    
    def serialize(self):
        data = {c.name: getattr(self, c.name) for c in self.__table__.columns}
        data["grupo"] = self.grupo_utn.nombre_sigla_grupo if self.grupo_utn else None
        return data
    
    
class TipoRegistroPropiedad(db.Model):
    __tablename__ = 'tipo_registro_propiedad'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    nombre = db.Column(db.Text, nullable=False)
    
    registros_propiedad = db.relationship('RegistrosPropiedad', back_populates='tipo_registro', cascade ="all, delete-orphan")
    
    def serialize(self):
        data = {c.name: getattr(self, c.name) for c in self.__table__.columns}
        return data