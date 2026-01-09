from core.models.documentacion_autores import DocumentacionBibliografica, Autor
from extension import db

class AutorService:

    @staticmethod
    def get_all():
        return [a.serialize() for a in Autor.query.all()]

    @staticmethod
    def get_by_id(autor_id: int):
        autor = Autor.query.get(autor_id)
        if not autor:
            raise Exception("Autor no encontrado")
        return autor.serialize()

    @staticmethod
    def create(data: dict):
        autor = Autor(
            nombre_apellido=data["nombre_apellido"]
        )
        db.session.add(autor)
        db.session.commit()
        return autor.serialize()

    @staticmethod
    def update(autor_id: int, data: dict):
        autor = Autor.query.get(autor_id)
        if not autor:
            raise Exception("Autor no encontrado")

        autor.nombre_apellido = data.get(
            "nombre_apellido", autor.nombre_apellido
        )

        db.session.commit()
        return autor.serialize()

    @staticmethod
    def delete(autor_id: int):
        autor = Autor.query.get(autor_id)
        if not autor:
            raise Exception("Autor no encontrado")

        db.session.delete(autor)
        db.session.commit()
        return {"message": "Autor eliminado correctamente"}

    # -------- RELACIÓN AUTOR - LIBRO --------

    @staticmethod
    def add_libro(autor_id: int, libro_id: int):
        autor = Autor.query.get(autor_id)
        if not autor:
            raise Exception("Autor no encontrado")

        libro = DocumentacionBibliografica.query.get(libro_id)
        if not libro:
            raise Exception("Libro no encontrado")

        if libro not in autor.libros:
            autor.libros.append(libro)
            db.session.commit()

        return autor.serialize()

    @staticmethod
    def remove_libro(autor_id: int, libro_id: int):
        autor = Autor.query.get(autor_id)
        if not autor:
            raise Exception("Autor no encontrado")

        libro = DocumentacionBibliografica.query.get(libro_id)
        if not libro:
            raise Exception("Libro no encontrado")

        if libro in autor.libros:
            autor.libros.remove(libro)
            db.session.commit()

        return autor.serialize()
