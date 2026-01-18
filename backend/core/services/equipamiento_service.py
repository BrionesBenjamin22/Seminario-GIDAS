from core.models.equipamiento import Equipamiento
from extension import db
from datetime import datetime

class EquipamientoService:

    @staticmethod
    def get_all():
        return [e.serialize() for e in Equipamiento.query.all()]

    @staticmethod
    def get_by_id(equipamiento_id: int):
        equipamiento = Equipamiento.query.get(equipamiento_id)
        if not equipamiento:
            raise Exception("Equipamiento no encontrado")
        return equipamiento.serialize()


    @staticmethod
    def create(data: dict):
        monto = data.get("monto_invertido")

        # --- Validaciones ---
        
        denominacion = data.get("denominacion")

        if not denominacion or not isinstance(denominacion, str):
            raise ValueError("La denominación es obligatoria.")

        denominacion = denominacion.strip()
        if not denominacion:
            raise ValueError("La denominación no puede estar vacía.")

        descripcion = data.get("descripcion_breve")
        
        if not descripcion or not isinstance(descripcion, str):
            raise ValueError("La descripción es obligatoria.")
        
        if descripcion.isdigit():
            raise ValueError("La descripción no puede ser solo un número.")

        descripcion = descripcion.strip()
        if not descripcion:
            raise ValueError("La descripción no puede estar vacía.")


        if monto is None:
            raise Exception("El monto invertido es obligatorio")

        try:
            monto = float(monto)
        except (TypeError, ValueError):
            raise Exception("El monto invertido debe ser numérico")

        if monto <= 0:
            raise Exception("El monto invertido debe ser mayor a 0")

        # --- Crear equipamiento ---
        equipamiento = Equipamiento(
            denominacion=denominacion,
            descripcion_breve=descripcion,
            fecha_incorporacion=datetime.strptime(
                data["fecha_incorporacion"], "%Y-%m-%d"
            ).date(),
            monto_invertido=monto,
            grupo_utn_id=data.get("grupo_utn_id")
        )

        db.session.add(equipamiento)
        db.session.commit()
        return equipamiento.serialize()


    @staticmethod
    def update(equipamiento_id: int, data: dict):
        equipamiento = Equipamiento.query.get(equipamiento_id)
        if not equipamiento:
            raise Exception("Equipamiento no encontrado")

        if "monto_invertido" in data:
            monto = data["monto_invertido"]

            try:
                monto = float(monto)
            except (TypeError, ValueError):
                raise Exception("El monto invertido debe ser numérico")

            if monto <= 0:
                raise Exception("El monto invertido debe ser mayor a 0")

            equipamiento.monto_invertido = monto

        # resto de campos...
        if "denominacion" in data:
            equipamiento.denominacion = data["denominacion"]

        if "descripcion_breve" in data:
            equipamiento.descripcion_breve = data["descripcion_breve"]

        if "fecha_incorporacion" in data:
            equipamiento.fecha_incorporacion = datetime.strptime(
                data["fecha_incorporacion"], "%Y-%m-%d"
            ).date()

        if "grupo_utn_id" in data:
            equipamiento.grupo_utn_id = data["grupo_utn_id"]

        db.session.commit()
        return equipamiento.serialize()


    @staticmethod
    def delete(equipamiento_id: int):
        equipamiento = Equipamiento.query.get(equipamiento_id)
        if not equipamiento:
            raise Exception("Equipamiento no encontrado")

        db.session.delete(equipamiento)
        db.session.commit()
        return {"message": "Equipamiento eliminado correctamente"}
