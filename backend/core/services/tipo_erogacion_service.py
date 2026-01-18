from core.models.erogacion import TipoErogacion
from extension import db

class TipoErogacionService:

    @staticmethod
    def get_all():
        return [t.serialize() for t in TipoErogacion.query.all()]

    @staticmethod
    def get_by_id(tipo_id: int):
        tipo = TipoErogacion.query.get(tipo_id)
        if not tipo:
            raise Exception("Tipo de erogación no encontrado")
        return tipo.serialize()

    @staticmethod
    def create(data: dict):
        nombre_normalizado = data["nombre"].strip().lower()

        existe = TipoErogacion.query.filter(
            db.func.lower(TipoErogacion.nombre) == nombre_normalizado
        ).first()

        if existe:
            raise Exception("Ya existe un tipo de erogación con ese nombre")

        nuevo = TipoErogacion(
            nombre=data["nombre"].strip()
        )

        db.session.add(nuevo)
        db.session.commit()
        return nuevo.serialize()

    @staticmethod
    def update(tipo_id: int, data: dict):
        tipo = TipoErogacion.query.get(tipo_id)
        if not tipo:
            raise Exception("Tipo de erogación no encontrado")

        if "nombre" in data:
            nombre_normalizado = data["nombre"].strip().lower()

            existe = TipoErogacion.query.filter(
                db.func.lower(TipoErogacion.nombre) == nombre_normalizado,
                TipoErogacion.id != tipo_id
            ).first()

            if existe:
                raise Exception("Ya existe un tipo de erogación con ese nombre")

            tipo.nombre = data["nombre"].strip()

        db.session.commit()
        return tipo.serialize()


    @staticmethod
    def delete(tipo_id: int):
        tipo = TipoErogacion.query.get(tipo_id)
        if not tipo:
            raise Exception("Tipo de erogación no encontrado")

        db.session.delete(tipo)
        db.session.commit()
        return {"message": "Tipo de erogación eliminado correctamente"}
