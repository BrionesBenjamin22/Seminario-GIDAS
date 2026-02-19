from datetime import datetime
from extension import db

from core.models.proyecto_investigacion import ProyectoInvestigacion, TipoProyecto, InvestigadorProyecto, BecarioProyecto
from core.models.grupo import GrupoInvestigacionUtn
from core.models.fuente_financiamiento import FuenteFinanciamiento
from core.models.programa_actividades import PlanificacionGrupo
from core.models.personal import Becario, Investigador
from sqlalchemy import func


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
        codigo = data.get("codigo_proyecto")
        if not codigo or not isinstance(codigo, int):
            raise ValueError("El campo 'codigo_proyecto' es obligatorio y debe ser un número entero")
        
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
    def cerrar_proyecto(proyecto_id: int):
        proyecto = ProyectoInvestigacion.query.get(proyecto_id)
        if not proyecto:
            raise Exception("Proyecto de investigación no encontrado")

        proyecto.fecha_fin = func.current_date()  # Cierra el proyecto al día de hoy
        db.session.commit()
        return {"message": "Proyecto cerrado correctamente"}
    # =========================
    # VINCULAR / DESVINCULAR BECARIOS
    # =========================
    @staticmethod
    def vincular_becarios_a_proyecto(proyecto_id, participaciones):

        if not isinstance(participaciones, list) or not participaciones:
            raise ValueError("Debe enviarse una lista de participaciones.")

        proyecto = ProyectoInvestigacion.query.get(proyecto_id)
        if not proyecto:
            raise ValueError("Proyecto no encontrado.")

        for item in participaciones:

            becario_id = item.get("id_becario")
            if not becario_id:
                raise ValueError("id_becario es obligatorio.")

            becario = Becario.query.get(becario_id)
            if not becario:
                raise ValueError(f"Becario {becario_id} no encontrado.")

            # Validar fechas
            try:
                fecha_inicio = datetime.strptime(
                    item["fecha_inicio"], "%Y-%m-%d"
                ).date()
            except Exception:
                raise ValueError("fecha_inicio debe tener formato YYYY-MM-DD")

            fecha_fin = None
            if item.get("fecha_fin"):
                fecha_fin = datetime.strptime(
                    item["fecha_fin"], "%Y-%m-%d"
                ).date()

                if fecha_fin < fecha_inicio:
                    raise ValueError("fecha_fin no puede ser anterior a fecha_inicio")

            # Verificar que no exista ya
            existente = BecarioProyecto.query.filter_by(
                id_proyecto=proyecto_id,
                id_becario=becario_id
            ).first()

            if existente:
                continue  # Evita duplicado

            nueva_participacion = BecarioProyecto(
                id_becario=becario_id,
                id_proyecto=proyecto_id,
                fecha_inicio=fecha_inicio,
                fecha_fin=fecha_fin
            )

            db.session.add(nueva_participacion)

        db.session.commit()
        return proyecto.serialize()



    @staticmethod
    def desvincular_becarios_de_proyecto(proyecto_id, participaciones):
        """
        participaciones:
        [
            {
                "id_becario": 3,
                "fecha_fin": "2024-10-15"
            }
        ]
        """

        if not isinstance(participaciones, list) or not participaciones:
            raise ValueError("Debe enviarse una lista no vacía de participaciones.")

        proyecto = ProyectoInvestigacion.query.get(proyecto_id)
        if not proyecto:
            raise ValueError("Proyecto no encontrado.")

        for item in participaciones:

            becario_id = item.get("id_becario")
            fecha_fin_str = item.get("fecha_fin")

            if not becario_id or not fecha_fin_str:
                raise ValueError("id_becario y fecha_fin son obligatorios.")

            try:
                fecha_fin = datetime.strptime(fecha_fin_str, "%Y-%m-%d").date()
            except ValueError:
                raise ValueError("fecha_fin debe tener formato YYYY-MM-DD.")

            participacion = BecarioProyecto.query.filter_by(
                id_proyecto=proyecto_id,
                id_becario=becario_id
            ).first()

            if not participacion:
                raise ValueError(
                    f"No existe participación activa para becario {becario_id}"
                )

            if fecha_fin < participacion.fecha_inicio:
                raise ValueError("La fecha_fin no puede ser anterior a fecha_inicio.")

            participacion.fecha_fin = fecha_fin

        db.session.commit()

        return proyecto.serialize()


    # =========================
    # VINCULAR / DESVINCULAR INVESTIGADORES
    # =========================
    @staticmethod
    def vincular_investigadores_a_proyecto(proyecto_id, participaciones):

        if not isinstance(participaciones, list) or not participaciones:
            raise ValueError("Debe enviarse una lista de participaciones.")

        proyecto = ProyectoInvestigacion.query.get(proyecto_id)
        if not proyecto:
            raise ValueError("Proyecto no encontrado.")

        for item in participaciones:

            investigador_id = item.get("id_investigador")
            if not investigador_id:
                raise ValueError("id_investigador es obligatorio.")

            investigador = Investigador.query.get(investigador_id)
            if not investigador:
                raise ValueError(f"Investigador {investigador_id} no encontrado.")

            try:
                fecha_inicio = datetime.strptime(
                    item["fecha_inicio"], "%Y-%m-%d"
                ).date()
            except Exception:
                raise ValueError("fecha_inicio debe tener formato YYYY-MM-DD")

            fecha_fin = None
            if item.get("fecha_fin"):
                fecha_fin = datetime.strptime(
                    item["fecha_fin"], "%Y-%m-%d"
                ).date()

                if fecha_fin < fecha_inicio:
                    raise ValueError("fecha_fin no puede ser anterior a fecha_inicio")

            existente = InvestigadorProyecto.query.filter_by(
                id_proyecto=proyecto_id,
                id_investigador=investigador_id
            ).first()

            if existente:
                continue

            nueva_participacion = InvestigadorProyecto(
                id_investigador=investigador_id,
                id_proyecto=proyecto_id,
                fecha_inicio=fecha_inicio,
                fecha_fin=fecha_fin
            )

            db.session.add(nueva_participacion)

        db.session.commit()
        return proyecto.serialize()



    @staticmethod
    def desvincular_investigadores_de_proyecto(proyecto_id, participaciones):
        """
        participaciones:
        [
            {
                "id_investigador": 1,
                "fecha_fin": "2024-09-30"
            }
        ]
        """

        if not isinstance(participaciones, list) or not participaciones:
            raise ValueError("Debe enviarse una lista no vacía de participaciones.")

        proyecto = ProyectoInvestigacion.query.get(proyecto_id)
        if not proyecto:
            raise ValueError("Proyecto no encontrado.")

        for item in participaciones:

            investigador_id = item.get("id_investigador")
            fecha_fin_str = item.get("fecha_fin")

            if not investigador_id or not fecha_fin_str:
                raise ValueError("id_investigador y fecha_fin son obligatorios.")

            try:
                fecha_fin = datetime.strptime(fecha_fin_str, "%Y-%m-%d").date()
            except ValueError:
                raise ValueError("fecha_fin debe tener formato YYYY-MM-DD.")

            participacion = InvestigadorProyecto.query.filter_by(
                id_proyecto=proyecto_id,
                id_investigador=investigador_id
            ).first()

            if not participacion:
                raise ValueError(
                    f"No existe participación activa para investigador con id: {investigador_id}"
                )

            if fecha_fin < participacion.fecha_inicio:
                raise ValueError("La fecha_fin no puede ser anterior a fecha_inicio.")

            participacion.fecha_fin = fecha_fin

        db.session.commit()

        return proyecto.serialize()




