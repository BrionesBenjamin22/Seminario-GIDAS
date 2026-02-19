from datetime import datetime
from core.models.transferencia_socio import Adoptante, TransferenciaSocioProductiva, TipoContrato
from core.models.grupo import GrupoInvestigacionUtn
from extension import db


class TransferenciaSocioProductivaService:

    # -------------------------------------------------
    # Validadores
    # -------------------------------------------------

    @staticmethod
    def _validar_texto(valor, campo, min_len=3):
        if valor is None:
            raise Exception(f"El campo '{campo}' es obligatorio")

        if not isinstance(valor, str):
            raise Exception(f"El campo '{campo}' debe ser texto")

        valor = valor.strip()

        if not valor:
            raise Exception(f"El campo '{campo}' no puede estar vacío")

        if len(valor) < min_len:
            raise Exception(
                f"El campo '{campo}' debe tener al menos {min_len} caracteres"
            )

        return valor

    @staticmethod
    def _validar_monto(monto):
        try:
            monto = float(monto)
        except (TypeError, ValueError):
            raise Exception("El monto debe ser numérico")

        if monto <= 0:
            raise Exception("El monto debe ser mayor a 0")

        return monto

    # -------------------------------------------------
    # CRUD
    # -------------------------------------------------

    @staticmethod
    def get_all(filters: dict = None):
        query = TransferenciaSocioProductiva.query

        grupo_utn_id = filters.get("grupo_utn_id") if filters else None
        if grupo_utn_id:
            query = query.filter(
                TransferenciaSocioProductiva.grupo_utn_id == grupo_utn_id
            )

        tipo_contrato_id = filters.get("tipo_contrato_id") if filters else None
        if tipo_contrato_id:
            query = query.filter(
                TransferenciaSocioProductiva.tipo_contrato_id == tipo_contrato_id
            )

        return [t.serialize() for t in query.all()]

    @staticmethod
    def get_by_id(transferencia_id):
        transferencia = TransferenciaSocioProductiva.query.get(transferencia_id)
        if not transferencia:
            raise Exception("Transferencia socio-productiva no encontrada")
        return transferencia.serialize()

    @staticmethod
    def create(data: dict):
    
        demandante = TransferenciaSocioProductivaService._validar_texto(
            data.get("demandante"), "demandante"
        )

        descripcion_actividad = TransferenciaSocioProductivaService._validar_texto(
            data.get("descripcion_actividad"), "descripcion_actividad", min_len=10
        )

        monto = TransferenciaSocioProductivaService._validar_monto(
            data.get("monto")
        )

        fecha_inicio = datetime.strptime(
            data["fecha_inicio"],
            "%Y-%m-%d"
        ).date()

        fecha_fin = None
        if data.get("fecha_fin"):
            fecha_fin = datetime.strptime(
                data["fecha_fin"],
                "%Y-%m-%d"
            ).date()
        
        # ---- Validar relaciones ----
        tipo_contrato_id = data.get("tipo_contrato_id")
        if not tipo_contrato_id or not TipoContrato.query.get(tipo_contrato_id):
            raise Exception("Tipo de contrato inválido")

        grupo_utn_id = data.get("grupo_utn_id")
        if not grupo_utn_id or not GrupoInvestigacionUtn.query.get(grupo_utn_id):
            raise Exception("Grupo UTN inválido")

        transferencia = TransferenciaSocioProductiva(
            demandante=demandante,
            descripcion_actividad=descripcion_actividad,
            monto=monto,
            fecha_inicio=fecha_inicio,
            fecha_fin=fecha_fin,
            tipo_contrato_id=tipo_contrato_id,
            grupo_utn_id=grupo_utn_id
        )

        db.session.add(transferencia)
        try:
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            print("Error:", str(e))
            raise Exception(f"Error real: {str(e)}")

        return transferencia.serialize()

    @staticmethod
    def update(transferencia_id, data: dict):
        transferencia = TransferenciaSocioProductiva.query.get(transferencia_id)
        if not transferencia:
            raise Exception("Transferencia socio-productiva no encontrada")


        if "demandante" in data:
            transferencia.demandante = TransferenciaSocioProductivaService._validar_texto(
                data["demandante"], "demandante"
            )

        if "descripcion_actividad" in data:
            transferencia.descripcion_actividad = (
                TransferenciaSocioProductivaService._validar_texto(
                    data["descripcion_actividad"],
                    "descripcion_actividad",
                    min_len=10
                )
            )

        if "monto" in data:
            transferencia.monto = TransferenciaSocioProductivaService._validar_monto(
                data["monto"]
            )

        if "fecha_inicio" in data:
            if not data["fecha_inicio"]:
                raise Exception("La fecha de inicio es obligatoria")
            transferencia.fecha_inicio = data["fecha_inicio"]
            
        if "fecha_fin" in data:
            transferencia.fecha_fin = data["fecha_fin"] if data["fecha_fin"] else None
        
        if "tipo_contrato_id" in data:
            if not TipoContrato.query.get(data["tipo_contrato_id"]):
                raise Exception("Tipo de contrato inválido")
            transferencia.tipo_contrato_id = data["tipo_contrato_id"]

        if "grupo_utn_id" in data:
            if not GrupoInvestigacionUtn.query.get(data["grupo_utn_id"]):
                raise Exception("Grupo UTN inválido")
            transferencia.grupo_utn_id = data["grupo_utn_id"]

        try:
            db.session.commit()
        except Exception:
            db.session.rollback()
            raise Exception("Error al actualizar la transferencia socio-productiva")

        return transferencia.serialize()

    @staticmethod
    def delete(transferencia_id):
        transferencia = TransferenciaSocioProductiva.query.get(transferencia_id)
        if not transferencia:
            raise Exception("Transferencia socio-productiva no encontrada")

        db.session.delete(transferencia)
        try:
            db.session.commit()
        except Exception:
            db.session.rollback()
            raise Exception("No se puede eliminar la transferencia socio-productiva")

        return {"message": "Transferencia socio-productiva eliminada correctamente"}
    
    @staticmethod
    def add_adoptantes(transferencia_id: int, adoptantes_ids: list[int]):
        if not isinstance(adoptantes_ids, list) or not adoptantes_ids:
            raise ValueError("adoptantes_ids debe ser una lista no vacía")

        transferencia = db.session.get(
            TransferenciaSocioProductiva,
            transferencia_id
        )

        if not transferencia:
            raise ValueError("Transferencia socio-productiva no encontrada")

        adoptantes = (
            db.session.query(Adoptante)
            .filter(Adoptante.id.in_(adoptantes_ids))
            .all()
        )

        if len(adoptantes) != len(adoptantes_ids):
            raise ValueError("Uno o más adoptantes no existen")

        for adoptante in adoptantes:
            if adoptante not in transferencia.adoptantes:
                transferencia.adoptantes.append(adoptante)

        db.session.commit()

        return transferencia.serialize()

    @staticmethod
    def remove_adoptantes(transferencia_id: int, adoptantes_ids: list[int]):
        if not isinstance(adoptantes_ids, list) or not adoptantes_ids:
            raise ValueError("adoptantes_ids debe ser una lista no vacía")
        transferencia = db.session.get(
            TransferenciaSocioProductiva,
            transferencia_id
        )

        if not transferencia:
            raise ValueError("Transferencia socio-productiva no encontrada")

        adoptantes = (
            db.session.query(Adoptante)
            .filter(Adoptante.id.in_(adoptantes_ids))
            .all()
        )

        if len(adoptantes) != len(adoptantes_ids):
            raise ValueError("Uno o más adoptantes no existen")

        for adoptante in adoptantes:
            if adoptante in transferencia.adoptantes:
                transferencia.adoptantes.remove(adoptante)

        db.session.commit()

        return transferencia.serialize()