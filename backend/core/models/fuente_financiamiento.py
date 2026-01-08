from extension import db

class FuenteFinanciamiento(db.Model):
    __tablename__ = 'fuente_financiamiento'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.Text) 

    # Relación uno-a-muchos con Becario
    becarios = db.relationship('Becario', back_populates='fuente_financiamiento')
    proyectos_investigacion = db.relationship('ProyectoInvestigacion', back_populates='fuente_financiamiento')
    erogaciones = db.relationship('Erogacion', back_populates='fuente_financiamiento', cascade="all, delete-orphan")
    
    def serialize(self):
        data = {c.name: getattr(self, c.name) for c in self.__table__.columns}
        data["proyectos"] = [p.codigo_proyecto for p in self.proyectos_investigacion]
        data["becarios"] = [b.nombre_apellido for b in self.becarios]
        return data
    
    def get_total_proyectos(self):
        return len(self.proyectos_investigacion)

    def get_total_becarios(self):
        return len(self.becarios)
    
    