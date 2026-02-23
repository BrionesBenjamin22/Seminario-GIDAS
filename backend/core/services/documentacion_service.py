from core.models.documentacion_autores import DocumentacionBibliografica, Autor
from extension import db


class DocumentacionBibliograficaService:

    # =========================
    # GET ALL (con orden alfabético)
    # =========================
    @staticmethod
    def get_all(filters: dict = None):
        query = DocumentacionBibliografica.query

        # ---- ORDEN ALFABÉTICO POR TÍTULO ----
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
        doc = DocumentacionBibliografica.query.get(doc_id)
        if not doc:
            raise Exception("Documentación bibliográfica no encontrada")
        return doc.serialize()

    # =========================
    # CREATE
    # =========================
    @staticmethod
    def create(data: dict):
        doc = DocumentacionBibliografica(
            titulo=data["titulo"],
            editorial=data["editorial"],
            anio=data["anio"],
            grupo_id=data.get("grupo_id")
        )

        db.session.add(doc)
        db.session.commit()
        return doc.serialize()

    # =========================
    # UPDATE
    # =========================
    @staticmethod
    def update(doc_id: int, data: dict):
        doc = DocumentacionBibliografica.query.get(doc_id)
        if not doc:
            raise Exception("Documentación bibliográfica no encontrada")

        doc.titulo = data.get("titulo", doc.titulo)
        doc.editorial = data.get("editorial", doc.editorial)
        doc.anio = data.get("anio", doc.anio)
        doc.grupo_id = data.get("grupo_id", doc.grupo_id)
        
        db.session.commit()
        return doc.serialize()

    # =========================
    # DELETE
    # =========================
    @staticmethod
    def delete(doc_id: int):
        doc = DocumentacionBibliografica.query.get(doc_id)
        if not doc:
            raise Exception("Documentación bibliográfica no encontrada")

        db.session.delete(doc)
        db.session.commit()
        return {"message": "Documentación bibliográfica eliminada correctamente"}

    # =========================
    # RELACIÓN DOCUMENTO - AUTOR
    # =========================
    @staticmethod
    def add_autor(doc_id: int, autor_id: int):
        doc = DocumentacionBibliografica.query.get(doc_id)
        if not doc:
            raise Exception("Documentación no encontrada")

        autor = Autor.query.get(autor_id)
        if not autor:
            raise Exception("Autor no encontrado")

        if autor not in doc.autores:
            doc.autores.append(autor)
            db.session.commit()

        return doc.serialize()

    @staticmethod
    def remove_autor(doc_id: int, autor_id: int):
        doc = DocumentacionBibliografica.query.get(doc_id)
        if not doc:
            raise Exception("Documentación no encontrada")

        autor = Autor.query.get(autor_id)
        if not autor:
            raise Exception("Autor no encontrado")

        if autor in doc.autores:
            doc.autores.remove(autor)
            db.session.commit()

        return doc.serialize()
