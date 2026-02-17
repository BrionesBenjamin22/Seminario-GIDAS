from sqlalchemy import func
from core.models.proyecto_investigacion import TipoProyecto
from extension import db

class TipoProyectoService:

    @staticmethod
    def get_all():
        tipos = TipoProyecto.query.order_by(TipoProyecto.nombre.asc()).all()
        return [
            {
                "id": t.id,
                "nombre": t.nombre
            } for t in tipos
        ]


    @staticmethod
    def get_by_id(tipo_id: int):
        tipo = TipoProyecto.query.get(tipo_id)
        if not tipo:
            raise Exception("Tipo de proyecto no encontrado")

        return {
            "id": tipo.id,
            "nombre": tipo.nombre
        }


    @staticmethod
    def create(data: dict):
        if not data or not data.get("nombre"):
            raise Exception("El nombre del tipo de proyecto es obligatorio")

        nombre = " ".join(data["nombre"].strip().split())

        # ---- VALIDAR DUPLICADO ----
        existente = TipoProyecto.query.filter(
            db.func.lower(TipoProyecto.nombre) == nombre.lower()
        ).first()

        if existente:
            raise Exception("Ya existe un tipo de proyecto con ese nombre")

        tipo = TipoProyecto(nombre=nombre)

        db.session.add(tipo)
        db.session.commit()

        return {
            "id": tipo.id,
            "nombre": tipo.nombre
        }


    @staticmethod
    def update(tipo_id: int, data: dict):
        tipo = TipoProyecto.query.get(tipo_id)
        if not tipo:
            raise Exception("Tipo de proyecto no encontrado")

        if "nombre" in data and data["nombre"]:
            nombre = " ".join(data["nombre"].strip().split())

            # ---- VALIDAR DUPLICADO (excluyendo el actual) ----
            existente = TipoProyecto.query.filter(
                func.lower(TipoProyecto.nombre) == nombre.lower(),
                TipoProyecto.id != tipo_id
            ).first()

            if existente:
                raise Exception("Ya existe un tipo de proyecto con ese nombre")

            tipo.nombre = nombre

        db.session.commit()
        return {
            "id": tipo.id,
            "nombre": tipo.nombre
        }

    @staticmethod
    def delete(tipo_id: int):
        tipo = TipoProyecto.query.get(tipo_id)
        if not tipo:
            raise Exception("Tipo de proyecto no encontrado")


        if tipo.proyectos_investigacion:
            raise Exception(
                "No se puede eliminar el tipo porque tiene proyectos asociados"
            )

        db.session.delete(tipo)
        db.session.commit()
        return {"message": "Tipo de proyecto eliminado correctamente"}
