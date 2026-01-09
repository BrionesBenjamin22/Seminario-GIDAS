from core.models.registro_patente import RegistrosPropiedad
from extension import db

class RegistrosPropiedadService:

    @staticmethod
    def get_all():
        return [r.serialize() for r in RegistrosPropiedad.query.all()]

    @staticmethod
    def get_by_id(registro_id: int):
        registro = RegistrosPropiedad.query.get(registro_id)
        if not registro:
            raise Exception("Registro de propiedad no encontrado")
        return registro.serialize()

    @staticmethod
    def create(data: dict):
        nuevo = RegistrosPropiedad(
            nombre_articulo=data["nombre_articulo"],
            organismo_registrante=data["organismo_registrante"],
            tipo_registro_id=data["tipo_registro_id"],
            grupo_utn_id=data["grupo_utn_id"]
        )

        db.session.add(nuevo)
        db.session.commit()
        return nuevo.serialize()

    @staticmethod
    def update(registro_id: int, data: dict):
        registro = RegistrosPropiedad.query.get(registro_id)
        if not registro:
            raise Exception("Registro de propiedad no encontrado")

        registro.nombre_articulo = data.get(
            "nombre_articulo", registro.nombre_articulo
        )
        registro.organismo_registrante = data.get(
            "organismo_registrante", registro.organismo_registrante
        )
        registro.tipo_registro_id = data.get(
            "tipo_registro_id", registro.tipo_registro_id
        )
        registro.grupo_utn_id = data.get(
            "grupo_utn_id", registro.grupo_utn_id
        )

        db.session.commit()
        return registro.serialize()

    @staticmethod
    def delete(registro_id: int):
        registro = RegistrosPropiedad.query.get(registro_id)
        if not registro:
            raise Exception("Registro de propiedad no encontrado")

        db.session.delete(registro)
        db.session.commit()
        return {"message": "Registro de propiedad eliminado correctamente"}
