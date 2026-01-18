from extension import db

class DistincionRecibida(db.Model):
    __tablename__ = 'distincion_recibida'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    fecha = db.Column(db.Date, nullable=False)
    descripcion = db.Column(db.Text, nullable=False)

    # --- Claves Foráneas y Relaciones ---
    proyecto_investigacion_id = db.Column(db.Integer, db.ForeignKey('proyecto_investigacion.id'))

    proyecto_investigacion = db.relationship('ProyectoInvestigacion', back_populates='distinciones')

    def serialize(self):
        data = {c.name: getattr(self, c.name) for c in self.__table__.columns}
        data.pop("proyecto_investigacion_id")
        data["proyecto"] = {
            "id": self.proyecto_investigacion.id,
            "codigo": self.proyecto_investigacion.codigo_proyecto,
            "nombre": self.proyecto_investigacion.nombre_proyecto
        } if self.proyecto_investigacion else None

        return data