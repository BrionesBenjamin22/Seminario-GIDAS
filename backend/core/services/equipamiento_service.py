from core.models.equipamiento import Equipamiento
from core.models.grupo import GrupoInvestigacionUtn
from extension import db
from datetime import datetime


class EquipamientoService:

    # ==========================================
    # HELPERS
    # ==========================================

    @staticmethod
    def _get_activo_or_404(equipamiento_id: int):
        equipamiento = db.session.get(Equipamiento, equipamiento_id)
        if not equipamiento or equipamiento.deleted_at is not None:
            raise Exception("Equipamiento no encontrado")
        return equipamiento


    # ==========================================
    # GET ALL
    # ==========================================

    @staticmethod
    def get_all():
        equipamientos = Equipamiento.query.filter(
            Equipamiento.deleted_at.is_(None)
        ).all()

        return [e.serialize() for e in equipamientos]


    # ==========================================
    # GET BY ID
    # ==========================================

    @staticmethod
    def get_by_id(equipamiento_id: int):
        equipamiento = EquipamientoService._get_activo_or_404(equipamiento_id)
        return equipamiento.serialize()


    # ==========================================
    # CREATE
    # ==========================================

    @staticmethod
    def create(data: dict, user_id: int):

        # --- Validaciones ---
        denominacion = data.get("denominacion")
        descripcion = data.get("descripcion_breve")
        monto = data.get("monto_invertido")
        fecha = data.get("fecha_incorporacion")
        grupo_id = data.get("grupo_utn_id")

        if not denominacion or not isinstance(denominacion, str):
            raise ValueError("La denominación es obligatoria.")

        if not descripcion or not isinstance(descripcion, str):
            raise ValueError("La descripción es obligatoria.")

        if not grupo_id:
            raise ValueError("El grupo es obligatorio.")

        grupo = db.session.get(GrupoInvestigacionUtn, grupo_id)
        if not grupo or grupo.deleted_at is not None:
            raise ValueError("Grupo no válido.")

        try:
            monto = float(monto)
        except (TypeError, ValueError):
            raise ValueError("El monto debe ser numérico.")

        if monto <= 0:
            raise ValueError("El monto debe ser mayor a 0.")

        try:
            fecha = datetime.strptime(fecha, "%Y-%m-%d").date()
        except:
            raise ValueError("Formato de fecha inválido. Usar YYYY-MM-DD.")

        equipamiento = Equipamiento(
            denominacion=denominacion.strip(),
            descripcion_breve=descripcion.strip(),
            fecha_incorporacion=fecha,
            monto_invertido=monto,
            grupo_utn_id=grupo_id,
            created_by=user_id
        )

        db.session.add(equipamiento)
        db.session.commit()

        return equipamiento.serialize()


    # ==========================================
    # UPDATE
    # ==========================================

    @staticmethod
    def update(equipamiento_id: int, data: dict):

        equipamiento = EquipamientoService._get_activo_or_404(equipamiento_id)

        if "denominacion" in data:
            equipamiento.denominacion = data["denominacion"].strip()

        if "descripcion_breve" in data:
            equipamiento.descripcion_breve = data["descripcion_breve"].strip()

        if "monto_invertido" in data:
            try:
                monto = float(data["monto_invertido"])
            except:
                raise ValueError("El monto debe ser numérico.")

            if monto <= 0:
                raise ValueError("El monto debe ser mayor a 0.")

            equipamiento.monto_invertido = monto

        if "fecha_incorporacion" in data:
            try:
                equipamiento.fecha_incorporacion = datetime.strptime(
                    data["fecha_incorporacion"], "%Y-%m-%d"
                ).date()
            except:
                raise ValueError("Formato de fecha inválido.")

        if "grupo_utn_id" in data:
            grupo = db.session.get(GrupoInvestigacionUtn, data["grupo_utn_id"])
            if not grupo or grupo.deleted_at is not None:
                raise ValueError("Grupo inválido.")

            equipamiento.grupo_utn_id = data["grupo_utn_id"]

        db.session.commit()

        return equipamiento.serialize()


    # ==========================================
    # SOFT DELETE
    # ==========================================

    @staticmethod
    def delete(equipamiento_id: int, user_id: int):

        equipamiento = EquipamientoService._get_activo_or_404(equipamiento_id)

        equipamiento.soft_delete(user_id)

        db.session.commit()

        return {"message": "Equipamiento eliminado correctamente"}