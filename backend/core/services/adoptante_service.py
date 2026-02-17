from core.models.transferencia_socio import Adoptante
from extension import db

class AdoptanteService:

    @staticmethod
    def get_all():
        return [a.serialize() for a in Adoptante.query.all()]

    @staticmethod
    def get_by_id(adoptante_id: int):
        adoptante = db.session.get(Adoptante, adoptante_id)
        if not adoptante:
            raise ValueError("Adoptante no encontrado.")
        return adoptante.serialize()

    @staticmethod
    def create(data: dict):
        if not data:
            raise ValueError("El body es obligatorio.")

        nombre = data.get("nombre")

        if not isinstance(nombre, str) or not nombre.strip():
            raise ValueError("El nombre es obligatorio y debe ser una cadena no vacía.")

        nombre = nombre.strip()

        # Opcional: evitar duplicados
        if db.session.query(Adoptante).filter_by(nombre=nombre).first():
            raise ValueError("Ya existe un adoptante con ese nombre.")

        adoptante = Adoptante(nombre=nombre)
        db.session.add(adoptante)
        db.session.commit()

        return adoptante.serialize()

    @staticmethod
    def update(adoptante_id: int, data: dict):
        if not data:
            raise ValueError("El body es obligatorio.")

        adoptante = db.session.get(Adoptante, adoptante_id)
        if not adoptante:
            raise ValueError("Adoptante no encontrado.")

        if "nombre" in data:
            nombre = data["nombre"]

            if not isinstance(nombre, str) or not nombre.strip():
                raise ValueError("El nombre debe ser una cadena no vacía.")

            adoptante.nombre = nombre.strip()

        db.session.commit()
        return adoptante.serialize()
