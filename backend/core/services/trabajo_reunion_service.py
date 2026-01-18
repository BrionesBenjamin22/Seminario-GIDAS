from core.models.trabajo_reunion import TrabajoReunionCientifica
from core.models.personal import Investigador
from core.models.grupo import GrupoInvestigacionUtn
from extension import db
from datetime import datetime, date
from sqlalchemy import func


class TrabajoReunionCientificaService:

    # -------------------------------------------------
    # Validadores internos
    # -------------------------------------------------

    @staticmethod
    def _validar_texto(valor, campo, min_len=2, max_len=255):
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

        if len(valor) > max_len:
            raise Exception(
                f"El campo '{campo}' no puede superar los {max_len} caracteres"
            )

        return valor

    @staticmethod
    def _validar_titulo_unico(titulo, trabajo_id=None):
        query = TrabajoReunionCientifica.query.filter(
            func.lower(TrabajoReunionCientifica.titulo_trabajo) == titulo.lower()
        )

        # En update: excluir el propio registro
        if trabajo_id:
            query = query.filter(TrabajoReunionCientifica.id != trabajo_id)

        if query.first():
            raise Exception("Ya existe un trabajo con ese título")

    # -------------------------------------------------
    # CRUD
    # -------------------------------------------------

    @staticmethod
    def get_all(filters: dict = None):
        query = TrabajoReunionCientifica.query

        investigador_id = filters.get("investigador_id") if filters else None
        if investigador_id:
            query = query.filter(
                TrabajoReunionCientifica.investigador_id == investigador_id
            )

        grupo_utn_id = filters.get("grupo_utn_id") if filters else None
        if grupo_utn_id:
            query = query.filter(
                TrabajoReunionCientifica.grupo_utn_id == grupo_utn_id
            )

        orden = filters.get("orden") if filters else None
        if orden == "asc":
            query = query.order_by(TrabajoReunionCientifica.fecha_inicio.asc())
        else:
            query = query.order_by(TrabajoReunionCientifica.fecha_inicio.desc())

        return [t.serialize() for t in query.all()]

    @staticmethod
    def get_by_id(trabajo_id: int):
        trabajo = TrabajoReunionCientifica.query.get(trabajo_id)
        if not trabajo:
            raise Exception("Trabajo en reunión científica no encontrado")
        return trabajo.serialize()

    @staticmethod
    def create(data: dict):
        # ---- Validar fecha ----
        try:
            fecha_inicio = datetime.strptime(
                data["fecha_inicio"], "%Y-%m-%d"
            ).date()
        except (KeyError, ValueError):
            raise Exception(
                "La fecha_inicio es obligatoria y debe tener formato YYYY-MM-DD"
            )

        if fecha_inicio > date.today():
            raise Exception("La fecha de inicio no puede ser futura")

        # ---- Validar textos ----
        titulo_trabajo = TrabajoReunionCientificaService._validar_texto(
            data.get("titulo_trabajo"), "titulo_trabajo", min_len=5, max_len=300
        )

        TrabajoReunionCientificaService._validar_titulo_unico(titulo_trabajo)

        nombre_reunion = TrabajoReunionCientificaService._validar_texto(
            data.get("nombre_reunion"), "nombre_reunion", min_len=3
        )

        ciudad = TrabajoReunionCientificaService._validar_texto(
            data.get("ciudad"), "ciudad", min_len=2
        )

        tipo_reunion_cientifica = TrabajoReunionCientificaService._validar_texto(
            data.get("tipo_reunion_cientifica"),
            "tipo_reunion_cientifica",
            min_len=3
        )

        # ---- Validar relaciones ----
        investigador_id = data.get("investigador_id")
        if not investigador_id or not Investigador.query.get(investigador_id):
            raise Exception("Investigador inválido")

        grupo_utn_id = data.get("grupo_utn_id")
        if not grupo_utn_id or not GrupoInvestigacionUtn.query.get(grupo_utn_id):
            raise Exception("Grupo UTN inválido")

        trabajo = TrabajoReunionCientifica(
            titulo_trabajo=titulo_trabajo,
            nombre_reunion=nombre_reunion,
            ciudad=ciudad,
            fecha_inicio=fecha_inicio,
            tipo_reunion_cientifica=tipo_reunion_cientifica,
            investigador_id=investigador_id,
            grupo_utn_id=grupo_utn_id
        )

        db.session.add(trabajo)
        db.session.commit()
        return trabajo.serialize()

    @staticmethod
    def update(trabajo_id: int, data: dict):
        trabajo = TrabajoReunionCientifica.query.get(trabajo_id)
        if not trabajo:
            raise Exception("Trabajo en reunión científica no encontrado")

        # ---- Update parcial ----
        if "fecha_inicio" in data:
            try:
                fecha = datetime.strptime(
                    data["fecha_inicio"], "%Y-%m-%d"
                ).date()
            except ValueError:
                raise Exception("La fecha_inicio debe tener formato YYYY-MM-DD")

            if fecha > date.today():
                raise Exception("La fecha de inicio no puede ser futura")

            trabajo.fecha_inicio = fecha

        if "titulo_trabajo" in data:
            titulo = TrabajoReunionCientificaService._validar_texto(
                data["titulo_trabajo"], "titulo_trabajo", min_len=5, max_len=300
            )

            TrabajoReunionCientificaService._validar_titulo_unico(
                titulo,
                trabajo_id=trabajo.id
            )

            trabajo.titulo_trabajo = titulo

        if "nombre_reunion" in data:
            trabajo.nombre_reunion = TrabajoReunionCientificaService._validar_texto(
                data["nombre_reunion"], "nombre_reunion", min_len=3
            )

        if "ciudad" in data:
            trabajo.ciudad = TrabajoReunionCientificaService._validar_texto(
                data["ciudad"], "ciudad", min_len=2
            )

        if "tipo_reunion_cientifica" in data:
            trabajo.tipo_reunion_cientifica = TrabajoReunionCientificaService._validar_texto(
                data["tipo_reunion_cientifica"],
                "tipo_reunion_cientifica",
                min_len=3
            )

        if "investigador_id" in data:
            if not Investigador.query.get(data["investigador_id"]):
                raise Exception("Investigador inválido")
            trabajo.investigador_id = data["investigador_id"]

        if "grupo_utn_id" in data:
            if not GrupoInvestigacionUtn.query.get(data["grupo_utn_id"]):
                raise Exception("Grupo UTN inválido")
            trabajo.grupo_utn_id = data["grupo_utn_id"]

        db.session.commit()
        return trabajo.serialize()

    @staticmethod
    def delete(trabajo_id: int):
        trabajo = TrabajoReunionCientifica.query.get(trabajo_id)
        if not trabajo:
            raise Exception("Trabajo en reunión científica no encontrado")

        db.session.delete(trabajo)
        db.session.commit()
        return {"message": "Trabajo eliminado correctamente"}
