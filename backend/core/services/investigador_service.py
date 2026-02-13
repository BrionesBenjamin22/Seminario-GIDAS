from extension import db
from core.models.personal import Investigador
from core.models.personal import TipoDedicacion
from core.models.categoria_utn import CategoriaUtn
from core.models.programa_incentivos import ProgramaIncentivos
from core.models.grupo import GrupoInvestigacionUtn
from core.models.proyecto_investigacion import ProyectoInvestigacion
from sqlalchemy.exc import IntegrityError


def crear_investigador(data):
    if not data:
        raise ValueError("Los datos no pueden estar vacíos.")

    nombre = data.get("nombre_apellido")
    horas = data.get("horas_semanales")
    tipo_dedicacion_id = data.get("tipo_dedicacion_id")
    categoria_utn_id = data.get("categoria_utn_id")
    programa_id = data.get("programa_incentivos_id")
    grupo_utn_id = data.get("grupo_utn_id")
    proyectos_ids = data.get("proyectos", [])

    # ---- Validaciones obligatorias ----
    if not nombre or not isinstance(nombre, str):
        raise ValueError("El nombre y apellido es obligatorio.")

    if not isinstance(horas, int) or horas <= 0:
        raise ValueError("Las horas semanales deben ser un número positivo.")

    if not tipo_dedicacion_id:
        raise ValueError("El tipo de dedicación es obligatorio.")

    tipo_dedicacion = TipoDedicacion.query.get(tipo_dedicacion_id)
    if not tipo_dedicacion:
        raise ValueError("Tipo de dedicación inválido.")

    # ---- Validaciones opcionales ----
    if categoria_utn_id and not CategoriaUtn.query.get(categoria_utn_id):
        raise ValueError("Categoría UTN inválida.")

    if programa_id and not ProgramaIncentivos.query.get(programa_id):
        raise ValueError("Programa de incentivos inválido.")

    if grupo_utn_id and not GrupoInvestigacionUtn.query.get(grupo_utn_id):
        raise ValueError("Grupo UTN inválido.")

    investigador = Investigador(
        nombre_apellido=nombre.strip(),
        horas_semanales=horas,
        tipo_dedicacion_id=tipo_dedicacion_id,
        categoria_utn_id=categoria_utn_id,
        programa_incentivos_id=programa_id,
        grupo_utn_id=grupo_utn_id,
        activo = True
    )

    # ---- Relación M:N proyectos ----
    if proyectos_ids:
        proyectos = ProyectoInvestigacion.query.filter(
            ProyectoInvestigacion.id.in_(proyectos_ids)
        ).all()

        if len(proyectos) != len(proyectos_ids):
            raise ValueError("Uno o más proyectos son inválidos.")

        investigador.proyectos.extend(proyectos)

    db.session.add(investigador)
    try:
        db.session.commit()
        return investigador
    except IntegrityError:
        db.session.rollback()
        raise ValueError("Error de integridad al crear el investigador.")



def actualizar_investigador(id, data):
    investigador = Investigador.query.get(id)
    if not investigador:
        raise ValueError("Investigador no encontrado.")

  
    if "activo" in data:
        if not isinstance(data["activo"], bool):
            raise ValueError("El campo 'activo' debe ser booleano.")

        if investigador.activo != data["activo"]:
            investigador.activo = data["activo"]
            db.session.commit()
            return investigador
  
    if not investigador.activo:
        raise ValueError(
            "No se puede modificar un investigador dado de baja. Reactívelo primero."
        )

    if "nombre_apellido" in data:
        nombre = data["nombre_apellido"]
        if not nombre or not isinstance(nombre, str):
            raise ValueError("Nombre inválido.")
        investigador.nombre_apellido = nombre.strip()

    if "horas_semanales" in data:
        horas = data["horas_semanales"]
        if not isinstance(horas, int) or horas <= 0:
            raise ValueError("Horas inválidas.")
        investigador.horas_semanales = horas

    # ---- Tipo de dedicación (NO puede quedar null) ----
    if "tipo_dedicacion_id" in data:
        if not data["tipo_dedicacion_id"]:
            raise ValueError("El tipo de dedicación no puede ser nulo.")

        tipo = TipoDedicacion.query.get(data["tipo_dedicacion_id"])
        if not tipo:
            raise ValueError("Tipo de dedicación inválido.")

        investigador.tipo_dedicacion_id = data["tipo_dedicacion_id"]

    # ---- Opcionales ----
    if "categoria_utn_id" in data:
        if data["categoria_utn_id"] and not CategoriaUtn.query.get(data["categoria_utn_id"]):
            raise ValueError("Categoría UTN inválida.")
        investigador.categoria_utn_id = data["categoria_utn_id"]

    if "programa_incentivos_id" in data:
        if data["programa_incentivos_id"] and not ProgramaIncentivos.query.get(data["programa_incentivos_id"]):
            raise ValueError("Programa de incentivos inválido.")
        investigador.programa_incentivos_id = data["programa_incentivos_id"]

    if "grupo_utn_id" in data:
        if data["grupo_utn_id"] and not GrupoInvestigacionUtn.query.get(data["grupo_utn_id"]):
            raise ValueError("Grupo UTN inválido.")
        investigador.grupo_utn_id = data["grupo_utn_id"]

    # ---- Proyectos (M:N) ----
    if "proyectos" in data:
        proyectos_ids = data["proyectos"]

        if not isinstance(proyectos_ids, list):
            raise ValueError("El campo 'proyectos' debe ser una lista de IDs.")

        proyectos = ProyectoInvestigacion.query.filter(
            ProyectoInvestigacion.id.in_(proyectos_ids)
        ).all()

        if len(proyectos) != len(proyectos_ids):
            raise ValueError("Uno o más proyectos son inválidos.")

        investigador.proyectos = proyectos

    try:
        db.session.commit()
        return investigador
    except Exception:
        db.session.rollback()
        raise



def eliminar_investigador(id):
    investigador = Investigador.query.get(id)
    if not investigador:
        raise ValueError("Investigador no encontrado.")
    
    if not investigador.activo:
        raise ValueError("El investigador ya se encuentra dado de baja.")

    investigador.activo = False

    db.session.commit()
    return {
        "message": "Investigador dado de baja correctamente",
        "id": investigador.id
    }


def reactivar_investigador(id):
    investigador = Investigador.query.get(id)
    if not investigador:
        raise ValueError("Investigador no encontrado.")

    investigador.activo = True
    db.session.commit()

    return investigador.serialize()

def listar_investigadores(activos=None):
    query = Investigador.query

    if activos == "true":
        query = query.filter_by(activo=True)
    elif activos == "false":
        query = query.filter_by(activo=False)
    elif activos == "all":
        pass
    else:
        query = query.filter_by(activo=True)

    return query.all()



def obtener_investigador_por_id(id):
    investigador = Investigador.query.get(id)
    if not investigador:
        raise ValueError("Investigador no encontrado.")
    return investigador
