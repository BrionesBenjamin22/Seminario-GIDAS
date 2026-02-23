from core.models.articulo_divulgacion import ArticuloDivulgacion
from core.models.grupo import GrupoInvestigacionUtn
from extension import db
from datetime import datetime, date


class ArticuloDivulgacionService:

    # -------------------------------------------------
    # Validadores internos
    # -------------------------------------------------

    @staticmethod
    def _validar_texto(valor, campo, min_len=3, max_len=500):
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
    def _validar_fecha(fecha_publicacion):
        if fecha_publicacion > date.today():
            raise Exception("La fecha de publicación no puede ser futura")

    # -------------------------------------------------
    # CRUD
    # -------------------------------------------------

    @staticmethod
    def get_all(filters: dict = None):
        query = ArticuloDivulgacion.query

        grupo_id = filters.get("grupo_utn_id") if filters else None
        if grupo_id:
            query = query.filter(
                ArticuloDivulgacion.grupo_utn_id == grupo_id
            )

        orden = filters.get("orden") if filters else None
        if orden == "asc":
            query = query.order_by(ArticuloDivulgacion.fecha_publicacion.asc())
        else:
            query = query.order_by(ArticuloDivulgacion.fecha_publicacion.desc())

        return [a.serialize() for a in query.all()]

    @staticmethod
    def get_by_id(articulo_id: int):
        articulo = ArticuloDivulgacion.query.get(articulo_id)
        if not articulo:
            raise Exception("Artículo de divulgación no encontrado")

        return articulo.serialize()

    @staticmethod
    def create(data: dict):

        # ---- Validar fecha ----
        try:
            fecha_publicacion = datetime.strptime(
                data["fecha_publicacion"], "%Y-%m-%d"
            ).date()
        except (KeyError, ValueError):
            raise Exception(
                "La fecha de publicación es obligatoria y debe tener formato YYYY-MM-DD"
            )

        ArticuloDivulgacionService._validar_fecha(fecha_publicacion)

        # ---- Validar textos ----
        titulo = ArticuloDivulgacionService._validar_texto(
            data.get("titulo"), "titulo", min_len=5
        )

        descripcion = ArticuloDivulgacionService._validar_texto(
            data.get("descripcion"), "descripcion", min_len=10
        )

        # ---- Validar relación ----
        grupo_utn_id = data.get("grupo_utn_id")
        if not grupo_utn_id or not GrupoInvestigacionUtn.query.get(grupo_utn_id):
            raise Exception("Grupo UTN inválido")

        articulo = ArticuloDivulgacion(
            titulo=titulo,
            descripcion=descripcion,
            fecha_publicacion=fecha_publicacion,
            grupo_utn_id=grupo_utn_id
        )

        db.session.add(articulo)

        try:
            db.session.commit()
        except Exception:
            db.session.rollback()
            raise Exception("Error al guardar el artículo de divulgación")

        return articulo.serialize()

    @staticmethod
    def update(articulo_id: int, data: dict):
        articulo = ArticuloDivulgacion.query.get(articulo_id)

        if not articulo:
            raise Exception("Artículo de divulgación no encontrado")

        # ---- Update parcial ----

        if "fecha_publicacion" in data:
            try:
                fecha_publicacion = datetime.strptime(
                    data["fecha_publicacion"], "%Y-%m-%d"
                ).date()
            except ValueError:
                raise Exception("La fecha debe tener formato YYYY-MM-DD")

            ArticuloDivulgacionService._validar_fecha(fecha_publicacion)
            articulo.fecha_publicacion = fecha_publicacion

        if "titulo" in data:
            articulo.titulo = ArticuloDivulgacionService._validar_texto(
                data["titulo"], "titulo", min_len=5
            )

        if "descripcion" in data:
            articulo.descripcion = ArticuloDivulgacionService._validar_texto(
                data["descripcion"], "descripcion", min_len=10
            )

        if "grupo_utn_id" in data:
            if not GrupoInvestigacionUtn.query.get(data["grupo_utn_id"]):
                raise Exception("Grupo UTN inválido")
            articulo.grupo_utn_id = data["grupo_utn_id"]

        try:
            db.session.commit()
        except Exception:
            db.session.rollback()
            raise Exception("Error al actualizar el artículo de divulgación")

        return articulo.serialize()

    @staticmethod
    def delete(articulo_id: int):
        articulo = ArticuloDivulgacion.query.get(articulo_id)

        if not articulo:
            raise Exception("Artículo de divulgación no encontrado")

        db.session.delete(articulo)

        try:
            db.session.commit()
        except Exception:
            db.session.rollback()
            raise Exception("Error al eliminar el artículo")

        return {"message": "Artículo de divulgación eliminado correctamente"}