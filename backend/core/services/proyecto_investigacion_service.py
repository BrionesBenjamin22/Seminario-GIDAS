from datetime import datetime
from extension import db

from core.models.proyecto_investigacion import ProyectoInvestigacion, TipoProyecto
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
        query = ProyectoInvestigacion.query

        if filters:
            if filters.get("tipo_proyecto_id"):
                query = query.filter(
                    ProyectoInvestigacion.tipo_proyecto_id == filters["tipo_proyecto_id"]
                )

            if filters.get("grupo_utn_id"):
                query = query.filter(
                    ProyectoInvestigacion.grupo_utn_id == filters["grupo_utn_id"]
                )

        orden = filters.get("orden") if filters else None
        if orden == "asc":
            query = query.order_by(ProyectoInvestigacion.fecha_inicio.asc())
        else:
            query = query.order_by(ProyectoInvestigacion.fecha_inicio.desc())

        return [p.serialize() for p in query.all()]

    # =========================
    # GET BY ID
    # =========================
    @staticmethod
    def get_by_id(proyecto_id: int):
        proyecto = ProyectoInvestigacion.query.get(proyecto_id)
        if not proyecto:
            raise Exception("Proyecto de investigación no encontrado")
        return proyecto.serialize()

    # =========================
    # CREATE
    # =========================
    @staticmethod
    def create(data: dict):
        # ---- Fecha inicio ----
        try:
            fecha_inicio = datetime.strptime(
                data["fecha_inicio"], "%Y-%m-%d"
            ).date()
        except (KeyError, ValueError):
            raise Exception("La fecha_inicio es obligatoria y debe tener formato YYYY-MM-DD")

        # ---- Fecha fin (opcional) ----
        fecha_fin = None
        if data.get("fecha_fin"):
            try:
                fecha_fin = datetime.strptime(
                    data["fecha_fin"], "%Y-%m-%d"
                ).date()
            except ValueError:
                raise Exception("La fecha_fin debe tener formato YYYY-MM-DD")

        if fecha_fin and fecha_fin < fecha_inicio:
            raise Exception("La fecha fin no puede ser anterior a la fecha inicio")

        # ---- Tipo de proyecto ----
        tipo = TipoProyecto.query.get(data.get("tipo_proyecto_id"))
        if not tipo:
            raise Exception("Tipo de proyecto inválido")

        # ---- Validaciones opcionales ----
        if data.get("grupo_utn_id"):
            if not GrupoInvestigacionUtn.query.get(data["grupo_utn_id"]):
                raise Exception("Grupo UTN inválido")

        if data.get("fuente_financiamiento_id"):
            if not FuenteFinanciamiento.query.get(data["fuente_financiamiento_id"]):
                raise Exception("Fuente de financiamiento inválida")

        if data.get("planificacion_id"):
            if not PlanificacionGrupo.query.get(data["planificacion_id"]):
                raise Exception("Planificación inválida")

        proyecto = ProyectoInvestigacion(
            codigo_proyecto=data["codigo_proyecto"],
            nombre_proyecto=data["nombre_proyecto"],
            descripcion_proyecto=data["descripcion_proyecto"],
            fecha_inicio=fecha_inicio,
            fecha_fin=fecha_fin,
            dificultades_proyecto=data.get("dificultades_proyecto"),
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
        proyecto = ProyectoInvestigacion.query.get(proyecto_id)
        if not proyecto:
            raise Exception("Proyecto de investigación no encontrado")

        for field in [
            "codigo_proyecto",
            "nombre_proyecto",
            "descripcion_proyecto",
            "dificultades_proyecto"
        ]:
            if field in data:
                setattr(proyecto, field, data[field])

        # ---- Fechas ----
        if "fecha_inicio" in data:
            proyecto.fecha_inicio = datetime.strptime(
                data["fecha_inicio"], "%Y-%m-%d"
            ).date()

        if "fecha_fin" in data:
            if data["fecha_fin"] is None:
                proyecto.fecha_fin = None
            else:
                proyecto.fecha_fin = datetime.strptime(
                    data["fecha_fin"], "%Y-%m-%d"
                ).date()

        if proyecto.fecha_fin and proyecto.fecha_fin < proyecto.fecha_inicio:
            raise Exception("La fecha fin no puede ser anterior a la fecha inicio")

        # ---- Tipo proyecto ----
        if "tipo_proyecto_id" in data:
            if not TipoProyecto.query.get(data["tipo_proyecto_id"]):
                raise Exception("Tipo de proyecto inválido")
            proyecto.tipo_proyecto_id = data["tipo_proyecto_id"]

        # ---- Grupo UTN ----
        if "grupo_utn_id" in data:
            if data["grupo_utn_id"] is None:
                proyecto.grupo_utn_id = None
            else:
                if not GrupoInvestigacionUtn.query.get(data["grupo_utn_id"]):
                    raise Exception("Grupo UTN inválido")
                proyecto.grupo_utn_id = data["grupo_utn_id"]

        # ---- Fuente financiamiento ----
        if "fuente_financiamiento_id" in data:
            if data["fuente_financiamiento_id"] is None:
                proyecto.fuente_financiamiento_id = None
            else:
                if not FuenteFinanciamiento.query.get(data["fuente_financiamiento_id"]):
                    raise Exception("Fuente de financiamiento inválida")
                proyecto.fuente_financiamiento_id = data["fuente_financiamiento_id"]

        # ---- Planificación ----
        if "planificacion_id" in data:
            if data["planificacion_id"] is None:
                proyecto.planificacion_id = None
            else:
                if not PlanificacionGrupo.query.get(data["planificacion_id"]):
                    raise Exception("Planificación inválida")
                proyecto.planificacion_id = data["planificacion_id"]

        db.session.commit()
        return proyecto.serialize()

    # =========================
    # DELETE
    # =========================
    @staticmethod
    def delete(proyecto_id: int):
        proyecto = ProyectoInvestigacion.query.get(proyecto_id)
        if not proyecto:
            raise Exception("Proyecto de investigación no encontrado")

        db.session.delete(proyecto)
        db.session.commit()
        return {"message": "Proyecto eliminado correctamente"}

    # =========================
    # VINCULAR / DESVINCULAR BECARIOS
    # =========================
    @staticmethod
    def vincular_becarios_a_proyecto(proyecto_id, becarios_ids):
        if proyecto_id is None:
            raise ValueError("El id del proyecto es obligatorio.")

        if not isinstance(becarios_ids, list) or not becarios_ids:
            raise ValueError("Debe enviarse una lista de ids de becarios.")

        proyecto = ProyectoInvestigacion.query.get(proyecto_id)
        if not proyecto:
            raise ValueError("Proyecto no encontrado.")

        becarios = Becario.query.filter(Becario.id.in_(becarios_ids)).all()
        if not becarios:
            raise ValueError("No se encontraron becarios válidos.")

        for becario in becarios:
            if becario not in proyecto.becarios:
                proyecto.becarios.append(becario)

        db.session.commit()
        return proyecto.serialize()

    @staticmethod
    def desvincular_becarios_de_proyecto(proyecto_id, becarios_ids):
        if proyecto_id is None:
            raise ValueError("El id del proyecto es obligatorio.")

        if not isinstance(becarios_ids, list) or not becarios_ids:
            raise ValueError("Debe enviarse una lista de ids de becarios.")

        proyecto = ProyectoInvestigacion.query.get(proyecto_id)
        if not proyecto:
            raise ValueError("Proyecto no encontrado.")

        becarios = Becario.query.filter(Becario.id.in_(becarios_ids)).all()
        if not becarios:
            raise ValueError("No se encontraron becarios válidos.")

        for becario in becarios:
            if becario in proyecto.becarios:
                proyecto.becarios.remove(becario)

        db.session.commit()
        return proyecto.serialize()

    # =========================
    # VINCULAR / DESVINCULAR INVESTIGADORES
    # =========================
    @staticmethod
    def vincular_investigadores_a_proyecto(proyecto_id, investigadores_ids):
        if proyecto_id is None:
            raise ValueError("El id del proyecto es obligatorio.")

        if not isinstance(investigadores_ids, list) or not investigadores_ids:
            raise ValueError("Debe enviarse una lista de ids de investigadores.")

        proyecto = ProyectoInvestigacion.query.get(proyecto_id)
        if not proyecto:
            raise ValueError("Proyecto no encontrado.")

        investigadores = Investigador.query.filter(
            Investigador.id.in_(investigadores_ids)
        ).all()

        if not investigadores:
            raise ValueError("No se encontraron investigadores válidos.")

        for investigador in investigadores:
            if investigador not in proyecto.investigadores:
                proyecto.investigadores.append(investigador)

        db.session.commit()
        return proyecto.serialize()

    @staticmethod
    def desvincular_investigadores_de_proyecto(proyecto_id, investigadores_ids):
        if proyecto_id is None:
            raise ValueError("El id del proyecto es obligatorio.")

        if not isinstance(investigadores_ids, list) or not investigadores_ids:
            raise ValueError("Debe enviarse una lista de ids de investigadores.")

        proyecto = ProyectoInvestigacion.query.get(proyecto_id)
        if not proyecto:
            raise ValueError("Proyecto no encontrado.")

        investigadores = Investigador.query.filter(
            Investigador.id.in_(investigadores_ids)
        ).all()

        if not investigadores:
            raise ValueError("No se encontraron investigadores válidos.")

        for investigador in investigadores:
            if investigador in proyecto.investigadores:
                proyecto.investigadores.remove(investigador)

        db.session.commit()
        return proyecto.serialize()

