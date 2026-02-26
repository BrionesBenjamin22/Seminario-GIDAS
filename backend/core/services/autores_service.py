from core.models.documentacion_autores import DocumentacionBibliografica, Autor
from extension import db


class AutorService:

    # =========================
    # Helpers
    # =========================

    @staticmethod
    def _get_or_404(autor_id: int):
        autor = db.session.get(Autor, autor_id)
        if not autor:
            raise Exception("Autor no encontrado")
        return autor

    # =========================
    # CRUD
    # =========================

    @staticmethod
    def get_all():
        autores = Autor.query.order_by(Autor.nombre_apellido.asc()).all()
        return [a.serialize() for a in autores]

    @staticmethod
    def get_by_id(autor_id: int):
        autor = AutorService._get_or_404(autor_id)
        return autor.serialize()

    @staticmethod
    def create(data: dict):
        nombre = data.get("nombre_apellido")

        if not nombre or not isinstance(nombre, str) or not nombre.strip():
            raise Exception("El nombre es obligatorio")

        nombre = nombre.strip()

        # Evitar duplicados exactos
        existente = (
            Autor.query
            .filter(Autor.nombre_apellido == nombre)
            .first()
        )

        if existente:
            raise Exception("Ya existe un autor con ese nombre")

        autor = Autor(nombre_apellido=nombre)

        db.session.add(autor)
        db.session.commit()

        return autor.serialize()

    @staticmethod
    def update(autor_id: int, data: dict):
        autor = AutorService._get_or_404(autor_id)

        if "nombre_apellido" in data:
            nombre = data["nombre_apellido"]

            if not nombre or not isinstance(nombre, str) or not nombre.strip():
                raise Exception("El nombre no puede estar vacío")

            autor.nombre_apellido = nombre.strip()

        db.session.commit()

        return autor.serialize()

    @staticmethod
    def delete(autor_id: int):
        autor = AutorService._get_or_404(autor_id)

        # opcional: evitar borrar si tiene libros asociados
        if autor.libros:
            raise Exception("No se puede eliminar un autor con libros asociados")

        db.session.delete(autor)
        db.session.commit()

        return {"message": "Autor eliminado correctamente"}

    # =========================
    # RELACIÓN AUTOR - LIBRO
    # =========================

    @staticmethod
    def add_libro(autor_id: int, libro_id: int):
        autor = AutorService._get_or_404(autor_id)

        libro = db.session.get(DocumentacionBibliografica, libro_id)
        if not libro:
            raise Exception("Libro no encontrado")

        if libro in autor.libros:
            raise Exception("El libro ya está asociado a este autor")

        autor.libros.append(libro)
        db.session.commit()

        return autor.serialize()

    @staticmethod
    def remove_libro(autor_id: int, libro_id: int):
        autor = AutorService._get_or_404(autor_id)

        libro = db.session.get(DocumentacionBibliografica, libro_id)
        if not libro:
            raise Exception("Libro no encontrado")

        if libro not in autor.libros:
            raise Exception("La relación no existe")

        autor.libros.remove(libro)
        db.session.commit()

        return autor.serialize()