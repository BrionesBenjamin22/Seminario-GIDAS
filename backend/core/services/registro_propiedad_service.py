from core.models.registro_patente import RegistrosPropiedad
from extension import db
from datetime import datetime


class RegistrosPropiedadService:

    # =========================
    # LISTAR
    # =========================
    @staticmethod
    def get_all(activos: str = "true"):
        query = RegistrosPropiedad.query

        if activos == "true":
            query = query.filter_by(activo=True)
        elif activos == "false":
            query = query.filter_by(activo=False)
        elif activos == "all":
            pass
        else:
            query = query.filter_by(activo=True)

        return [r.serialize() for r in query.all()]

    # =========================
    # OBTENER POR ID
    # =========================
    @staticmethod
    def get_by_id(registro_id: int):
        registro = RegistrosPropiedad.query.get(registro_id)
        if not registro:
            raise Exception("Registro de propiedad no encontrado")

        return registro.serialize()

    # =========================
    # CREAR
    # =========================
    @staticmethod
    def create(data: dict, user_id: int):
        try:
            fecha_registro = datetime.strptime(
                data["fecha_registro"], "%Y-%m-%d"
            ).date()
        except (KeyError, ValueError):
            raise ValueError(
                "fecha_registro es obligatoria y debe tener formato YYYY-MM-DD"
            )

        nuevo = RegistrosPropiedad(
            nombre_articulo=data["nombre_articulo"],
            organismo_registrante=data["organismo_registrante"],
            fecha_registro=fecha_registro,
            tipo_registro_id=data["tipo_registro_id"],
            grupo_utn_id=data["grupo_utn_id"],
            created_by=user_id,  # 🔥 auditoría
        )

        db.session.add(nuevo)
        db.session.commit()

        return nuevo.serialize()

    # =========================
    # ACTUALIZAR
    # =========================
    @staticmethod
    def update(registro_id: int, data: dict):
        registro = RegistrosPropiedad.query.get(registro_id)

        if not registro:
            raise Exception("Registro de propiedad no encontrado")

        if not registro.activo:
            raise ValueError(
                "No se puede modificar un registro eliminado. Restaúrelo primero."
            )

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

        if "fecha_registro" in data:
            try:
                registro.fecha_registro = datetime.strptime(
                    data["fecha_registro"], "%Y-%m-%d"
                ).date()
            except ValueError:
                raise ValueError("fecha_registro debe tener formato YYYY-MM-DD")

        db.session.commit()
        return registro.serialize()

    # =========================
    # SOFT DELETE
    # =========================
    @staticmethod
    def delete(registro_id: int, user_id: int):
        registro = RegistrosPropiedad.query.get(registro_id)

        if not registro:
            raise Exception("Registro de propiedad no encontrado")

        if not registro.activo:
            raise ValueError("El registro ya se encuentra eliminado.")

        registro.soft_delete(user_id)  # 🔥 usa el mixin
        db.session.commit()

        return {"message": "Registro eliminado correctamente (soft delete)"}

    # =========================
    # RESTORE
    # =========================
    @staticmethod
    def restore(registro_id: int):
        registro = RegistrosPropiedad.query.get(registro_id)

        if not registro:
            raise Exception("Registro de propiedad no encontrado")

        registro.restore()
        registro.activo = True

        db.session.commit()

        return registro.serialize()