from core.models.personal import Investigador
from core.models.grupo import GrupoInvestigacionUtn
from core.models.proyecto_investigacion import ProyectoInvestigacion
from core.models.trabajo_revista import TrabajosRevistasReferato
from extension import db
from datetime import datetime

class TrabajosRevistasReferatoService:

    @staticmethod
    def get_all(filters: dict = None):
        query = TrabajosRevistasReferato.query
        filters = filters or {}

        # ---- FILTRAR POR PROYECTO ----
        if filters.get("proyecto_id"):
            query = query.filter(
                TrabajosRevistasReferato.proyecto_id == filters["proyecto_id"]
            )

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
            query = query.order_by(TrabajosRevistasReferato.id.asc())
        else:
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
        ]        
        for field in required_fields:
            if not data.get(field):
                raise Exception(f"El campo '{field}' es obligatorio")


        # ---- Validar grupo UTN (opcional) ----
        grupo_utn_id = data.get("grupo_utn_id")
        if grupo_utn_id:
            grupo = GrupoInvestigacionUtn.query.get(grupo_utn_id)
            if not grupo:
                raise Exception("Grupo UTN inválido")
            
        fecha = None
        if data.get("fecha"):
            fecha = datetime.strptime(
                data["fecha"], "%Y-%m-%d"
            ).date()

        trabajo = TrabajosRevistasReferato(
            titulo_trabajo=data["titulo_trabajo"],
            nombre_revista=data["nombre_revista"],
            editorial=data["editorial"],
            issn=data["issn"],
            fecha=fecha,
            pais=data["pais"],
            grupo_utn_id=grupo_utn_id,
            tipo_reunion_id=data["tipo_reunion_id"] 
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
            
        if "fecha" in data:
            trabajo.fecha = datetime.strptime(
                data["fecha"], "%Y-%m-%d"
            ).date()

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
    
    @staticmethod
    def vincular_investigadores(trabajo_id: int, investigadores_ids: list[int]):
        if not investigadores_ids or not isinstance(investigadores_ids, list):
            raise ValueError("Debe enviarse una lista de ids de investigadores")

        trabajo = db.session.get(TrabajosRevistasReferato, trabajo_id)
        if not trabajo:
            raise ValueError("Trabajo en revista no encontrado")

        # Traemos todos los investigadores que existan
        investigadores = (
            db.session.query(Investigador)
            .filter(Investigador.id.in_(investigadores_ids))
            .all()
        )

        if len(investigadores) != len(investigadores_ids):
            raise ValueError("Uno o más investigadores no existen")

        # Vinculamos solo los que no estén ya vinculados
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

        investigadores = (
            db.session.query(Investigador)
            .filter(Investigador.id.in_(investigadores_ids))
            .all()
        )

        for inv in investigadores:
            if inv in trabajo.investigadores:
                trabajo.investigadores.remove(inv)

        db.session.commit()

        return trabajo.serialize()
