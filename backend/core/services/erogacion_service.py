from core.models.erogacion import Erogacion
from extension import db

class ErogacionService:

    @staticmethod
    def get_all():
        return [e.serialize() for e in Erogacion.query.all()]

    @staticmethod
    def get_by_id(erogacion_id: int):
        erogacion = Erogacion.query.get(erogacion_id)
        if not erogacion:
            raise Exception("Erogación no encontrada")
        return erogacion.serialize()

    @staticmethod
    def create(data: dict):
        erogacion = Erogacion(
            egresos=data["egresos"],
            ingresos=data["ingresos"],
            tipo_erogacion_id=data.get("tipo_erogacion_id"),
            fuente_financiamiento_id=data.get("fuente_financiamiento_id"),
            grupo_utn_id=data.get("grupo_utn_id")
        )

        db.session.add(erogacion)
        db.session.commit()
        return erogacion.serialize()

    @staticmethod
    def update(erogacion_id: int, data: dict):
        erogacion = Erogacion.query.get(erogacion_id)
        if not erogacion:
            raise Exception("Erogación no encontrada")

        erogacion.egresos = data.get("egresos", erogacion.egresos)
        erogacion.ingresos = data.get("ingresos", erogacion.ingresos)
        erogacion.tipo_erogacion_id = data.get(
            "tipo_erogacion_id",
            erogacion.tipo_erogacion_id
        )
        erogacion.fuente_financiamiento_id = data.get(
            "fuente_financiamiento_id",
            erogacion.fuente_financiamiento_id
        )
        erogacion.grupo_utn_id = data.get(
            "grupo_utn_id",
            erogacion.grupo_utn_id
        )

        db.session.commit()
        return erogacion.serialize()

    @staticmethod
    def delete(erogacion_id: int):
        erogacion = Erogacion.query.get(erogacion_id)
        if not erogacion:
            raise Exception("Erogación no encontrada")

        db.session.delete(erogacion)
        db.session.commit()
        return {"message": "Erogación eliminada correctamente"}
