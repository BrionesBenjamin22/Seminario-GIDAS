from extension import db

class Beca(db.Model):
    __tablename__ = "beca"

    id = db.Column(db.Integer, primary_key=True)
    nombre_beca = db.Column(db.String(100), nullable=False)
    descripcion = db.Column(db.Text, nullable=True)
    
    becarios = db.relationship("Beca_Becario", back_populates="beca", cascade="all, delete-orphan")

    def serialize(self):
        return {
            "id": self.id,
            "nombre_beca": self.nombre_beca,
            "descripcion": self.descripcion
        }

    
class Beca_Becario(db.Model):
    __tablename__ = "beca_becario"
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    id_beca = db.Column(
        db.Integer,
        db.ForeignKey("beca.id")
    )

    id_becario = db.Column(
        db.Integer,
        db.ForeignKey("becario.id")
    )

    fecha_inicio = db.Column(db.Date, nullable=False)
    fecha_fin = db.Column(db.Date, nullable=True)
    monto_percibido = db.Column(db.Float, nullable=True)

    beca = db.relationship("Beca", back_populates="becarios")
    becario = db.relationship("Becario", back_populates="becas")