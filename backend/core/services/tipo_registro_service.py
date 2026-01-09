from core.models.registro_patente import TipoRegistroPropiedad
from extension import db

class TipoRegistroPropiedadService:

    @staticmethod
    def get_all():
        return [t.serialize() for t in TipoRegistroPropiedad.query.all()]

    @staticmethod
    def get_by_id(tipo_id: int):
        tipo = TipoRegistroPropiedad.query.get(tipo_id)
        if not tipo:
            raise Exception("Tipo de registro no encontrado")
        return tipo.serialize()

    @staticmethod
    def create(data: dict):
        nuevo = TipoRegistroPropiedad(
            nombre=data["nombre"]
        )
        db.session.add(nuevo)
        db.session.commit()
        return nuevo.serialize()

    @staticmethod
    def update(tipo_id: int, data: dict):
        tipo = TipoRegistroPropiedad.query.get(tipo_id)
        if not tipo:
            raise Exception("Tipo de registro no encontrado")

        tipo.nombre = data.get("nombre", tipo.nombre)

        db.session.commit()
        return tipo.serialize()

    @staticmethod
    def delete(tipo_id: int):
        tipo = TipoRegistroPropiedad.query.get(tipo_id)
        if not tipo:
            raise Exception("Tipo de registro no encontrado")

        db.session.delete(tipo)
        db.session.commit()
        return {"message": "Tipo de registro eliminado correctamente"}
