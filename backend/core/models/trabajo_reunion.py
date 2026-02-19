from extension import db

investigador_x_trabajo_reunion = db.Table(
    'investigador_x_trabajo_reunion',
    db.Column('investigador_id', db.Integer, db.ForeignKey('investigador.id'), primary_key=True),
    db.Column('trabajo_reunion_id', db.Integer, db.ForeignKey('trabajo_reunion_cientifica.id'), primary_key=True)
)


class TrabajoReunionCientifica(db.Model):
    __tablename__ = 'trabajo_reunion_cientifica'
    id = db.Column(db.Integer, primary_key=True)
    titulo_trabajo = db.Column(db.Text, nullable=False, unique=True)
    nombre_reunion = db.Column(db.Text, nullable=False)
    procedencia = db.Column(db.Text, nullable=False) # procedencia
    fecha_inicio = db.Column(db.Date, nullable=False)
    
    tipo_reunion_id = db.Column(db.Integer, db.ForeignKey('tipo_reunion_cientifica.id'), nullable=False)
    tipo_reunion_cientifica = db.relationship('TipoReunion', back_populates='trabajos_reunion_cientifica')
    
    # --- Clave Foránea y Relación ---
    investigadores = db.relationship(
        'Investigador',
        secondary=investigador_x_trabajo_reunion,
        back_populates='trabajos_reunion_cientifica'
    )

	
	# --- Relaciones (Muchos-a-Uno) ---
    grupo_utn_id = db.Column(db.Integer, db.ForeignKey('grupo_utn.id')) 
    grupo_utn = db.relationship('GrupoInvestigacionUtn', back_populates='trabajos_reunion_cientifica')
    
    def serialize(self):
        data = {c.name: getattr(self, c.name) for c in self.__table__.columns}
        data.pop("tipo_reunion_id", None)
        data.pop("grupo_utn_id", None)
        data["tipo_reunion"] = {
            "id": self.tipo_reunion_cientifica.id,
            "nombre": self.tipo_reunion_cientifica.nombre
        }
        data["investigadores"] = [
            {
                "id": inv.id,
                "nombre_apellido": inv.nombre_apellido
            } for inv in self.investigadores
        ]
        data["grupo_utn"] = self.grupo_utn.nombre_unidad_academica if self.grupo_utn else None
        return data
    
    
class TipoReunion(db.Model):
    __tablename__ = 'tipo_reunion_cientifica'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False, unique=True)

    trabajos_reunion_cientifica = db.relationship(
        'TrabajoReunionCientifica',
        back_populates='tipo_reunion_cientifica',
        lazy='select'
    )
    trabajos_revistas = db.relationship(
        'TrabajosRevistasReferato',
        back_populates='tipo_reunion',
        lazy='select'
    )
    
    visitas = db.relationship(
        'VisitaAcademica',
        back_populates='procedencia_visita',
        lazy='select'
    )

    def serialize(self):
        return {
            "id": self.id,
            "nombre": self.nombre
        }
        
