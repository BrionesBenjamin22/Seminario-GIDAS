from core.models.participacion_relevante import ParticipacionRelevante
from core.models.personal import Investigador
from extension import db
from datetime import datetime, date
from sqlalchemy import and_
import unicodedata

def normalizar_texto(texto: str) -> str:
    texto = texto.strip().lower()
    texto = unicodedata.normalize("NFD", texto)
    texto = "".join(c for c in texto if unicodedata.category(c) != "Mn")
    texto = " ".join(texto.split())
    return texto

class ParticipacionRelevanteService:

    @staticmethod
    def get_all(filters: dict = None):
        query = ParticipacionRelevante.query

        # ---- FILTRAR POR INVESTIGADOR ----
        investigador_id = filters.get("investigador_id") if filters else None
        if investigador_id:
            query = query.filter(
                ParticipacionRelevante.investigador_id == investigador_id
            )

        # ---- ORDEN POR FECHA ----
        orden = filters.get("orden") if filters else None
        if orden == "asc":
            query = query.order_by(ParticipacionRelevante.fecha.asc())
        else:
            query = query.order_by(ParticipacionRelevante.fecha.desc())

        return [p.serialize() for p in query.all()]


    @staticmethod
    def get_by_id(participacion_id: int):
        part = ParticipacionRelevante.query.get(participacion_id)
        if not part:
            raise Exception("Participación relevante no encontrada")
        return part.serialize()



    @staticmethod
    def create(data: dict):
        # ---- Validar fecha ----
        try:
            fecha = datetime.strptime(data["fecha"], "%Y-%m-%d").date()
        except (KeyError, ValueError):
            raise Exception("La fecha es obligatoria y debe tener formato YYYY-MM-DD")

        if fecha > date.today():
            raise Exception("La fecha no puede ser futura")

        # ---- Validar campos obligatorios ----
        for field in ["nombre_evento", "forma_participacion"]:
            if not data.get(field):
                raise Exception(f"El campo '{field}' es obligatorio")

        nombre_evento = normalizar_texto(data["nombre_evento"])

        # ---- Validar investigador ----
        investigador_id = data.get("investigador_id")
        if investigador_id:
            investigador = Investigador.query.get(investigador_id)
            if not investigador:
                raise Exception("Investigador inválido")

            # ---- Validar duplicado para el mismo investigador ----
            existente = ParticipacionRelevante.query.filter(
                and_(
                    ParticipacionRelevante.investigador_id == investigador_id,
                    ParticipacionRelevante.nombre_evento == nombre_evento
                )
            ).first()

            if existente:
                raise Exception(
                    "El investigador ya tiene una participación relevante en ese evento"
                )

        participacion = ParticipacionRelevante(
            nombre_evento=nombre_evento,
            forma_participacion=data["forma_participacion"],
            fecha=fecha,
            investigador_id=investigador_id
        )

        db.session.add(participacion)
        db.session.commit()
        return participacion.serialize()



    @staticmethod
    def update(participacion_id: int, data: dict):
        part = ParticipacionRelevante.query.get(participacion_id)
        if not part:
            raise Exception("Participación relevante no encontrada")

        if "nombre_evento" in data:
            nombre_evento = normalizar_texto(data["nombre_evento"])
        else:
            nombre_evento = part.nombre_evento

        investigador_id = (
            data["investigador_id"]
            if "investigador_id" in data
            else part.investigador_id
        )

        # ---- Validar investigador ----
        if investigador_id:
            investigador = Investigador.query.get(investigador_id)
            if not investigador:
                raise Exception("Investigador inválido")

            # ---- Validar duplicado para el mismo investigador ----
            existente = ParticipacionRelevante.query.filter(
                ParticipacionRelevante.investigador_id == investigador_id,
                ParticipacionRelevante.nombre_evento == nombre_evento,
                ParticipacionRelevante.id != participacion_id
            ).first()

            if existente:
                raise Exception(
                    "El investigador ya tiene una participación relevante en ese evento"
                )

        if "nombre_evento" in data:
            part.nombre_evento = nombre_evento

        if "forma_participacion" in data:
            part.forma_participacion = data["forma_participacion"]

        if "fecha" in data:
            fecha = datetime.strptime(data["fecha"], "%Y-%m-%d").date()
            if fecha > date.today():
                raise Exception("La fecha no puede ser futura")
            part.fecha = fecha

        if "investigador_id" in data:
            part.investigador_id = investigador_id

        db.session.commit()
        return part.serialize()


    @staticmethod
    def delete(participacion_id: int):
        part = ParticipacionRelevante.query.get(participacion_id)
        if not part:
            raise Exception("Participación relevante no encontrada")

        db.session.delete(part)
        db.session.commit()
        return {"message": "Participación relevante eliminada correctamente"}
