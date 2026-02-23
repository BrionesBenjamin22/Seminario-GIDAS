from extension import db
from core.models.personal import Personal, Becario, Investigador
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


def actualizar_personal(id, data, rol):
    print("---- DEBUG ACTUALIZAR ----")
    print("ROL:", rol)
    print("ID:", id)
    print("DATA:", data)

    if rol == "personal":
        entidad = Personal.query.get(id)
    elif rol == "becario":
        entidad = Becario.query.get(id)
    elif rol == "investigador":
        entidad = Investigador.query.get(id)
    else:
        raise ValueError("Rol inválido.")

    if not entidad:
        raise ValueError("Registro no encontrado.")

    # ---- ACTUALIZAR CAMPOS COMUNES ----
    if "nombre_apellido" in data:
        entidad.nombre_apellido = data["nombre_apellido"]

    if "horas_semanales" in data:
        entidad.horas_semanales = data["horas_semanales"]

    if "activo" in data:
        entidad.activo = data["activo"]

    # ---- CAMPOS ESPECÍFICOS INVESTIGADOR ----
    if rol == "investigador":
        if "tipo_dedicacion_id" in data:
            entidad.tipo_dedicacion_id = data["tipo_dedicacion_id"]

        if "categoria_utn_id" in data:
            entidad.categoria_utn_id = data["categoria_utn_id"]

        if "programa_incentivos_id" in data:
            entidad.programa_incentivos_id = data["programa_incentivos_id"]

        if "grupo_utn_id" in data:
            entidad.grupo_utn_id = data["grupo_utn_id"]

    # ---- CAMPOS ESPECÍFICOS BECARIO ----
    if rol == "becario":
        if "tipo_formacion_id" in data:
            entidad.tipo_formacion_id = data["tipo_formacion_id"]

        if "fuente_financiamiento_id" in data:
            entidad.fuente_financiamiento_id = data["fuente_financiamiento_id"]

        if "grupo_utn_id" in data:
            entidad.grupo_utn_id = data["grupo_utn_id"]

    # ---- CAMPOS PERSONAL ----
    if rol == "personal":
        if "tipo_personal_id" in data:
            entidad.tipo_personal_id = data["tipo_personal_id"]

        if "grupo_utn_id" in data:
            entidad.grupo_utn_id = data["grupo_utn_id"]

    try:
        db.session.commit()
        print("ACTUALIZACIÓN REALMENTE GUARDADA")
        return entidad
    except Exception as e:
        db.session.rollback()
        print("ERROR REAL:", e)
        raise


def eliminar_personal_por_rol(id, rol):
    if rol == 'personal':
        personal = Personal.query.get(id)
    elif rol == 'becario':
        personal = Becario.query.get(id)
    elif rol == 'investigador':
        personal = Investigador.query.get(id)
    else:
        raise ValueError("Rol inválido.")
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
