from extension import db
from core.models.directivos import Cargo
from sqlalchemy.exc import IntegrityError


class CargoService:

    @staticmethod
    def get_all():
        cargos = Cargo.query.all()
        return [c.serialize() for c in cargos]

    @staticmethod
    def get_by_id(cargo_id: int):
        cargo = Cargo.query.get(cargo_id)
        if not cargo:
            raise ValueError("Cargo no encontrado")
        return cargo.serialize()

    @staticmethod
    def create(data: dict):
        nombre = data.get("nombre")

        if not nombre:
            raise ValueError("El nombre es obligatorio")

        cargo = Cargo(nombre=nombre)

        db.session.add(cargo)
        db.session.commit()

        return cargo.serialize()

    @staticmethod
    def update(cargo_id: int, data: dict):
        cargo = Cargo.query.get(cargo_id)

        if not cargo:
            raise ValueError("Cargo no encontrado")

        nombre = data.get("nombre")
        if nombre:
            cargo.nombre = nombre

        db.session.commit()

        return cargo.serialize()

    @staticmethod
    def delete(cargo_id: int):
        cargo = Cargo.query.get(cargo_id)

        if not cargo:
            raise ValueError("Cargo no encontrado")

        db.session.delete(cargo)
        db.session.commit()

        return {"message": "Cargo eliminado correctamente"}