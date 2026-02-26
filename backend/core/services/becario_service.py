from extension import db
from core.models.personal import Becario, TipoFormacion
from core.models.grupo import GrupoInvestigacionUtn
from core.models.proyecto_investigacion import ProyectoInvestigacion


# =====================================================
# HELPERS
# =====================================================

def _get_activo_or_404(id: int):
    becario = db.session.get(Becario, id)

    if not becario or becario.deleted_at is not None:
        raise ValueError("Becario no encontrado.")

    return becario


# =====================================================
# CREATE
# =====================================================

def crear_becario(data: dict, user_id: int):

    if not data:
        raise ValueError("Los datos no pueden estar vacíos.")

    nombre = data.get("nombre_apellido")
    horas = data.get("horas_semanales")
    tipo_formacion_id = data.get("tipo_formacion_id")
    grupo_utn_id = data.get("grupo_utn_id")

    proyectos_ids = data.get("proyectos", [])

    if not nombre or not isinstance(nombre, str):
        raise ValueError("El nombre y apellido es obligatorio.")

    if not isinstance(horas, int) or horas <= 0:
        raise ValueError("Las horas semanales deben ser un número positivo.")

    if not TipoFormacion.query.get(tipo_formacion_id):
        raise ValueError("Tipo de formación inválido.")

    if grupo_utn_id and not GrupoInvestigacionUtn.query.get(grupo_utn_id):
        raise ValueError("Grupo UTN inválido.")


    becario = Becario(
        nombre_apellido=nombre.strip(),
        horas_semanales=horas,
        tipo_formacion_id=tipo_formacion_id,
        grupo_utn_id=grupo_utn_id,

        activo=True
    )

    # Asignar proyectos (M:N)
    if proyectos_ids:
        proyectos = ProyectoInvestigacion.query.filter(
            ProyectoInvestigacion.id.in_(proyectos_ids)
        ).all()

        if len(proyectos) != len(proyectos_ids):
            raise ValueError("Uno o más proyectos son inválidos.")

        becario.participaciones_proyecto = proyectos

    db.session.add(becario)

    try:
        db.session.commit()
        return becario
    except Exception:
        db.session.rollback()
        raise


# =====================================================
# UPDATE
# =====================================================

def actualizar_becario(id: int, data: dict):

    becario = _get_activo_or_404(id)

    if "activo" in data:
        if not isinstance(data["activo"], bool):
            raise ValueError("El campo 'activo' debe ser booleano.")

        becario.activo = data["activo"]

    if "nombre_apellido" in data:
        nombre = data["nombre_apellido"]
        if not nombre or not isinstance(nombre, str):
            raise ValueError("Nombre inválido.")
        becario.nombre_apellido = nombre.strip()

    if "horas_semanales" in data:
        horas = data["horas_semanales"]
        if not isinstance(horas, int) or horas <= 0:
            raise ValueError("Horas inválidas.")
        becario.horas_semanales = horas

    if "tipo_formacion_id" in data:
        if not TipoFormacion.query.get(data["tipo_formacion_id"]):
            raise ValueError("Tipo de formación inválido.")
        becario.tipo_formacion_id = data["tipo_formacion_id"]

    if "grupo_utn_id" in data:
        if data["grupo_utn_id"] and not GrupoInvestigacionUtn.query.get(data["grupo_utn_id"]):
            raise ValueError("Grupo UTN inválido.")
        becario.grupo_utn_id = data["grupo_utn_id"]


    # Reemplazar proyectos
    if "proyectos" in data:
        proyectos_ids = data["proyectos"]

        if not isinstance(proyectos_ids, list):
            raise ValueError("El campo 'proyectos' debe ser una lista.")

        proyectos = ProyectoInvestigacion.query.filter(
            ProyectoInvestigacion.id.in_(proyectos_ids)
        ).all()

        if len(proyectos) != len(proyectos_ids):
            raise ValueError("Uno o más proyectos son inválidos.")

        becario.participaciones_proyecto = proyectos

    try:
        db.session.commit()
        return becario
    except Exception:
        db.session.rollback()
        raise


# =====================================================
# SOFT DELETE
# =====================================================

def eliminar_becario(id: int, user_id: int):

    becario = _get_activo_or_404(id)

    if not becario.activo:
        raise ValueError("El becario ya se encuentra dado de baja.")

    becario.activo = False
    becario.soft_delete(user_id)

    try:
        db.session.commit()
    except Exception:
        db.session.rollback()
        raise

    return {
        "message": "Becario eliminado correctamente.",
        "id": becario.id
    }


# =====================================================
# LISTAR
# =====================================================

def listar_becarios(activos=None):

    query = Becario.query.filter(Becario.deleted_at.is_(None))

    if activos == "true":
        query = query.filter_by(activo=True)
    elif activos == "false":
        query = query.filter_by(activo=False)
    elif activos == "all":
        pass
    else:
        query = query.filter_by(activo=True)

    return query.all()


# =====================================================
# OBTENER POR ID
# =====================================================

def obtener_becario_por_id(id: int):
    return _get_activo_or_404(id)