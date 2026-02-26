from core.models.grupo import GrupoInvestigacionUtn
from core.models.documentacion_autores import DocumentacionBibliografica, Autor
from extension import db
from datetime import datetime


class DocumentacionBibliograficaService:

    # =========================
    # Helpers
    # =========================

    @staticmethod
    def _get_activo_or_404(doc_id: int):
        doc = db.session.get(DocumentacionBibliografica, doc_id)
        if not doc or doc.deleted_at is not None:
            raise Exception("Documentación bibliográfica no encontrada")
        return doc

    # =========================
    # GET ALL
    # =========================
    @staticmethod
    def get_all(filters: dict = None):
        query = DocumentacionBibliografica.query.filter(
            DocumentacionBibliografica.deleted_at.is_(None)
        )

        if filters:
            orden = filters.get("orden")
            if orden == "asc":
                query = query.order_by(DocumentacionBibliografica.titulo.asc())
            elif orden == "desc":
                query = query.order_by(DocumentacionBibliografica.titulo.desc())

        return [d.serialize() for d in query.all()]

    # =========================
    # GET BY ID
    # =========================
    @staticmethod
    def get_by_id(doc_id: int):
        doc = DocumentacionBibliograficaService._get_activo_or_404(doc_id)
        return doc.serialize()

    # =========================
    # CREATE
    # =========================
    @staticmethod
    def create(data: dict, user_id: int):

        grupo = db.session.get(GrupoInvestigacionUtn, data["grupo_id"])
        if not grupo or grupo.deleted_at is not None:
                raise Exception("Grupo no encontrado")
        if not data.get("titulo") or not data.get("editorial"):
            raise Exception("Título y editorial son obligatorios")

        if not isinstance(data.get("anio"), int):
            raise Exception("El año debe ser numérico")

        doc = DocumentacionBibliografica(
            titulo=data["titulo"].strip(),
            editorial=data["editorial"].strip(),
            anio=data["anio"],
            grupo_id=data["grupo_id"],
            created_by=user_id
        )

        db.session.add(doc)
        db.session.commit()

        return doc.serialize()

    # =========================
    # UPDATE
    # =========================
    @staticmethod
    def update(doc_id: int, data: dict):
        doc = DocumentacionBibliograficaService._get_activo_or_404(doc_id)

        if "titulo" in data:
            doc.titulo = data["titulo"].strip()

        if "editorial" in data:
            doc.editorial = data["editorial"].strip()

        if "anio" in data:
            doc.anio = data["anio"]

        if "grupo_id" in data:
            doc.grupo_id = data["grupo_id"]

        db.session.commit()

        return doc.serialize()

    # =========================
    # SOFT DELETE
    # =========================
    @staticmethod
    def delete(doc_id: int, user_id: int):
        doc = DocumentacionBibliograficaService._get_activo_or_404(doc_id)

        doc.soft_delete(user_id)

        db.session.commit()

        return {"message": "Documentación bibliográfica eliminada correctamente"}

    # =========================
    # RELACIÓN DOCUMENTO - AUTOR
    # =========================
    @staticmethod
    def add_autor(doc_id: int, autor_id: int):
        doc = DocumentacionBibliograficaService._get_activo_or_404(doc_id)

        autor = db.session.get(Autor, autor_id)
        if not autor or getattr(autor, "deleted_at", None) is not None:
            raise ValueError("Autor no encontrado")

        if autor in doc.autores:
            raise ValueError("El autor ya está asociado")

        doc.autores.append(autor)
        db.session.commit()

        return doc.serialize()

    @staticmethod
    def remove_autor(doc_id: int, autor_id: int):
        doc = DocumentacionBibliograficaService._get_activo_or_404(doc_id)

        autor = db.session.get(Autor, autor_id)
        if not autor:
            raise Exception("Autor no encontrado")

        if autor not in doc.autores:
            raise Exception("La relación no existe")

        doc.autores.remove(autor)
        db.session.commit()

        return doc.serialize()