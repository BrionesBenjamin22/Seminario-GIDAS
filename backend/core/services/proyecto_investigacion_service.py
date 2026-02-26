from datetime import datetime
from extension import db
from sqlalchemy import func

from core.models.distinciones import DistincionRecibida
from core.models.proyecto_investigacion import (
    ProyectoInvestigacion,
    TipoProyecto,
    InvestigadorProyecto,
    BecarioProyecto
)
from core.models.grupo import GrupoInvestigacionUtn
from core.models.fuente_financiamiento import FuenteFinanciamiento
from core.models.programa_actividades import PlanificacionGrupo
from core.models.personal import Becario, Investigador


class ProyectoInvestigacionService:

    # =========================
    # GET ALL
    # =========================
    @staticmethod
    def get_all(filters: dict = None):

        query = ProyectoInvestigacion.query.filter(
            ProyectoInvestigacion.deleted_at.is_(None)
        )

        filters = filters or {}

        if filters.get("tipo_proyecto_id"):
            query = query.filter(
                ProyectoInvestigacion.tipo_proyecto_id == filters["tipo_proyecto_id"]
            )

        if filters.get("grupo_utn_id"):
            query = query.filter(
                ProyectoInvestigacion.grupo_utn_id == filters["grupo_utn_id"]
            )

        if filters.get("tiene_distinciones"):
            query = query.filter(
                ProyectoInvestigacion.distinciones.any(
                    DistincionRecibida.deleted_at.is_(None)
                )
            )

        orden = filters.get("orden")

        if orden == "asc":
            query = query.order_by(ProyectoInvestigacion.fecha_inicio.asc())
        elif orden == "monto_asc":
            query = query.order_by(ProyectoInvestigacion.monto_destinado.asc())
        elif orden == "monto_desc":
            query = query.order_by(ProyectoInvestigacion.monto_destinado.desc())
        else:
            query = query.order_by(ProyectoInvestigacion.fecha_inicio.desc())

        return [p.serialize() for p in query.all()]

    # =========================
    # GET BY ID
    # =========================
    @staticmethod
    def get_by_id(proyecto_id: int):

        proyecto = ProyectoInvestigacion.query.filter_by(
            id=proyecto_id,
            deleted_at=None
        ).first()

        if not proyecto:
            raise Exception("Proyecto de investigación no encontrado")

        return proyecto.serialize()

    # =========================
    # CREATE
    # =========================
    @staticmethod
    def create(data: dict):

        if not isinstance(data.get("codigo_proyecto"), int):
            raise ValueError("codigo_proyecto debe ser entero")

        fecha_inicio = datetime.strptime(
            data["fecha_inicio"], "%Y-%m-%d"
        ).date()

        fecha_fin = None
        if data.get("fecha_fin"):
            fecha_fin = datetime.strptime(
                data["fecha_fin"], "%Y-%m-%d"
            ).date()
            if fecha_fin < fecha_inicio:
                raise Exception("La fecha fin no puede ser anterior a la fecha inicio")

        if not TipoProyecto.query.get(data.get("tipo_proyecto_id")):
            raise Exception("Tipo de proyecto inválido")

        proyecto = ProyectoInvestigacion(
            codigo_proyecto=data["codigo_proyecto"],
            nombre_proyecto=data["nombre_proyecto"],
            descripcion_proyecto=data["descripcion_proyecto"],
            fecha_inicio=fecha_inicio,
            fecha_fin=fecha_fin,
            dificultades_proyecto=data.get("dificultades_proyecto"),
            monto_destinado=data.get("monto_destinado"),
            tipo_proyecto_id=data["tipo_proyecto_id"],
            grupo_utn_id=data.get("grupo_utn_id"),
            fuente_financiamiento_id=data.get("fuente_financiamiento_id"),
            planificacion_id=data.get("planificacion_id"),
        )

        db.session.add(proyecto)
        db.session.commit()

        return proyecto.serialize()

    # =========================
    # UPDATE
    # =========================
    @staticmethod
    def update(proyecto_id: int, data: dict):

        proyecto = ProyectoInvestigacion.query.filter_by(
            id=proyecto_id,
            deleted_at=None
        ).first()

        if not proyecto:
            raise Exception("Proyecto no encontrado")

        for field in [
            "codigo_proyecto",
            "nombre_proyecto",
            "descripcion_proyecto",
            "dificultades_proyecto",
            "monto_destinado"
        ]:
            if field in data:
                setattr(proyecto, field, data[field])

        if "fecha_inicio" in data:
            proyecto.fecha_inicio = datetime.strptime(
                data["fecha_inicio"], "%Y-%m-%d"
            ).date()

        if "fecha_fin" in data:
            proyecto.fecha_fin = (
                datetime.strptime(data["fecha_fin"], "%Y-%m-%d").date()
                if data["fecha_fin"]
                else None
            )

        if proyecto.fecha_fin and proyecto.fecha_fin < proyecto.fecha_inicio:
            raise Exception("La fecha fin no puede ser anterior a la fecha inicio")

        db.session.commit()
        return proyecto.serialize()

    # =========================
    # CERRAR PROYECTO
    # =========================
    @staticmethod
    def cerrar_proyecto(proyecto_id: int):

        proyecto = ProyectoInvestigacion.query.filter_by(
            id=proyecto_id,
            deleted_at=None
        ).first()

        if not proyecto:
            raise Exception("Proyecto no encontrado")

        proyecto.fecha_fin = func.current_date()
        db.session.commit()

        return {"message": "Proyecto cerrado correctamente"}

    # =====================================================
    # VINCULAR / DESVINCULAR INVESTIGADORES
    # =====================================================

    @staticmethod
    def vincular_investigadores_a_proyecto(proyecto_id, participaciones):

        proyecto = ProyectoInvestigacion.query.filter_by(
            id=proyecto_id,
            deleted_at=None
        ).first()

        if not proyecto:
            raise ValueError("Proyecto no encontrado.")

        for item in participaciones:

            investigador_id = item.get("id_investigador")

            existente = InvestigadorProyecto.query.filter_by(
                id_proyecto=proyecto_id,
                id_investigador=investigador_id,
                deleted_at=None
            ).first()

            if existente:
                raise ValueError("Ya existe participación activa.")

            nueva = InvestigadorProyecto(
                id_investigador=investigador_id,
                id_proyecto=proyecto_id,
                fecha_inicio=datetime.strptime(
                    item["fecha_inicio"], "%Y-%m-%d"
                ).date(),
                fecha_fin=datetime.strptime(
                    item["fecha_fin"], "%Y-%m-%d"
                ).date() if item.get("fecha_fin") else None
            )

            db.session.add(nueva)

        db.session.commit()
        return proyecto.serialize()

    @staticmethod
    def desvincular_investigadores_de_proyecto(proyecto_id, participaciones):

        proyecto = ProyectoInvestigacion.query.filter_by(
            id=proyecto_id,
            deleted_at=None
        ).first()

        if not proyecto:
            raise ValueError("Proyecto no encontrado.")

        for item in participaciones:

            participacion = InvestigadorProyecto.query.filter_by(
                id_proyecto=proyecto_id,
                id_investigador=item.get("id_investigador"),
                deleted_at=None
            ).first()

            if not participacion:
                raise ValueError("Participación activa no encontrada.")

            participacion.soft_delete(user_id=1)

        db.session.commit()
        return proyecto.serialize()

    # =====================================================
    # VINCULAR / DESVINCULAR BECARIOS
    # =====================================================

    @staticmethod
    def vincular_becarios_a_proyecto(proyecto_id, participaciones):

        proyecto = ProyectoInvestigacion.query.filter_by(
            id=proyecto_id,
            deleted_at=None
        ).first()

        if not proyecto:
            raise ValueError("Proyecto no encontrado.")

        for item in participaciones:

            becario_id = item.get("id_becario")

            existente = BecarioProyecto.query.filter_by(
                id_proyecto=proyecto_id,
                id_becario=becario_id,
                deleted_at=None
            ).first()

            if existente:
                raise ValueError("Ya existe participación activa.")

            nueva = BecarioProyecto(
                id_becario=becario_id,
                id_proyecto=proyecto_id,
                fecha_inicio=datetime.strptime(
                    item["fecha_inicio"], "%Y-%m-%d"
                ).date(),
                fecha_fin=datetime.strptime(
                    item["fecha_fin"], "%Y-%m-%d"
                ).date() if item.get("fecha_fin") else None
            )

            db.session.add(nueva)

        db.session.commit()
        return proyecto.serialize()

    @staticmethod
    def desvincular_becarios_de_proyecto(proyecto_id, participaciones):

        proyecto = ProyectoInvestigacion.query.filter_by(
            id=proyecto_id,
            deleted_at=None
        ).first()

        if not proyecto:
            raise ValueError("Proyecto no encontrado.")

        for item in participaciones:

            participacion = BecarioProyecto.query.filter_by(
                id_proyecto=proyecto_id,
                id_becario=item.get("id_becario"),
                deleted_at=None
            ).first()

            if not participacion:
                raise ValueError("Participación activa no encontrada.")

            participacion.soft_delete(user_id=1)

        db.session.commit()
        return proyecto.serialize()