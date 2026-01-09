from extension import db
from core.models.programa_actividades import PlanificacionGrupo
from core.models.grupo import GrupoInvestigacionUtn
from sqlalchemy.exc import IntegrityError


def crear_planificacion_grupo(data):
    if not data:
        raise ValueError("Los datos no pueden estar vacíos.")

    descripcion = data.get("descripcion")
    anio = data.get("anio")
    grupo_id = data.get("grupo_id")

    if not descripcion or not isinstance(descripcion, str):
        raise ValueError("La descripción es obligatoria.")

    if not isinstance(anio, int) or anio < 2000:
        raise ValueError("El año es inválido.")

    grupo = GrupoInvestigacionUtn.query.get(grupo_id)
    if not grupo:
        raise ValueError("Grupo UTN inválido.")

    # 🔒 Regla: una planificación por grupo y año
    existente = PlanificacionGrupo.query.filter_by(
        grupo_id=grupo_id,
        anio=anio
    ).first()

    if existente:
        raise ValueError(
            "Ya existe una planificación para ese grupo en el año indicado."
        )

    planificacion = PlanificacionGrupo(
        descripcion=descripcion.strip(),
        anio=anio,
        grupo_id=grupo_id
    )

    db.session.add(planificacion)
    try:
        db.session.commit()
        return planificacion
    except Exception:
        db.session.rollback()
        raise


def actualizar_planificacion_grupo(id, data):
    planificacion = PlanificacionGrupo.query.get(id)
    if not planificacion:
        raise ValueError("Planificación no encontrada.")

    if "descripcion" in data:
        descripcion = data["descripcion"]
        if not descripcion or not isinstance(descripcion, str):
            raise ValueError("Descripción inválida.")
        planificacion.descripcion = descripcion.strip()

    if "anio" in data:
        anio = data["anio"]
        if not isinstance(anio, int) or anio < 2000:
            raise ValueError("Año inválido.")

        duplicado = PlanificacionGrupo.query.filter(
            PlanificacionGrupo.grupo_id == planificacion.grupo_id,
            PlanificacionGrupo.anio == anio,
            PlanificacionGrupo.id != id
        ).first()

        if duplicado:
            raise ValueError(
                "Ya existe otra planificación para ese grupo y año."
            )

        planificacion.anio = anio

    try:
        db.session.commit()
        return planificacion
    except Exception:
        db.session.rollback()
        raise


def eliminar_planificacion_grupo(id):
    planificacion = PlanificacionGrupo.query.get(id)
    if not planificacion:
        raise ValueError("Planificación no encontrada.")

    if planificacion.proyectos_investigacion:
        raise ValueError(
            "No se puede eliminar la planificación porque tiene proyectos asociados."
        )

    db.session.delete(planificacion)
    db.session.commit()


def listar_planificaciones():
    return PlanificacionGrupo.query.all()


def obtener_planificacion_por_id(id):
    planificacion = PlanificacionGrupo.query.get(id)
    if not planificacion:
        raise ValueError("Planificación no encontrada.")
    return planificacion
