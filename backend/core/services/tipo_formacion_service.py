from extension import db
from core.models.personal import TipoFormacion


def crear_tipo_formacion(data):
    if not data:
        raise ValueError("Los datos no pueden estar vacíos.")

    nombre = data.get("nombre")
    if not nombre or not isinstance(nombre, str):
        raise ValueError("El nombre debe ser un texto no vacío.")

    nombre = nombre.strip().lower()
    if not nombre:
        raise ValueError("El nombre no puede estar vacío.")

    if TipoFormacion.query.filter_by(nombre=nombre).first():
        raise ValueError("Ya existe un tipo de formación con ese nombre.")

    nuevo = TipoFormacion(nombre=nombre)
    db.session.add(nuevo)

    try:
        db.session.commit()
        return nuevo
    except Exception:
        db.session.rollback()
        raise


def actualizar_tipo_formacion(id, data):
    tipo = TipoFormacion.query.get(id)
    if not tipo:
        raise ValueError("Tipo de formación no encontrado.")

    nombre = data.get("nombre")
    if not nombre or not isinstance(nombre, str):
        raise ValueError("El nombre debe ser un texto no vacío.")

    nombre = nombre.strip().lower()
    if not nombre:
        raise ValueError("El nombre no puede estar vacío.")

    duplicado = TipoFormacion.query.filter(
        TipoFormacion.nombre == nombre,
        TipoFormacion.id != id
    ).first()

    if duplicado:
        raise ValueError("Ya existe un tipo de formación con ese nombre.")

    tipo.nombre = nombre

    try:
        db.session.commit()
        return tipo
    except Exception:
        db.session.rollback()
        raise


def eliminar_tipo_formacion(id):
    tipo = TipoFormacion.query.get(id)
    if not tipo:
        raise ValueError("Tipo de formación no encontrado.")

    if tipo.becarios.count() > 0:
        raise ValueError(
            "No se puede eliminar el tipo de formación porque está asociado a becarios."
        )

    db.session.delete(tipo)
    try:
        db.session.commit()
        return tipo
    except Exception:
        db.session.rollback()
        raise


def listar_tipos_formacion():
    return TipoFormacion.query.all()


def obtener_tipo_formacion_por_id(id):
    tipo = TipoFormacion.query.get(id)
    if not tipo:
        raise ValueError("No se encontró un tipo de formación con ese id.")
    return tipo
