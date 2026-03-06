from extension import db
from core.models.personal import Personal, Becario, Investigador, PersonalHorasHistorial, BecarioHorasHistorial, InvestigadorHorasHistorial
from core.models.tipo_personal import TipoPersonal
from core.models.grupo import GrupoInvestigacionUtn
from datetime import date


# =====================================================
# CREAR PERSONAL
# =====================================================

def crear_personal(data, user_id):

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
        activo=True,
        created_by=user_id
    )

    db.session.add(nuevo)
    db.session.flush()

    # Crear historial inicial
    historial = PersonalHorasHistorial(
        personal_id=nuevo.id,
        horas_semanales=horas,
        fecha_inicio=date.today(),
        fecha_fin=None,
        created_by=user_id
    )

    db.session.add(historial)
    db.session.commit()

    return nuevo

# =====================================================
# ACTUALIZAR PERSONAL
# =====================================================

def actualizar_personal(id, data, rol, user_id:int):
    if rol == "personal":
        entidad = Personal.query.get(id)
        HistorialModel = PersonalHorasHistorial
        fk_field = "personal_id"

    elif rol == "becario":
        entidad = Becario.query.get(id)
        HistorialModel = BecarioHorasHistorial
        fk_field = "becario_id"

    elif rol == "investigador":
        entidad = Investigador.query.get(id)
        HistorialModel = InvestigadorHorasHistorial
        fk_field = "investigador_id"
    
    if not entidad:
        raise ValueError("Registro no encontrado.")

    if entidad.deleted_at is not None:
        raise ValueError("No se puede modificar un registro eliminado.")

    # -------- CAMPOS COMUNES --------
    if "nombre_apellido" in data:
        entidad.nombre_apellido = data["nombre_apellido"].strip()

    if "horas_semanales" in data:

        horas = data["horas_semanales"]

        if not isinstance(horas, int) or horas <= 0:
            raise ValueError("Las horas semanales deben ser un número positivo.")

        historial_activo = next(
            (h for h in entidad.historial_horas if h.fecha_fin is None),
            None
        )

        if not historial_activo:
            nuevo = HistorialModel(
                **{fk_field: entidad.id},
                horas_semanales=horas,
                fecha_inicio=date.today(),
                fecha_fin=None,
                created_by=user_id
            )
            db.session.add(nuevo)

        elif historial_activo.horas_semanales != horas:

            historial_activo.fecha_fin = date.today()

            nuevo = HistorialModel(
                **{fk_field: entidad.id},
                horas_semanales=horas,
                fecha_inicio=date.today(),
                fecha_fin=None,
                created_by=user_id
            )
            db.session.add(nuevo)

        entidad.horas_semanales = horas

    if "activo" in data:
        entidad.activo = data["activo"]

    # -------- INVESTIGADOR --------
    if rol == "investigador":

        if "tipo_dedicacion_id" in data:
            entidad.tipo_dedicacion_id = data["tipo_dedicacion_id"]

        if "categoria_utn_id" in data:
            entidad.categoria_utn_id = data["categoria_utn_id"]

        if "programa_incentivos_id" in data:
            entidad.programa_incentivos_id = data["programa_incentivos_id"]

        if "grupo_utn_id" in data:
            if not GrupoInvestigacionUtn.query.get(data["grupo_utn_id"]):
                raise ValueError("Grupo UTN inválido.")
            entidad.grupo_utn_id = data["grupo_utn_id"]

    # -------- BECARIO --------
    if rol == "becario":

        if "tipo_formacion_id" in data:
            entidad.tipo_formacion_id = data["tipo_formacion_id"]

        if "grupo_utn_id" in data:
            if not GrupoInvestigacionUtn.query.get(data["grupo_utn_id"]):
                raise ValueError("Grupo UTN inválido.")
            entidad.grupo_utn_id = data["grupo_utn_id"]

    # -------- PERSONAL --------
    if rol == "personal":

        if "tipo_personal_id" in data:
            if not TipoPersonal.query.get(data["tipo_personal_id"]):
                raise ValueError("Tipo de personal inválido.")
            entidad.tipo_personal_id = data["tipo_personal_id"]

        if "grupo_utn_id" in data:
            if not GrupoInvestigacionUtn.query.get(data["grupo_utn_id"]):
                raise ValueError("Grupo UTN inválido.")
            entidad.grupo_utn_id = data["grupo_utn_id"]

    db.session.commit()

    return entidad


# =====================================================
# SOFT DELETE
# =====================================================

def eliminar_personal_por_rol(id, rol, user_id):

    if rol == 'personal':
        entidad = Personal.query.get(id)
    elif rol == 'becario':
        entidad = Becario.query.get(id)
    elif rol == 'investigador':
        entidad = Investigador.query.get(id)
    else:
        raise ValueError("Rol inválido.")

    if not entidad:
        raise ValueError("Registro no encontrado.")

    if entidad.deleted_at is not None:
        raise ValueError("El registro ya se encuentra eliminado.")

    # Cerrar historial activo
    historial_activo = next(
        (h for h in entidad.historial_horas if h.fecha_fin is None),
        None
    )

    if historial_activo:
        historial_activo.fecha_fin = date.today()

    entidad.activo = False
    entidad.soft_delete(user_id)

    db.session.commit()

    return {
        "message": "Personal eliminado correctamente (soft delete).",
        "id": entidad.id
    }
# =====================================================
# RESTORE
# =====================================================

def restaurar_personal(id, rol):

    if rol == 'personal':
        entidad = Personal.query.get(id)
    elif rol == 'becario':
        entidad = Becario.query.get(id)
    elif rol == 'investigador':
        entidad = Investigador.query.get(id)
    else:
        raise ValueError("Rol inválido.")

    if not entidad:
        raise ValueError("Personal no encontrado.")

    entidad.restore()

    db.session.commit()

    return entidad


# =====================================================
# LISTAR
# =====================================================
def listar_personal(activos="true"):

    query = Personal.query

    if activos is None:
        activos = "true"

    activos = activos.strip().lower()

    if activos == "true":
        query = query.filter(Personal.deleted_at.is_(None))

    elif activos == "false":
        query = query.filter(Personal.deleted_at.isnot(None))

    elif activos == "all":
        pass

    else:
        query = query.filter(Personal.deleted_at.is_(None))

    return query.all()


# =====================================================
# OBTENER POR ID
# =====================================================

def obtener_personal_por_id(id):

    personal = Personal.query.get(id)

    if not personal:
        raise ValueError("Personal no encontrado.")

    return personal