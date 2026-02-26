from core.models.trabajo_reunion import TrabajoReunionCientifica, TipoReunion
from core.models.personal import Investigador
from core.models.grupo import GrupoInvestigacionUtn
from extension import db
from datetime import datetime, date
from sqlalchemy import func


class TrabajoReunionCientificaService:

    # =================================================
    # VALIDADORES
    # =================================================

    @staticmethod
    def _validar_texto(valor, campo, min_len=2, max_len=255):
        if valor is None:
            raise ValueError(f"El campo '{campo}' es obligatorio")

        if not isinstance(valor, str):
            raise ValueError(f"El campo '{campo}' debe ser texto")

        valor = valor.strip()

        if not valor:
            raise ValueError(f"El campo '{campo}' no puede estar vacío")

        if len(valor) < min_len:
            raise ValueError(
                f"El campo '{campo}' debe tener al menos {min_len} caracteres"
            )

        if len(valor) > max_len:
            raise ValueError(
                f"El campo '{campo}' no puede superar los {max_len} caracteres"
            )

        return valor


    @staticmethod
    def _validar_titulo_unico(titulo, trabajo_id=None):
        query = TrabajoReunionCientifica.query.filter(
            func.lower(TrabajoReunionCientifica.titulo_trabajo) == titulo.lower(),
            TrabajoReunionCientifica.deleted_at.is_(None)  # 🔥 solo activos
        )

        if trabajo_id:
            query = query.filter(
                TrabajoReunionCientifica.id != trabajo_id
            )

        if query.first():
            raise ValueError("Ya existe un trabajo activo con ese título")


    # =================================================
    # GET ALL (con filtro activos)
    # =================================================

    @staticmethod
    def get_all(filters: dict = None):
        query = TrabajoReunionCientifica.query

        # 🔥 Solo activos por defecto
        activos = filters.get("activos") if filters else "true"

        if activos == "true":
            query = query.filter(TrabajoReunionCientifica.deleted_at.is_(None))
        elif activos == "false":
            query = query.filter(TrabajoReunionCientifica.deleted_at.isnot(None))
        elif activos == "all":
            pass

        # 🔥 FILTRO CORRECTO M:N
        investigador_id = filters.get("investigador_id") if filters else None
        if investigador_id:
            query = query.join(
                TrabajoReunionCientifica.investigadores
            ).filter(
                Investigador.id == investigador_id,
                Investigador.deleted_at.is_(None)
            )

        grupo_utn_id = filters.get("grupo_utn_id") if filters else None
        if grupo_utn_id:
            query = query.filter(
                TrabajoReunionCientifica.grupo_utn_id == grupo_utn_id
            )

        orden = filters.get("orden") if filters else None
        if orden == "asc":
            query = query.order_by(
                TrabajoReunionCientifica.fecha_inicio.asc()
            )
        else:
            query = query.order_by(
                TrabajoReunionCientifica.fecha_inicio.desc()
            )

        return [t.serialize() for t in query.all()]


    # =================================================
    # GET BY ID
    # =================================================

    @staticmethod
    def get_by_id(trabajo_id: int):
        trabajo = TrabajoReunionCientifica.query.get(trabajo_id)
        if not trabajo:
            raise ValueError("Trabajo en reunión científica no encontrado")

        return trabajo.serialize()


    # =================================================
    # CREATE
    # =================================================

    @staticmethod
    def create(data: dict, user_id: int):

        try:
            fecha_inicio = datetime.strptime(
                data["fecha_inicio"], "%Y-%m-%d"
            ).date()
        except (KeyError, ValueError):
            raise ValueError(
                "La fecha_inicio es obligatoria y debe tener formato YYYY-MM-DD"
            )

        if fecha_inicio > date.today():
            raise ValueError("La fecha de inicio no puede ser futura")

        titulo = TrabajoReunionCientificaService._validar_texto(
            data.get("titulo_trabajo"), "titulo_trabajo", 5, 300
        )

        TrabajoReunionCientificaService._validar_titulo_unico(titulo)

        nombre_reunion = TrabajoReunionCientificaService._validar_texto(
            data.get("nombre_reunion"), "nombre_reunion", 3
        )

        procedencia = TrabajoReunionCientificaService._validar_texto(
            data.get("procedencia"), "procedencia", 2
        )

        tipo_reunion_id = data.get("tipo_reunion_id")
        if not tipo_reunion_id or not TipoReunion.query.get(tipo_reunion_id):
            raise ValueError("Tipo de reunión científica inválido")

        grupo_utn_id = data.get("grupo_utn_id")
        if not grupo_utn_id or not GrupoInvestigacionUtn.query.get(grupo_utn_id):
            raise ValueError("Grupo UTN inválido")

        trabajo = TrabajoReunionCientifica(
            titulo_trabajo=titulo,
            nombre_reunion=nombre_reunion,
            procedencia=procedencia,
            fecha_inicio=fecha_inicio,
            tipo_reunion_id=tipo_reunion_id,
            grupo_utn_id=grupo_utn_id,
            created_by=user_id  # 🔥 auditoría
        )

        db.session.add(trabajo)
        db.session.commit()

        return trabajo.serialize()


    # =================================================
    # UPDATE
    # =================================================

    @staticmethod
    def update(trabajo_id: int, data: dict):
        trabajo = TrabajoReunionCientifica.query.get(trabajo_id)

        if not trabajo:
            raise ValueError("Trabajo en reunión científica no encontrado")

        if trabajo.deleted_at is not None:
            raise ValueError("No se puede modificar un trabajo eliminado")

        if "fecha_inicio" in data:
            fecha = datetime.strptime(
                data["fecha_inicio"], "%Y-%m-%d"
            ).date()

            if fecha > date.today():
                raise ValueError("La fecha no puede ser futura")

            trabajo.fecha_inicio = fecha

        if "titulo_trabajo" in data:
            titulo = TrabajoReunionCientificaService._validar_texto(
                data["titulo_trabajo"], "titulo_trabajo", 5, 300
            )

            TrabajoReunionCientificaService._validar_titulo_unico(
                titulo, trabajo.id
            )

            trabajo.titulo_trabajo = titulo

        if "nombre_reunion" in data:
            trabajo.nombre_reunion = TrabajoReunionCientificaService._validar_texto(
                data["nombre_reunion"], "nombre_reunion", 3
            )

        if "procedencia" in data:
            trabajo.procedencia = TrabajoReunionCientificaService._validar_texto(
                data["procedencia"], "procedencia", 2
            )

        db.session.commit()
        return trabajo.serialize()


    # =================================================
    # SOFT DELETE
    # =================================================

    @staticmethod
    def delete(trabajo_id: int, user_id: int):
        trabajo = TrabajoReunionCientifica.query.get(trabajo_id)

        if not trabajo:
            raise ValueError("Trabajo no encontrado")

        if trabajo.deleted_at is not None:
            raise ValueError("El trabajo ya está eliminado")

        trabajo.soft_delete(user_id)

        db.session.commit()
        return {"message": "Trabajo eliminado correctamente (soft delete)"}


    # =================================================
    # RESTORE
    # =================================================

    @staticmethod
    def restore(trabajo_id: int):
        trabajo = TrabajoReunionCientifica.query.get(trabajo_id)

        if not trabajo:
            raise ValueError("Trabajo no encontrado")

        trabajo.restore()
        trabajo.activo = True

        db.session.commit()
        return trabajo.serialize()


    # =================================================
    # M:N Investigadores
    # =================================================

    @staticmethod
    def vincular_investigadores(trabajo_id: int, investigadores_ids: list[int]):

        trabajo = TrabajoReunionCientifica.query.get(trabajo_id)
        if not trabajo:
            raise ValueError("Trabajo no encontrado")

        investigadores = (
            db.session.query(Investigador)
            .filter(
                Investigador.id.in_(investigadores_ids),
                Investigador.deleted_at.is_(None)
            )
            .all()
        )

        if len(investigadores) != len(investigadores_ids):
            raise ValueError("Uno o más investigadores no existen o están eliminados")

        for inv in investigadores:
            if inv not in trabajo.investigadores:
                trabajo.investigadores.append(inv)

        db.session.commit()
        return trabajo.serialize()


    @staticmethod
    def desvincular_investigadores(trabajo_id: int, investigadores_ids: list[int]):

        trabajo = TrabajoReunionCientifica.query.get(trabajo_id)
        if not trabajo:
            raise ValueError("Trabajo no encontrado")

        for inv in trabajo.investigadores[:]:
            if inv.id in investigadores_ids:
                trabajo.investigadores.remove(inv)

        db.session.commit()
        return trabajo.serialize()