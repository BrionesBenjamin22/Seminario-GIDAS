from core.models.transferencia_socio import TipoContrato
from extension import db
from sqlalchemy import func


class TipoContratoService:

    # -------------------------------------------------
    # Validadores
    # -------------------------------------------------

    @staticmethod
    def _validar_nombre(nombre, contrato_id=None):
        if nombre is None:
            raise Exception("El nombre es obligatorio")

        if not isinstance(nombre, str):
            raise Exception("El nombre debe ser texto")

        nombre = nombre.strip()

        if not nombre:
            raise Exception("El nombre no puede estar vacío")

        if len(nombre) < 2:
            raise Exception("El nombre debe tener al menos 2 caracteres")

        # Unicidad (case-insensitive)
        query = TipoContrato.query.filter(
            func.lower(TipoContrato.nombre) == nombre.lower()
        )

        if contrato_id:
            query = query.filter(TipoContrato.id != contrato_id)

        if query.first():
            raise Exception("Ya existe un tipo de contrato con ese nombre")

        return nombre

    # -------------------------------------------------
    # CRUD
    # -------------------------------------------------

    @staticmethod
    def get_all():
        return [
            t.serialize()
            for t in TipoContrato.query.order_by(TipoContrato.nombre.asc()).all()
        ]

    @staticmethod
    def get_by_id(tipo_contrato_id):
        tipo = TipoContrato.query.get(tipo_contrato_id)
        if not tipo:
            raise Exception("Tipo de contrato no encontrado")
        return tipo.serialize()

    @staticmethod
    def create(data: dict):
        nombre = TipoContratoService._validar_nombre(
            data.get("nombre")
        )

        tipo = TipoContrato(nombre=nombre)

        db.session.add(tipo)
        try:
            db.session.commit()
        except Exception:
            db.session.rollback()
            raise Exception("Error al guardar el tipo de contrato")

        return tipo.serialize()

    @staticmethod
    def update(tipo_contrato_id, data: dict):
        tipo = TipoContrato.query.get(tipo_contrato_id)
        if not tipo:
            raise Exception("Tipo de contrato no encontrado")

        if "nombre" in data:
            tipo.nombre = TipoContratoService._validar_nombre(
                data["nombre"],
                contrato_id=tipo.id
            )

        try:
            db.session.commit()
        except Exception:
            db.session.rollback()
            raise Exception("Error al actualizar el tipo de contrato")

        return tipo.serialize()

    @staticmethod
    def delete(tipo_contrato_id):
        tipo = TipoContrato.query.get(tipo_contrato_id)
        if not tipo:
            raise Exception("Tipo de contrato no encontrado")

        db.session.delete(tipo)
        try:
            db.session.commit()
        except Exception:
            db.session.rollback()
            raise Exception("No se puede eliminar el tipo de contrato")

        return {"message": "Tipo de contrato eliminado correctamente"}
