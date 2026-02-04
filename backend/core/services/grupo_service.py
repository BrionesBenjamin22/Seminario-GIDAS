from extension import db
from core.models.grupo import GrupoInvestigacionUtn


def crear_grupo_utn(data):
    if GrupoInvestigacionUtn.query.first():
        raise ValueError("Ya existe un grupo de investigación. Solo se permite uno.")

    if not data:
        raise ValueError("Los datos no pueden estar vacíos.")
        
    # Extraer datos del payload
    nombre_unidad_academica = data.get("nombre_unidad_academica")
    nombre_sigla_grupo = data.get("nombre_sigla_grupo")
    mail = data.get("mail")
    objetivo_desarrollo = data.get("objetivo_desarrollo")
    director = data.get("director")
    vicedirector = data.get("vicedirector")

    # Validaciones
    if not nombre_unidad_academica or not nombre_sigla_grupo or not mail or not objetivo_desarrollo:
        raise ValueError("Faltan campos obligatorios: nombre_unidad_academica, nombre_sigla_grupo, mail, objetivo_desarrollo son requeridos.")

    nuevo_grupo = GrupoInvestigacionUtn(
        nombre_unidad_academica=nombre_unidad_academica,
        nombre_sigla_grupo=nombre_sigla_grupo,
        mail=mail,
        objetivo_desarrollo=objetivo_desarrollo,
        director=director,
        vicedirector=vicedirector
    )
    
    db.session.add(nuevo_grupo)
    try:
        db.session.commit()
        return nuevo_grupo
    except Exception as e:
        db.session.rollback()
        raise e


def obtener_grupo_utn():
    """
    Devuelve el grupo UTN único.
    Si no existe, lo crea usando load().
    """
    return GrupoInvestigacionUtn.load()


def actualizar_grupo_utn(data):
    grupo = GrupoInvestigacionUtn.load()
    if not grupo:
        raise ValueError("No se puede actualizar porque no existe ningún grupo de investigación.")

    if not data:
        raise ValueError("Los datos no pueden estar vacíos.")

    # Extraer datos del payload
    mail = data.get("mail")
    nombre_unidad_academica = data.get("nombre_unidad_academica")
    objetivo_desarrollo = data.get("objetivo_desarrollo")
    nombre_sigla_grupo = data.get("nombre_sigla_grupo")
    director = data.get("director")
    vicedirector = data.get("vicedirector")


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
        
    if director is not None:
        grupo.director = director.strip() if isinstance(director, str) else director
    
    if vicedirector is not None:
        grupo.vicedirector = vicedirector.strip() if isinstance(vicedirector, str) else vicedirector


    try:
        db.session.commit()
        return grupo
    except Exception:
        db.session.rollback()
        raise

def eliminar_grupo_utn():
    grupo = GrupoInvestigacionUtn.query.first()
    if not grupo:
        raise ValueError("No hay ningún grupo de investigación para eliminar.")

    db.session.delete(grupo)
    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        raise e
