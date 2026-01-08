from extension import db
from core.models.grupo import GrupoInvestigacionUtn


def obtener_grupo_utn():
    """
    Devuelve el grupo UTN único.
    Si no existe, lo crea usando load().
    """
    return GrupoInvestigacionUtn.load()


def actualizar_grupo_utn(data):
    grupo = GrupoInvestigacionUtn.load()

    if not data:
        raise ValueError("Los datos no pueden estar vacíos.")

    mail = data.get("mail")
    nombre_unidad_academica = data.get("nombre_unidad_academica")
    objetivo_desarrollo = data.get("objetivo_desarrollo")
    nombre_sigla_grupo = data.get("nombre_sigla_grupo")

    if mail is not None:
        if not isinstance(mail, str) or not mail.strip():
            raise ValueError("El mail debe ser un texto no vacío.")
        grupo.mail = mail.strip()

    if nombre_unidad_academica is not None:
        if not isinstance(nombre_unidad_academica, str) or not nombre_unidad_academica.strip():
            raise ValueError("El nombre de la unidad académica no puede estar vacío.")
        grupo.nombre_unidad_academica = nombre_unidad_academica.strip()

    if objetivo_desarrollo is not None:
        if not isinstance(objetivo_desarrollo, str) or not objetivo_desarrollo.strip():
            raise ValueError("El objetivo de desarrollo no puede estar vacío.")
        grupo.objetivo_desarrollo = objetivo_desarrollo.strip()

    if nombre_sigla_grupo is not None:
        if not isinstance(nombre_sigla_grupo, str) or not nombre_sigla_grupo.strip():
            raise ValueError("El nombre o sigla del grupo no puede estar vacío.")
        grupo.nombre_sigla_grupo = nombre_sigla_grupo.strip()

    try:
        db.session.commit()
        return grupo
    except Exception:
        db.session.rollback()
        raise
