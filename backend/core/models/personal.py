from extension import db
from core.models.proyecto_investigacion import becario_proyecto, investigador_proyecto
from core.models.trabajo_reunion import investigador_x_trabajo_reunion
from core.models.trabajo_revista import investigador_x_trabajo_revista

# =====================================================
# PERSONAL
# =====================================================
class Personal(db.Model):
    __tablename__ = 'personal'

    id = db.Column(db.Integer, primary_key=True)
    nombre_apellido = db.Column(db.String(120), nullable=False)
    horas_semanales = db.Column(db.Integer, nullable=False)
    activo = db.Column(db.Boolean, default=True, nullable=False)

    tipo_personal_id = db.Column(db.Integer, db.ForeignKey('tipo_personal.id'), nullable=False)
    grupo_utn_id = db.Column(db.Integer, db.ForeignKey('grupo_utn.id'), nullable=False)

    tipo_personal = db.relationship('TipoPersonal', back_populates='personal')
    grupo_utn = db.relationship('GrupoInvestigacionUtn', back_populates='personal')
    

    def serialize(self):
        return {
            "id": self.id,
            "nombre_apellido": self.nombre_apellido,
            "horas_semanales": self.horas_semanales,
            "activo": self.activo,
            "tipo_personal_id": self.tipo_personal_id,
            "grupo_utn_id": self.grupo_utn_id,
            "tipo_personal_nombre": self.tipo_personal.nombre if self.tipo_personal else None,
            "grupo": self.grupo_utn.nombre_sigla_grupo if self.grupo_utn else None,
        }


# =====================================================
# BECARIO
# =====================================================
class Becario(db.Model):
    __tablename__ = 'becario'

    id = db.Column(db.Integer, primary_key=True)
    nombre_apellido = db.Column(db.String(120), nullable=False)
    horas_semanales = db.Column(db.Integer, nullable=False)
    activo = db.Column(db.Boolean, default=True, nullable=False)

    tipo_formacion_id = db.Column(
        db.Integer,
        db.ForeignKey('tipo_formacion_becario.id'),
        nullable=False
    )

    grupo_utn_id = db.Column(db.Integer, db.ForeignKey('grupo_utn.id'))
    fuente_financiamiento_id = db.Column(db.Integer, db.ForeignKey('fuente_financiamiento.id'))

    # --- Relaciones ---
    tipo_formacion = db.relationship(
        'TipoFormacion',
        back_populates='becarios'
    )

    grupo_utn = db.relationship(
        'GrupoInvestigacionUtn',
        back_populates='becarios'
    )

    fuente_financiamiento = db.relationship(
        'FuenteFinanciamiento',
        back_populates='becarios'
    )

    proyectos = db.relationship(
        'ProyectoInvestigacion',
        secondary=becario_proyecto,
        back_populates='becarios'
    )

    def serialize(self):
        return {
            "id": self.id,
            "nombre_apellido": self.nombre_apellido,
            "horas_semanales": self.horas_semanales,
            "activo": self.activo,

            "tipo_formacion_id": self.tipo_formacion_id,
            "fuente_financiamiento_id": self.fuente_financiamiento_id,
            "grupo_utn_id": self.grupo_utn_id,

            "tipo_formacion": self.tipo_formacion.nombre if self.tipo_formacion else None,
            "fuente_financiamiento": self.fuente_financiamiento.nombre if self.fuente_financiamiento else None,
            "grupo": self.grupo_utn.nombre_sigla_grupo if self.grupo_utn else None,

            "proyectos": [
                {
                    "id": p.id,
                    "codigo": p.codigo_proyecto,
                    "nombre": p.nombre_proyecto
                }
                for p in self.proyectos
            ]
        }


# =====================================================
# TIPO FORMACIÓN (🔥 CORREGIDO)
# =====================================================
class TipoFormacion(db.Model):
    __tablename__ = 'tipo_formacion_becario'

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)

    # 🔥 RELACIÓN QUE FALTABA
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
class Investigador(db.Model):
    __tablename__ = 'investigador'

    id = db.Column(db.Integer, primary_key=True)
    nombre_apellido = db.Column(db.String(120), nullable=False)
    horas_semanales = db.Column(db.Integer, nullable=False)
    activo = db.Column(db.Boolean, default=True, nullable=False)

    tipo_dedicacion_id = db.Column(db.Integer, db.ForeignKey('tipo_dedicacion.id'))
    categoria_utn_id = db.Column(db.Integer, db.ForeignKey('categoria_utn.id'), nullable=True)
    programa_incentivos_id = db.Column(db.Integer, db.ForeignKey('programa_incentivos_investigador.id'), nullable=True)
    grupo_utn_id = db.Column(db.Integer, db.ForeignKey('grupo_utn.id'), nullable=True)

    # --- Relaciones ---
    categoria_utn = db.relationship('CategoriaUtn', back_populates='investigadores')
    programa_incentivos = db.relationship('ProgramaIncentivos', back_populates='investigadores')
    grupo_utn = db.relationship('GrupoInvestigacionUtn', back_populates='investigadores')
    tipo_dedicacion = db.relationship('TipoDedicacion', back_populates='investigadores')

    trabajos_reunion_cientifica = db.relationship(
    'TrabajoReunionCientifica',
    secondary=investigador_x_trabajo_reunion,
    back_populates='investigadores'
    )

    actividades_docencia = db.relationship(
        'ActividadDocencia',
        back_populates='investigador',
        cascade='all, delete-orphan'
    )

    participaciones_relevantes = db.relationship(
        'ParticipacionRelevante',
        back_populates='investigador',
        cascade='all, delete-orphan'
    )

    trabajos_revistas = db.relationship(
        'TrabajosRevistasReferato',
        secondary=investigador_x_trabajo_revista,
        back_populates='investigadores'
    )


    proyectos = db.relationship(
        'ProyectoInvestigacion',
        secondary=investigador_proyecto,
        back_populates='investigadores'
    )

    def serialize(self):
        return {
            "id": self.id,
            "nombre_apellido": self.nombre_apellido,
            "horas_semanales": self.horas_semanales,
            "activo": self.activo,

            # 🔥 IDS
        "categoria_utn_id": self.categoria_utn_id,
        "programa_incentivos_id": self.programa_incentivos_id,
        "tipo_dedicacion_id": self.tipo_dedicacion_id,
        "grupo_utn_id": self.grupo_utn_id,

        # 🔥 NOMBRES
        "categoria_utn": self.categoria_utn.nombre if self.categoria_utn else None,
        "programa_incentivos": self.programa_incentivos.nombre if self.programa_incentivos else None,
        "tipo_dedicacion": self.tipo_dedicacion.nombre if self.tipo_dedicacion else None,
        "grupo": self.grupo_utn.nombre_sigla_grupo if self.grupo_utn else None,

            "proyectos": [
                {"id": p.id, "codigo": p.codigo_proyecto, "nombre": p.nombre_proyecto}
                for p in self.proyectos
            ],

            

            "participaciones_relevantes": [
                {"id": p.id, "evento": p.nombre_evento}
                for p in self.participaciones_relevantes
            ],

            "trabajos_reunion_cientifica": [
                {"id": t.id, "trabajo": t.titulo_trabajo}
                for t in self.trabajos_reunion_cientifica
            ]
        }

    