from core.models.distinciones import DistincionRecibida
from extension import db
from datetime import datetime, date

class DistincionRecibidaService:

    @staticmethod
    def get_all(filters: dict = None):
        query = DistincionRecibida.query

        # ---- FILTRAR POR PROYECTO ----
        
        proyecto_id = filters.get("proyecto_id") if filters else None
        if proyecto_id:
            query = query.filter(
                DistincionRecibida.proyecto_investigacion_id == proyecto_id
            )

        # ---- ORDEN POR FECHA ----
        
        orden = filters.get("orden") if filters else None
        if orden == "asc":
            query = query.order_by(DistincionRecibida.fecha.asc())
        else:
            # default: descendente (más recientes primero)
            query = query.order_by(DistincionRecibida.fecha.desc())

        return [d.serialize() for d in query.all()]


    @staticmethod
    def get_by_id(distincion_id: int):
        dist = DistincionRecibida.query.get(distincion_id)
        if not dist:
            raise Exception("Distinción no encontrada")
        return dist.serialize()

    @staticmethod
    def create(data: dict):
        # --- Validar fecha ---
        try:
            fecha = datetime.strptime(data["fecha"], "%Y-%m-%d").date()
        except (KeyError, ValueError):
            raise Exception("La fecha es obligatoria y debe tener formato YYYY-MM-DD")

        # (opcional) no permitir fechas futuras
        if fecha > date.today():
            raise Exception("La fecha no puede ser futura")

        dist = DistincionRecibida(
            fecha=fecha,
            descripcion=data["descripcion"],
            proyecto_investigacion_id=data.get("proyecto_investigacion_id"),
        )

        db.session.add(dist)
        db.session.commit()
        return dist.serialize()

    @staticmethod
    def update(distincion_id: int, data: dict):
        dist = DistincionRecibida.query.get(distincion_id)
        if not dist:
            raise Exception("Distinción no encontrada")

        if "fecha" in data:
            try:
                fecha = datetime.strptime(data["fecha"], "%Y-%m-%d").date()
            except ValueError:
                raise Exception("La fecha debe tener formato YYYY-MM-DD")

            if fecha > date.today():
                raise Exception("La fecha no puede ser futura")

            dist.fecha = fecha

        if "descripcion" in data:
            dist.descripcion = data["descripcion"]

        if "proyecto_investigacion_id" in data:
            dist.proyecto_investigacion_id = data["proyecto_investigacion_id"]


        db.session.commit()
        return dist.serialize()

    @staticmethod
    def delete(distincion_id: int):
        dist = DistincionRecibida.query.get(distincion_id)
        if not dist:
            raise Exception("Distinción no encontrada")

        db.session.delete(dist)
        db.session.commit()
        return {"message": "Distinción eliminada correctamente"}
