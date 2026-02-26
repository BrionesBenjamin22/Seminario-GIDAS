from core.models.personal import Investigador
from core.models.grupo import GrupoInvestigacionUtn
from core.models.trabajo_revista import TrabajosRevistasReferato
from core.models.trabajo_reunion import TipoReunion
from extension import db
from datetime import datetime
from sqlalchemy import func


class TrabajosRevistasReferatoService:

    # =================================================
    # GET ALL
    # =================================================
    @staticmethod
    def get_all(filters: dict = None):
        query = TrabajosRevistasReferato.query
        filters = filters or {}

        # 🔥 FILTRO ACTIVOS
        activos = filters.get("activos", "true")

        if activos == "true":
            query = query.filter(TrabajosRevistasReferato.deleted_at.is_(None))
        elif activos == "false":
            query = query.filter(TrabajosRevistasReferato.deleted_at.isnot(None))
        elif activos == "all":
            pass

        # ---- FILTRAR POR GRUPO ----
        if filters.get("grupo_utn_id"):
            query = query.filter(
                TrabajosRevistasReferato.grupo_utn_id == filters["grupo_utn_id"]
            )

        # ---- FILTRAR POR PAÍS ----
        if filters.get("pais"):
            query = query.filter(
                TrabajosRevistasReferato.pais.ilike(
                    f"%{filters['pais']}%"
                )
            )

        # ---- FILTRAR POR EDITORIAL ----
        if filters.get("editorial"):
            query = query.filter(
                TrabajosRevistasReferato.editorial.ilike(
                    f"%{filters['editorial']}%"
                )
            )

        # ---- ORDEN ----
        orden = filters.get("orden")
        if orden == "asc":
            query = query.order_by(TrabajosRevistasReferato.fecha.asc())
        else:
            query = query.order_by(TrabajosRevistasReferato.fecha.desc())

        return [t.serialize() for t in query.all()]


    # =================================================
    # GET BY ID
    # =================================================
    @staticmethod
    def get_by_id(trabajo_id: int):
        trabajo = db.session.get(TrabajosRevistasReferato, trabajo_id)

        if not trabajo:
            raise ValueError("Trabajo en revista no encontrado")

        return trabajo.serialize()


    # =================================================
    # CREATE
    # =================================================
    @staticmethod
    def create(data: dict, user_id: int):

        required_fields = [
            "titulo_trabajo",
            "nombre_revista",
            "editorial",
            "issn",
            "pais",
            "fecha",
            "tipo_reunion_id"
        ]

        for field in required_fields:
            if not data.get(field):
                raise ValueError(f"El campo '{field}' es obligatorio")

        # ---- Validar fecha ----
        try:
            fecha = datetime.strptime(
                data["fecha"], "%Y-%m-%d"
            ).date()
        except ValueError:
            raise ValueError("La fecha debe tener formato YYYY-MM-DD")

        # ---- Validar grupo ----
        grupo_utn_id = data.get("grupo_utn_id")
        if grupo_utn_id:
            if not GrupoInvestigacionUtn.query.get(grupo_utn_id):
                raise ValueError("Grupo UTN inválido")

        # ---- Validar tipo reunión ----
        if not TipoReunion.query.get(data["tipo_reunion_id"]):
            raise ValueError("Tipo de reunión inválido")

        trabajo = TrabajosRevistasReferato(
            titulo_trabajo=data["titulo_trabajo"].strip(),
            nombre_revista=data["nombre_revista"].strip(),
            editorial=data["editorial"].strip(),
            issn=data["issn"].strip(),
            fecha=fecha,
            pais=data["pais"].strip(),
            grupo_utn_id=grupo_utn_id,
            tipo_reunion_id=data["tipo_reunion_id"],
            created_by=user_id  # 🔥 auditoría
        )

        db.session.add(trabajo)
        db.session.commit()

        return trabajo.serialize()


    # =================================================
    # UPDATE
    # =================================================
    @staticmethod
    def update(trabajo_id: int, data: dict):

        trabajo = db.session.get(TrabajosRevistasReferato, trabajo_id)

        if not trabajo:
            raise ValueError("Trabajo en revista no encontrado")

        if trabajo.deleted_at is not None:
            raise ValueError("No se puede modificar un trabajo eliminado")

        for field in [
            "titulo_trabajo",
            "nombre_revista",
            "editorial",
            "issn",
            "pais"
        ]:
            if field in data:
                setattr(trabajo, field, data[field].strip())

        if "fecha" in data:
            trabajo.fecha = datetime.strptime(
                data["fecha"], "%Y-%m-%d"
            ).date()

        if "grupo_utn_id" in data:
            if data["grupo_utn_id"] is None:
                trabajo.grupo_utn_id = None
            else:
                if not GrupoInvestigacionUtn.query.get(data["grupo_utn_id"]):
                    raise ValueError("Grupo UTN inválido")
                trabajo.grupo_utn_id = data["grupo_utn_id"]

        db.session.commit()

        return trabajo.serialize()


    # =================================================
    # SOFT DELETE
    # =================================================
    @staticmethod
    def delete(trabajo_id: int, user_id: int):

        trabajo = db.session.get(TrabajosRevistasReferato, trabajo_id)

        if not trabajo:
            raise ValueError("Trabajo en revista no encontrado")

        if trabajo.deleted_at is not None:
            raise ValueError("El trabajo ya está eliminado")

        trabajo.soft_delete(user_id)

        db.session.commit()

        return {"message": "Trabajo eliminado correctamente (soft delete)"}


    # =================================================
    # RESTORE
    # =================================================
    @staticmethod
    def restore(trabajo_id: int):

        trabajo = db.session.get(TrabajosRevistasReferato, trabajo_id)

        if not trabajo:
            raise ValueError("Trabajo en revista no encontrado")

        trabajo.restore()
        trabajo.activo = True

        db.session.commit()

        return trabajo.serialize()


    # =================================================
    # VINCULAR INVESTIGADORES
    # =================================================
    @staticmethod
    def vincular_investigadores(trabajo_id: int, investigadores_ids: list[int]):

        trabajo = db.session.get(TrabajosRevistasReferato, trabajo_id)
        if not trabajo:
            raise ValueError("Trabajo en revista no encontrado")

        investigadores = (
            db.session.query(Investigador)
            .filter(
                Investigador.id.in_(investigadores_ids),
                Investigador.deleted_at.is_(None)
            )
            .all()
        )

        if len(investigadores) != len(investigadores_ids):
            raise ValueError("Uno o más investigadores no existen o están eliminados")

        for inv in investigadores:
            if inv not in trabajo.investigadores:
                trabajo.investigadores.append(inv)

        db.session.commit()

        return trabajo.serialize()


    @staticmethod
    def desvincular_investigadores(trabajo_id: int, investigadores_ids: list[int]):

        trabajo = db.session.get(TrabajosRevistasReferato, trabajo_id)
        if not trabajo:
            raise ValueError("Trabajo en revista no encontrado")

        for inv in trabajo.investigadores[:]:
            if inv.id in investigadores_ids:
                trabajo.investigadores.remove(inv)

        db.session.commit()

        return trabajo.serialize()