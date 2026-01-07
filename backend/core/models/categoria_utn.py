from extension import db

class CategoriaUtn(db.Model):
    __tablename__ = 'categoria_utn'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.Text, nullable=False)
    
    investigadores = db.relationship('Investigador', back_populates='categoria_utn', lazy='dynamic')
    
    def serialize(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}  # type: ignore
