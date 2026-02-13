from core.models.erogacion import Erogacion, TipoErogacion
from core.models.fuente_financiamiento import FuenteFinanciamiento
from core.models.grupo import GrupoInvestigacionUtn
from extension import db


class ErogacionService:

    # =========================
    # GET ALL (con filtros y orden)
    # =========================
    @staticmethod
    def get_all(filters: dict = None):
        query = Erogacion.query

        if filters:
            # ---- FILTROS ----
            if filters.get("fuente_financiamiento_id"):
                query = query.filter(
                    Erogacion.fuente_financiamiento_id == filters["fuente_financiamiento_id"]
                )

            if filters.get("tipo_erogacion_id"):
                query = query.filter(
                    Erogacion.tipo_erogacion_id == filters["tipo_erogacion_id"]
                )

            # ---- ORDEN ----
            if filters.get("orden_ingresos") == "asc":
                query = query.order_by(Erogacion.ingresos.asc())
            elif filters.get("orden_ingresos") == "desc":
                query = query.order_by(Erogacion.ingresos.desc())

            if filters.get("orden_egresos") == "asc":
                query = query.order_by(Erogacion.egresos.asc())
            elif filters.get("orden_egresos") == "desc":
                query = query.order_by(Erogacion.egresos.desc())

        return [e.serialize() for e in query.all()]

    # =========================
    # GET BY ID
    # =========================
    @staticmethod
    def get_by_id(erogacion_id: int):
        erogacion = Erogacion.query.get(erogacion_id)
        if not erogacion:
            raise Exception("Erogación no encontrada")
        return erogacion.serialize()


    

    @staticmethod
    def create(data: dict):
        if not data:
            raise Exception("El body es obligatorio")

        # ---- egresos ----
        if "egresos" not in data:
            raise Exception("El campo 'egresos' es obligatorio")

        try:
            egresos = float(data["egresos"])
        except (TypeError, ValueError):
            raise Exception("El campo 'egresos' debe ser numérico")

        if egresos < 0:
            raise Exception("El campo 'egresos' no puede ser negativo")

        # ---- ingresos ----
        if "ingresos" not in data:
            raise Exception("El campo 'ingresos' es obligatorio")

        try:
            ingresos = float(data["ingresos"])
        except (TypeError, ValueError):
            raise Exception("El campo 'ingresos' debe ser numérico")

        if ingresos < 0:
            raise Exception("El campo 'ingresos' no puede ser negativo")

        # ---- al menos uno distinto de 0 ----
        if egresos == 0 and ingresos == 0:
            raise Exception("Egresos e ingresos no pueden ser ambos 0")

        # ---- tipo erogación ----
        if data.get("tipo_erogacion_id"):
            if not TipoErogacion.query.get(data["tipo_erogacion_id"]):
                raise Exception("Tipo de erogación inválido")

        # ---- fuente financiamiento ----
        if data.get("fuente_financiamiento_id"):
            if not FuenteFinanciamiento.query.get(data["fuente_financiamiento_id"]):
                raise Exception("Fuente de financiamiento inválida")

        # ---- grupo UTN ----
        if data.get("grupo_utn_id"):
            if not GrupoInvestigacionUtn.query.get(data["grupo_utn_id"]):
                raise Exception("Grupo UTN inválido")
        
        numero = data.get("numeroErogacion")
        if not numero:
            raise ValueError("El número de erogación es obligatorio")

        erogacion = Erogacion(
            numero_erogacion=numero,
            egresos=egresos,
            ingresos=ingresos,
            tipo_erogacion_id=data.get("tipo_erogacion_id"),
            fuente_financiamiento_id=data.get("fuente_financiamiento_id"),
            grupo_utn_id=data.get("grupo_utn_id")
        )

        db.session.add(erogacion)
        db.session.commit()
        return erogacion.serialize()

    
    @staticmethod
    def update(erogacion_id: int, data: dict):
        if not data:
            raise Exception("El body es obligatorio")

        erogacion = Erogacion.query.get(erogacion_id)
        if not erogacion:
            raise Exception("Erogación no encontrada")

        # ---- egresos ----
        if "egresos" in data:
            try:
                egresos = float(data["egresos"])
            except (TypeError, ValueError):
                raise Exception("El campo 'egresos' debe ser numérico")

            if egresos < 0:
                raise Exception("El campo 'egresos' no puede ser negativo")

            erogacion.egresos = egresos

        # ---- ingresos ----
        if "ingresos" in data:
            try:
                ingresos = float(data["ingresos"])
            except (TypeError, ValueError):
                raise Exception("El campo 'ingresos' debe ser numérico")

            if ingresos < 0:
                raise Exception("El campo 'ingresos' no puede ser negativo")

            erogacion.ingresos = ingresos

        # ---- validar estado final ----
        if erogacion.egresos == 0 and erogacion.ingresos == 0:
            raise Exception("Egresos e ingresos no pueden ser ambos 0")

        # ---- tipo erogación ----
        if "tipo_erogacion_id" in data:
            if data["tipo_erogacion_id"] is None:
                erogacion.tipo_erogacion_id = None
            else:
                if not TipoErogacion.query.get(data["tipo_erogacion_id"]):
                    raise Exception("Tipo de erogación inválido")
                erogacion.tipo_erogacion_id = data["tipo_erogacion_id"]

        # ---- fuente financiamiento ----
        if "fuente_financiamiento_id" in data:
            if data["fuente_financiamiento_id"] is None:
                erogacion.fuente_financiamiento_id = None
            else:
                if not FuenteFinanciamiento.query.get(data["fuente_financiamiento_id"]):
                    raise Exception("Fuente de financiamiento inválida")
                erogacion.fuente_financiamiento_id = data["fuente_financiamiento_id"]

        # ---- grupo UTN ----
        if "grupo_utn_id" in data:
            if data["grupo_utn_id"] is None:
                erogacion.grupo_utn_id = None
            else:
                if not GrupoInvestigacionUtn.query.get(data["grupo_utn_id"]):
                    raise Exception("Grupo UTN inválido")
                erogacion.grupo_utn_id = data["grupo_utn_id"]

        db.session.commit()
        return erogacion.serialize()
  
  
    @staticmethod
    def delete(erogacion_id: int):
        erogacion = Erogacion.query.get(erogacion_id)
        if not erogacion:
            raise Exception("Erogación no encontrada")

        db.session.delete(erogacion)
        db.session.commit()
        return {"message": "Erogación eliminada correctamente"}
