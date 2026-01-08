from extension import db

class Equipamiento(db.Model):
    __tablename__ = 'equipamiento_grupo'

    id = db.Column(db.Integer, primary_key=True)
    denominacion = db.Column(db.Text, nullable=False)
    descripcion_breve = db.Column(db.Text, nullable=False)
    fecha_incorporacion = db.Column(db.Date, nullable=False)  # mejor como Date
    monto_invertido = db.Column(db.Float, nullable=False)

    # --- Claves Foráneas y Relaciones ---
    grupo_utn_id = db.Column(db.Integer, db.ForeignKey('grupo_utn.id'))
    grupo_utn = db.relationship('GrupoInvestigacionUtn', back_populates='equipamiento')


    def serialize(self):
        """Serializa la instancia de Equipamiento en un diccionario."""
        data = {c.name: getattr(self, c.name) for c in self.__table__.columns}
        data["grupo"] = self.grupo_utn.nombre_sigla_grupo if self.grupo_utn else None
        data["fuente_financiamiento"] = self.fuente_financiamiento.nombre if self.fuente_financiamiento else None
        return data
    
    