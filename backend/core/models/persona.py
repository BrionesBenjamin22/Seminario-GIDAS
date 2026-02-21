from extension import db

class Persona(db.Model):
    __tablename__ = "persona"
    
    id = db.Column(db.Integer, primary_key=True)
    nombre_apellido = db.Column(db.String(100), nullable=False)
    dni = db.Column(db.Integer, unique=True, nullable=False)
    
    usuario = db.relationship(
        "Usuario",
        back_populates="persona",
        uselist=False
    )
    
    
    def serialize(self):
        return {
            "id": self.id,
            "nombre_apellido": self.nombre_apellido,
            "dni": self.dni
        }
    
    