import datetime
from extension import db

autor_libro = db.Table('autorxlibro', 
                       db.Column('id_autor', db.Integer, db.ForeignKey('autor.id'), primary_key=True),
                       db.Column('id_libro', db.Integer, db.ForeignKey('documentacion_bibliografica.id'), primary_key=True)
)

class DocumentacionBibliografica(db.Model): #antes Documentacion. Ahora DocumentacionBibliografica
    __tablename__ = 'documentacion_bibliografica'
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.Text, nullable=False) 
    editorial = db.Column(db.Text, nullable=False) 
    anio = db.Column(db.Integer, nullable=False) 
    grupo_id = db.Column(db.Integer, db.ForeignKey('grupo_utn.id')) 
    fecha = db.Column(db.Date, default=datetime.datetime.utcnow, nullable=False)
    # --- Clave Foránea y Relación ---
    
    grupo_utn = db.relationship('GrupoInvestigacionUtn', back_populates='documentacion')
    autores = db.relationship("Autor", secondary=autor_libro, back_populates="libros")


    def serialize(self):
        data = {c.name: getattr(self, c.name) for c in self.__table__.columns}
        data["fecha"] = self.fecha.isoformat() if self.fecha else None
        data["grupo"] = self.grupo_utn.nombre_unidad_academica if self.grupo_utn else None
        data["autores"] = [
            {"id": a.id, "nombre_apellido": a.nombre_apellido}
            for a in self.autores
        ]
        return data

    
    
class Autor(db.Model):
    __tablename__ = 'autor'
    id = db.Column(db.Integer, primary_key=True)
    nombre_apellido = db.Column(db.Text, nullable=False)  
    libros = db.relationship("DocumentacionBibliografica", secondary=autor_libro, back_populates="autores")
    
    def serialize(self):
        data = {c.name: getattr(self, c.name) for c in self.__table__.columns}
        data["libros"] = [
            {"id": a.id, "titulo": a.titulo}
            for a in self.libros
        ]
        
        return data
        
        
