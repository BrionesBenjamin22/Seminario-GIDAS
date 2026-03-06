from extension import db
from core.models.personal import Investigador, TipoDedicacion, InvestigadorHorasHistorial
from core.models.categoria_utn import CategoriaUtn
from core.models.programa_incentivos import ProgramaIncentivos
from core.models.grupo import GrupoInvestigacionUtn
from core.models.proyecto_investigacion import ProyectoInvestigacion
from sqlalchemy.exc import IntegrityError
from datetime import date


# =====================================================
# CREATE
# =====================================================

def crear_investigador(data, user_id):

    if not data:
        raise ValueError("Los datos no pueden estar vacíos.")

    nombre = data.get("nombre_apellido")
    horas = data.get("horas_semanales")
    tipo_dedicacion_id = data.get("tipo_dedicacion_id")

    if not nombre or not isinstance(nombre, str):
        raise ValueError("El nombre y apellido es obligatorio.")

    if not isinstance(horas, int) or horas <= 0:
        raise ValueError("Las horas semanales deben ser un número positivo.")

    if not tipo_dedicacion_id:
        raise ValueError("El tipo de dedicación es obligatorio.")

    if not TipoDedicacion.query.get(tipo_dedicacion_id):
        raise ValueError("Tipo de dedicación inválido.")

    investigador = Investigador(
        nombre_apellido=nombre.strip(),
        horas_semanales=horas,
        tipo_dedicacion_id=tipo_dedicacion_id,
        categoria_utn_id=data.get("categoria_utn_id"),
        programa_incentivos_id=data.get("programa_incentivos_id"),
        grupo_utn_id=data.get("grupo_utn_id"),
        activo=True,
        created_by=user_id
    )

    db.session.add(investigador)
    db.session.flush()  # Necesario para obtener investigador.id

    # Crear historial inicial
    historial = InvestigadorHorasHistorial(
        investigador_id=investigador.id,
        horas_semanales=horas,
        fecha_inicio=date.today(),
        fecha_fin=None,
        created_by=user_id
    )

    db.session.add(historial)

    try:
        db.session.commit()
        return investigador
    except IntegrityError:
        db.session.rollback()
        raise ValueError("Error de integridad al crear el investigador.")


# =====================================================
# UPDATE
# =====================================================

def actualizar_investigador(id, data, user_id):

    investigador = Investigador.query.filter(
        Investigador.deleted_at.is_(None),
        Investigador.id == id
    ).first()

    if not investigador:
        raise ValueError("Investigador no encontrado.")

    if not data:
        raise ValueError("El body es obligatorio.")


    if "nombre_apellido" in data:
        nombre = data["nombre_apellido"]
        if not nombre or not isinstance(nombre, str):
            raise ValueError("Nombre inválido.")
        investigador.nombre_apellido = nombre.strip()

    # Horas (manejo histórico)
    if "horas_semanales" in data:
        horas = data["horas_semanales"]

        if not isinstance(horas, int) or horas <= 0:
            raise ValueError("Horas inválidas.")

        historial_activo = next(
            (h for h in investigador.historial_horas if h.fecha_fin is None),
            None
        )

        # Si no hay historial activo → crear uno
        if not historial_activo:
            nuevo = InvestigadorHorasHistorial(
                investigador_id=id,
                horas_semanales=horas,
                fecha_inicio=date.today(),
                fecha_fin=None,
                created_by=user_id
            )
            db.session.add(nuevo)

        # Si existe y cambia el valor → cerrar y crear nuevo
        elif historial_activo.horas_semanales != horas:

            historial_activo.fecha_fin = date.today()

            nuevo = InvestigadorHorasHistorial(
                investigador_id=id,
                horas_semanales=horas,
                fecha_inicio=date.today(),
                fecha_fin=None,
                created_by=user_id
            )

            db.session.add(nuevo)

        investigador.horas_semanales = horas


    if "tipo_dedicacion_id" in data:
        if not TipoDedicacion.query.get(data["tipo_dedicacion_id"]):
            raise ValueError("Tipo de dedicación inválido.")
        investigador.tipo_dedicacion_id = data["tipo_dedicacion_id"]

    if "categoria_utn_id" in data:
        investigador.categoria_utn_id = data["categoria_utn_id"]

    if "programa_incentivos_id" in data:
        investigador.programa_incentivos_id = data["programa_incentivos_id"]

    if "grupo_utn_id" in data:
        investigador.grupo_utn_id = data["grupo_utn_id"]

    investigador.updated_by = user_id

    try:
        db.session.commit()
        return investigador
    except Exception:
        db.session.rollback()
        raise


# =====================================================
# DELETE (Soft Delete + cerrar historial)
# =====================================================

def eliminar_investigador(id, user_id):

    investigador = Investigador.query.filter(
        Investigador.deleted_at.is_(None),
        Investigador.id == id
    ).first()

    if not investigador:
        raise ValueError("Investigador no encontrado.")

    # Cerrar historial activo
    historial_activo = next(
        (h for h in investigador.historial_horas if h.fecha_fin is None),
        None
    )

    if historial_activo:
        historial_activo.fecha_fin = date.today()

    investigador.activo = False
    investigador.soft_delete(user_id)

    db.session.commit()

    return {
        "message": "Investigador eliminado correctamente.",
        "id": investigador.id
    }


# =====================================================
# RESTAURAR
# =====================================================

def restaurar_investigador(id):

    investigador = db.session.query(Investigador).filter(
        Investigador.deleted_at.isnot(None),
        Investigador.id == id
    ).first()

    if not investigador:
        raise ValueError("No existe investigador eliminado para restaurar.")

    investigador.restore()
    investigador.activo = True

    db.session.commit()

    return investigador


# =====================================================
# LISTAR
# =====================================================

def listar_investigadores(activos=None):

    query = Investigador.query

    if activos == "true":
        query = query.filter(Investigador.deleted_at.is_(None))
    elif activos == "false":
        query = query.filter(Investigador.deleted_at.isnot(None))
    else:
        query = query.filter(Investigador.deleted_at.is_(None))

    return query.all()


# =====================================================
# OBTENER POR ID
# =====================================================

def obtener_investigador_por_id(id):

    investigador = Investigador.query.get(id)

    if not investigador:
        raise ValueError("Investigador no encontrado.")

    return investigador