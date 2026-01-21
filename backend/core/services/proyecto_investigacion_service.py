from core.models.proyecto_investigacion import ProyectoInvestigacion, TipoProyecto
from core.models.grupo import GrupoInvestigacionUtn
from core.models.fuente_financiamiento import FuenteFinanciamiento
from core.models.programa_actividades import PlanificacionGrupo
from extension import db
from datetime import datetime, date


class ProyectoInvestigacionService:

    @staticmethod
    def get_all(filters: dict = None):
        query = ProyectoInvestigacion.query

        # ---- FILTROS ----
        if filters:
            if filters.get("tipo_proyecto_id"):
                query = query.filter(
                    ProyectoInvestigacion.tipo_proyecto_id == filters["tipo_proyecto_id"]
                )

            if filters.get("grupo_utn_id"):
                query = query.filter(
                    ProyectoInvestigacion.grupo_utn_id == filters["grupo_utn_id"]
                )

        # ---- ORDEN ----
        orden = filters.get("orden") if filters else None
        if orden == "asc":
            query = query.order_by(ProyectoInvestigacion.fecha_inicio.asc())
        else:
            query = query.order_by(ProyectoInvestigacion.fecha_inicio.desc())

        return [p.serialize() for p in query.all()]


    @staticmethod
    def get_by_id(proyecto_id: int):
        proyecto = ProyectoInvestigacion.query.get(proyecto_id)
        if not proyecto:
            raise Exception("Proyecto de investigación no encontrado")
        return proyecto.serialize()


    @staticmethod
    def create(data: dict):
        # ---- Validar fechas ----
        try:
            fecha_inicio = datetime.strptime(data["fecha_inicio"], "%Y-%m-%d").date()
            fecha_fin = datetime.strptime(data["fecha_fin"], "%Y-%m-%d").date()
        except (KeyError, ValueError):
            raise Exception("Las fechas son obligatorias y deben tener formato YYYY-MM-DD")

        if fecha_fin < fecha_inicio:
            raise Exception("La fecha fin no puede ser anterior a la fecha inicio")

        # ---- Validar tipo de proyecto ----
        tipo = TipoProyecto.query.get(data.get("tipo_proyecto_id"))
        if not tipo:
            raise Exception("Tipo de proyecto inválido")

        # ---- Validaciones opcionales ----
        if data.get("grupo_utn_id"):
            grupo = GrupoInvestigacionUtn.query.get(data["grupo_utn_id"])
            if not grupo:
                raise Exception("Grupo UTN inválido")
            
        if data.get("fuente_financiamiento_id"):
            fuente = FuenteFinanciamiento.query.get(data["fuente_financiamiento_id"])
            if not fuente:
                raise Exception("Fuente de financiamiento inválida")

        if data.get("planificacion_id"):
            planificacion = PlanificacionGrupo.query.get(data["planificacion_id"])
            if not planificacion:
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
            proyecto.fecha_fin = datetime.strptime(
                data["fecha_fin"], "%Y-%m-%d"
            ).date()

        if proyecto.fecha_fin < proyecto.fecha_inicio:
            raise Exception("La fecha fin no puede ser anterior a la fecha inicio")

        # ---- Tipo de proyecto ----
        if "tipo_proyecto_id" in data:
            if not TipoProyecto.query.get(data["tipo_proyecto_id"]):
                raise Exception("Tipo de proyecto inválido")
            proyecto.tipo_proyecto_id = data["tipo_proyecto_id"]

        # ---- Grupo UTN ----
        if "grupo_utn_id" in data:
            if data["grupo_utn_id"] is None:
                proyecto.grupo_utn_id = None
            else:
                grupo = GrupoInvestigacionUtn.query.get(data["grupo_utn_id"])
                if not grupo:
                    raise Exception("Grupo UTN inválido")
                proyecto.grupo_utn_id = data["grupo_utn_id"]

        # ---- Fuente de financiamiento ----
        if "fuente_financiamiento_id" in data:
            if data["fuente_financiamiento_id"] is None:
                proyecto.fuente_financiamiento_id = None
            else:
                fuente = FuenteFinanciamiento.query.get(data["fuente_financiamiento_id"])
                if not fuente:
                    raise Exception("Fuente de financiamiento inválida")
                proyecto.fuente_financiamiento_id = data["fuente_financiamiento_id"]

        
        if "planificacion_id" in data:
            if data["planificacion_id"] is None:
                proyecto.planificacion_id = None
            else:
                planificacion = PlanificacionGrupo.query.get(data["planificacion_id"])
                if not planificacion:
                    raise Exception("Planificación inválida")
                proyecto.planificacion_id = data["planificacion_id"]

        db.session.commit()
        return proyecto.serialize()


    @staticmethod
    def delete(proyecto_id: int):
        proyecto = ProyectoInvestigacion.query.get(proyecto_id)
        if not proyecto:
            raise Exception("Proyecto de investigación no encontrado")

        db.session.delete(proyecto)
        db.session.commit()
        return {"message": "Proyecto eliminado correctamente"}
