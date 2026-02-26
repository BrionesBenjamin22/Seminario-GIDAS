from core.models.audit_mixin import AuditMixin
from extension import db
from core.models.trabajo_reunion import investigador_x_trabajo_reunion
from core.models.trabajo_revista import investigador_x_trabajo_revista

# =====================================================
# PERSONAL
# =====================================================
class Personal(db.Model, AuditMixin):
    __tablename__ = 'personal'

    id = db.Column(db.Integer, primary_key=True)
    nombre_apellido = db.Column(db.String(120), nullable=False)
    horas_semanales = db.Column(db.Integer, nullable=False)

    tipo_personal_id = db.Column(db.Integer, db.ForeignKey('tipo_personal.id'), nullable=False)
    grupo_utn_id = db.Column(db.Integer, db.ForeignKey('grupo_utn.id'), nullable=False)

    tipo_personal = db.relationship('TipoPersonal', back_populates='personal')
    grupo_utn = db.relationship('GrupoInvestigacionUtn', back_populates='personal')

    def serialize(self):
        data = self.to_dict()

        data.update({
            "tipo_personal": self.tipo_personal.nombre if self.tipo_personal else None,
            "grupo": self.grupo_utn.nombre_sigla_grupo if self.grupo_utn else None,
        })

        return data
    
# =====================================================
# BECARIO
# =====================================================
class Becario(db.Model, AuditMixin):
    __tablename__ = 'becario'

    id = db.Column(db.Integer, primary_key=True)
    nombre_apellido = db.Column(db.String(120), nullable=False)
    horas_semanales = db.Column(db.Integer, nullable=False)

    tipo_formacion_id = db.Column(
        db.Integer,
        db.ForeignKey('tipo_formacion_becario.id'),
        nullable=False
    )

    grupo_utn_id = db.Column(db.Integer, db.ForeignKey('grupo_utn.id'))
    fuente_financiamiento_id = db.Column(db.Integer, db.ForeignKey('fuente_financiamiento.id'))

    # Relaciones
    tipo_formacion = db.relationship('TipoFormacion', back_populates='becarios')
    grupo_utn = db.relationship('GrupoInvestigacionUtn', back_populates='becarios')
    fuente_financiamiento = db.relationship('FuenteFinanciamiento', back_populates='becarios')

    participaciones_proyecto = db.relationship(
        "BecarioProyecto",
        back_populates="becario",
        cascade="all, delete-orphan"
    )

    becas = db.relationship(
        "Beca_Becario",
        back_populates="becario",
        cascade="all, delete-orphan"
    )

    def serialize(self):
        data = self.to_dict()

        data.update({
            "tipo_formacion": self.tipo_formacion.nombre if self.tipo_formacion else None,
            "fuente_financiamiento": self.fuente_financiamiento.nombre if self.fuente_financiamiento else None,
            "grupo": self.grupo_utn.nombre_sigla_grupo if self.grupo_utn else None,
            "proyectos": [
                {
                    "id": p.proyecto.id,
                    "codigo": p.proyecto.codigo_proyecto,
                    "nombre": p.proyecto.nombre_proyecto,
                    "fecha_inicio": p.fecha_inicio.isoformat(),
                    "fecha_fin": p.fecha_fin.isoformat() if p.fecha_fin else None
                }
                for p in self.participaciones_proyecto
                if p.deleted_at is None
            ],
            "becas": [
                {
                    "id": b.beca.id,
                    "nombre_beca": b.beca.nombre_beca,
                    "descripcion": b.beca.descripcion,
                    "fecha_inicio": b.fecha_inicio.isoformat(),
                    "fecha_fin": b.fecha_fin.isoformat() if b.fecha_fin else None,
                    "monto_percibido": b.monto_percibido
                }
                for b in self.becas
                if b.deleted_at is None
            ]
        })

        return data


class TipoFormacion(db.Model):
    __tablename__ = 'tipo_formacion_becario'

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)

    becarios = db.relationship(
        'Becario',
        back_populates='tipo_formacion',
        lazy='select'
    )

    def serialize(self):
        return {
            "id": self.id,
            "nombre": self.nombre
        }


# =====================================================
# TIPO DEDICACIÓN
# =====================================================
class TipoDedicacion(db.Model):
    __tablename__ = 'tipo_dedicacion'

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)

    investigadores = db.relationship(
        'Investigador',
        back_populates='tipo_dedicacion',
        lazy='select'
    )

    def serialize(self):
        return {
            "id": self.id,
            "nombre": self.nombre
        }


# =====================================================
# INVESTIGADOR
# =====================================================
class Investigador(db.Model, AuditMixin):
    __tablename__ = 'investigador'

    id = db.Column(db.Integer, primary_key=True)
    nombre_apellido = db.Column(db.String(120), nullable=False)
    horas_semanales = db.Column(db.Integer, nullable=False)

    tipo_dedicacion_id = db.Column(db.Integer, db.ForeignKey('tipo_dedicacion.id'))
    categoria_utn_id = db.Column(db.Integer, db.ForeignKey('categoria_utn.id'), nullable=True)
    programa_incentivos_id = db.Column(db.Integer, db.ForeignKey('programa_incentivos_investigador.id'), nullable=True)
    grupo_utn_id = db.Column(db.Integer, db.ForeignKey('grupo_utn.id'), nullable=True)

    categoria_utn = db.relationship('CategoriaUtn', back_populates='investigadores')
    programa_incentivos = db.relationship('ProgramaIncentivos', back_populates='investigadores')
    grupo_utn = db.relationship('GrupoInvestigacionUtn', back_populates='investigadores')
    tipo_dedicacion = db.relationship('TipoDedicacion', back_populates='investigadores')

    participaciones_proyecto = db.relationship(
        "InvestigadorProyecto",
        back_populates="investigador",
        cascade="all, delete-orphan"
    )

    actividades_docencia = db.relationship(
    'ActividadDocencia',
    back_populates='investigador'
    )    
    
    participaciones_relevantes = db.relationship(
        "ParticipacionRelevante",
        back_populates="investigador",
        cascade="all, delete-orphan")

    trabajos_reunion_cientifica = db.relationship(
        'TrabajoReunionCientifica',
        secondary=investigador_x_trabajo_reunion,
        back_populates='investigadores'
    )
    
    trabajos_revistas = db.relationship(
        'TrabajosRevistasReferato',
        secondary=investigador_x_trabajo_revista,
        back_populates='investigadores'
    )

    def serialize(self):
        data = self.to_dict()

        data.update({
            "categoria_utn": self.categoria_utn.nombre if self.categoria_utn else None,
            "programa_incentivos": self.programa_incentivos.nombre if self.programa_incentivos else None,
            "tipo_dedicacion": self.tipo_dedicacion.nombre if self.tipo_dedicacion else None,
            "grupo": self.grupo_utn.nombre_sigla_grupo if self.grupo_utn else None,
            "proyectos": [
                {
                    "id": p.proyecto.id,
                    "codigo": p.proyecto.codigo_proyecto,
                    "nombre": p.proyecto.nombre_proyecto,
                    "fecha_inicio": p.fecha_inicio.isoformat(),
                    "fecha_fin": p.fecha_fin.isoformat() if p.fecha_fin else None
                }
                for p in self.participaciones_proyecto
                if p.deleted_at is None
            ]
        })

        return data