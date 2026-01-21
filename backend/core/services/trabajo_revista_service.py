from core.models.grupo import GrupoInvestigacionUtn
from core.models.proyecto_investigacion import ProyectoInvestigacion
from core.models.trabajo_revista import TrabajosRevistasReferato
from extension import db



class TrabajosRevistasReferatoService:

    @staticmethod
    def get_all(filters: dict = None):
        query = TrabajosRevistasReferato.query

        # ---- FILTRAR POR PROYECTO ----
        proyecto_id = filters.get("proyecto_id") if filters else None
        if proyecto_id:
            query = query.filter(
                TrabajosRevistasReferato.proyecto_id == proyecto_id
            )

        # ---- FILTRAR POR GRUPO ----
        grupo_utn_id = filters.get("grupo_utn_id") if filters else None
        if grupo_utn_id:
            query = query.filter(
                TrabajosRevistasReferato.grupo_utn_id == grupo_utn_id
            )

        # ---- ORDEN ----
        orden = filters.get("orden") if filters else None
        if orden == "asc":
            query = query.order_by(TrabajosRevistasReferato.id.asc())
        else:
            # default: descendente
            query = query.order_by(TrabajosRevistasReferato.id.desc())

        return [t.serialize() for t in query.all()]


    @staticmethod
    def get_by_id(trabajo_id: int):
        trabajo = TrabajosRevistasReferato.query.get(trabajo_id)
        if not trabajo:
            raise Exception("Trabajo en revista no encontrado")
        return trabajo.serialize()


    @staticmethod
    def create(data: dict):
        # ---- Validaciones obligatorias ----
        required_fields = [
            "titulo_trabajo",
            "nombre_revista",
            "editorial",
            "issn",
            "pais",
            "proyecto_id"
        ]

        for field in required_fields:
            if not data.get(field):
                raise Exception(f"El campo '{field}' es obligatorio")

        # ---- Validar proyecto ----
        proyecto = ProyectoInvestigacion.query.get(data["proyecto_id"])
        if not proyecto:
            raise Exception("Proyecto de investigación inválido")

        # ---- Validar grupo UTN (opcional) ----
        grupo_utn_id = data.get("grupo_utn_id")
        if grupo_utn_id:
            grupo = GrupoInvestigacionUtn.query.get(grupo_utn_id)
            if not grupo:
                raise Exception("Grupo UTN inválido")

        trabajo = TrabajosRevistasReferato(
            titulo_trabajo=data["titulo_trabajo"],
            nombre_revista=data["nombre_revista"],
            editorial=data["editorial"],
            issn=data["issn"],
            pais=data["pais"],
            proyecto_id=data["proyecto_id"],
            grupo_utn_id=grupo_utn_id
        )

        db.session.add(trabajo)
        db.session.commit()
        return trabajo.serialize()


    @staticmethod
    def update(trabajo_id: int, data: dict):
        trabajo = TrabajosRevistasReferato.query.get(trabajo_id)
        if not trabajo:
            raise Exception("Trabajo en revista no encontrado")

        if "titulo_trabajo" in data:
            trabajo.titulo_trabajo = data["titulo_trabajo"]

        if "nombre_revista" in data:
            trabajo.nombre_revista = data["nombre_revista"]

        if "editorial" in data:
            trabajo.editorial = data["editorial"]

        if "issn" in data:
            trabajo.issn = data["issn"]

        if "pais" in data:
            trabajo.pais = data["pais"]

        if "proyecto_id" in data:
            proyecto = ProyectoInvestigacion.query.get(data["proyecto_id"])
            if not proyecto:
                raise Exception("Proyecto de investigación inválido")
            trabajo.proyecto_id = data["proyecto_id"]

        if "grupo_utn_id" in data:
            if data["grupo_utn_id"] is None:
                trabajo.grupo_utn_id = None
            else:
                grupo = GrupoInvestigacionUtn.query.get(data["grupo_utn_id"])
                if not grupo:
                    raise Exception("Grupo UTN inválido")
                trabajo.grupo_utn_id = data["grupo_utn_id"]

        db.session.commit()
        return trabajo.serialize()


    @staticmethod
    def delete(trabajo_id: int):
        trabajo = TrabajosRevistasReferato.query.get(trabajo_id)
        if not trabajo:
            raise Exception("Trabajo en revista no encontrado")

        db.session.delete(trabajo)
        db.session.commit()
        return {"message": "Trabajo en revista eliminado correctamente"}
