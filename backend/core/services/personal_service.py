from extension import db
from core.models.personal import Personal
from core.models.tipo_personal import TipoPersonal
from core.models.grupo import GrupoInvestigacionUtn


def crear_personal(data):
    if not data:
        raise ValueError("Los datos no pueden estar vacíos.")

    nombre = data.get("nombre_apellido")
    horas = data.get("horas_semanales")
    tipo_personal_id = data.get("tipo_personal_id")
    grupo_utn_id = data.get("grupo_utn_id")

    if not nombre or not isinstance(nombre, str):
        raise ValueError("El nombre y apellido es obligatorio.")

    if not isinstance(horas, int) or horas <= 0:
        raise ValueError("Las horas semanales deben ser un número positivo.")

    if not tipo_personal_id or not TipoPersonal.query.get(tipo_personal_id):
        raise ValueError("Tipo de personal inválido.")

    if not grupo_utn_id or not GrupoInvestigacionUtn.query.get(grupo_utn_id):
        raise ValueError("Grupo UTN inválido.")

    nuevo = Personal(
        nombre_apellido=nombre.strip(),
        horas_semanales=horas,
        tipo_personal_id=tipo_personal_id,
        grupo_utn_id=grupo_utn_id,
        activo=True
    )

    db.session.add(nuevo)
    try:
        db.session.commit()
        return nuevo
    except Exception:
        db.session.rollback()
        raise


def actualizar_personal(id, data):
    personal = Personal.query.get(id)
    if not personal:
        raise ValueError("Personal no encontrado.")

   
    if "activo" in data:
        if not isinstance(data["activo"], bool):
            raise ValueError("El campo 'activo' debe ser booleano.")

        if personal.activo == data["activo"]:
            estado = "activo" if personal.activo else "inactivo"
            raise ValueError(f"El personal ya se encuentra {estado}.")

        personal.activo = data["activo"]

        try:
            db.session.commit()
            return personal
        except Exception:
            db.session.rollback()
            raise
        
    if not personal.activo:
        raise ValueError(
            "No se puede modificar personal dado de baja. Reactívelo primero."
        )


    if "nombre_apellido" in data:
        nombre = data["nombre_apellido"]
        if not nombre or not isinstance(nombre, str):
            raise ValueError("Nombre inválido.")
        personal.nombre_apellido = nombre.strip()

    if "horas_semanales" in data:
        horas = data["horas_semanales"]
        if not isinstance(horas, int) or horas <= 0:
            raise ValueError("Horas inválidas.")
        personal.horas_semanales = horas

    if "tipo_personal_id" in data:
        tipo_id = data["tipo_personal_id"]
        if not TipoPersonal.query.get(tipo_id):
            raise ValueError("Tipo de personal inválido.")
        personal.tipo_personal_id = tipo_id

    if "grupo_utn_id" in data:
        grupo_id = data["grupo_utn_id"]
        if not GrupoInvestigacionUtn.query.get(grupo_id):
            raise ValueError("Grupo UTN inválido.")
        personal.grupo_utn_id = grupo_id

    try:
        db.session.commit()
        return personal
    except Exception:
        db.session.rollback()
        raise


def eliminar_personal(id):
    personal = Personal.query.get(id)
    if not personal:
        raise ValueError("Personal no encontrado.")

    if not personal.activo:
        raise ValueError("El personal ya se encuentra dado de baja.")

    personal.activo = False

    try:
        db.session.commit()
    except Exception:
        db.session.rollback()
        raise

    return {
        "message": "Personal dado de baja correctamente.",
        "id": personal.id
    }



def listar_personal(activos=None):
    query = Personal.query

    if activos == "true":
        query = query.filter_by(activo=True)
    elif activos == "false":
        query = query.filter_by(activo=False)
    elif activos == "all":
        pass
    else:
        query = query.filter_by(activo=True)

    return query.all()


def obtener_personal_por_id(id):
    personal = Personal.query.get(id)
    if not personal:
        raise ValueError("Personal no encontrado.")
    return personal
