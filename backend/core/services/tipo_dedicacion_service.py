from extension import db
from core.models.personal import TipoDedicacion


def crear_tipo_dedicacion(data):
    if not data:
        raise ValueError("Los datos no pueden estar vacíos.")

    nombre = data.get("nombre")
    if not nombre or not isinstance(nombre, str):
        raise ValueError("El nombre debe ser un texto no vacío.")

    nombre = nombre.strip()
    if not nombre:
        raise ValueError("El nombre no puede estar vacío.")

    if TipoDedicacion.query.filter_by(nombre=nombre).first():
        raise ValueError("Ya existe un tipo de dedicación con ese nombre.")

    nuevo = TipoDedicacion(nombre=nombre)
    db.session.add(nuevo)

    try:
        db.session.commit()
        return nuevo
    except Exception:
        db.session.rollback()
        raise


def actualizar_tipo_dedicacion(id, data):
    tipo = TipoDedicacion.query.get(id)
    if not tipo:
        raise ValueError("Tipo de dedicación no encontrado.")

    nombre = data.get("nombre")
    if not nombre or not isinstance(nombre, str):
        raise ValueError("El nombre debe ser un texto no vacío.")

    nombre = nombre.strip()
    if not nombre:
        raise ValueError("El nombre no puede estar vacío.")

    duplicado = TipoDedicacion.query.filter(
        TipoDedicacion.nombre == nombre,
        TipoDedicacion.id != id
    ).first()

    if duplicado:
        raise ValueError("Ya existe un tipo de dedicación con ese nombre.")

    tipo.nombre = nombre

    try:
        db.session.commit()
        return tipo
    except Exception:
        db.session.rollback()
        raise


def eliminar_tipo_dedicacion(id):
    tipo = TipoDedicacion.query.get(id)
    if not tipo:
        raise ValueError("Tipo de dedicación no encontrado.")

    if tipo.investigadores.count() > 0:
        raise ValueError(
            "No se puede eliminar el tipo de dedicación porque está asociado a investigadores."
        )

    db.session.delete(tipo)
    try:
        db.session.commit()
        return tipo
    except Exception:
        db.session.rollback()
        raise


def listar_tipos_dedicacion():
    return TipoDedicacion.query.all()


def obtener_tipo_dedicacion_por_id(id):
    tipo = TipoDedicacion.query.get(id)
    if not tipo:
        raise ValueError("No se encontró un tipo de dedicación con ese id.")
    return tipo
