from extension import db
from core.models.personal import Becario
from core.models.grupo import GrupoInvestigacionUtn
from core.models.fuente_financiamiento import FuenteFinanciamiento
from core.models.personal import TipoFormacion
from core.models.proyecto_investigacion import ProyectoInvestigacion


def crear_becario(data):
    if not data:
        raise ValueError("Los datos no pueden estar vacíos.")

    nombre = data.get("nombre_apellido")
    horas = data.get("horas_semanales")
    tipo_formacion_id = data.get("tipo_formacion_id")
    grupo_utn_id = data.get("grupo_utn_id")
    fuente_id = data.get("fuente_financiamiento_id")
    proyectos_ids = data.get("proyectos", [])

    if not nombre or not isinstance(nombre, str):
        raise ValueError("El nombre y apellido es obligatorio.")

    if not isinstance(horas, int) or horas <= 0:
        raise ValueError("Las horas semanales deben ser un número positivo.")

    if not TipoFormacion.query.get(tipo_formacion_id):
        raise ValueError("Tipo de formación inválido.")

    if grupo_utn_id and not GrupoInvestigacionUtn.query.get(grupo_utn_id):
        raise ValueError("Grupo UTN inválido.")

    if fuente_id and not FuenteFinanciamiento.query.get(fuente_id):
        raise ValueError("Fuente de financiamiento inválida.")

    becario = Becario(
        nombre_apellido=nombre.strip(),
        horas_semanales=horas,
        tipo_formacion_id=tipo_formacion_id,
        grupo_utn_id=grupo_utn_id,
        fuente_financiamiento_id=fuente_id,
        activo=True
    )

    # Asignar proyectos (M:N)
    if proyectos_ids:
        proyectos = ProyectoInvestigacion.query.filter(
            ProyectoInvestigacion.id.in_(proyectos_ids)
        ).all()

        if len(proyectos) != len(proyectos_ids):
            raise ValueError("Uno o más proyectos son inválidos.")

        becario.proyectos.extend(proyectos)


    db.session.add(becario)
    try:
        db.session.commit()
        return becario
    except Exception:
        db.session.rollback()
        raise


def actualizar_becario(id, data):
    becario = Becario.query.get(id)
    if not becario:
        raise ValueError("Becario no encontrado.")


    if "activo" in data:
        if not isinstance(data["activo"], bool):
            raise ValueError("El campo 'activo' debe ser booleano.")

        # Si no cambia el estado
        if becario.activo == data["activo"]:
            estado = "activo" if becario.activo else "inactivo"
            raise ValueError(f"El becario ya se encuentra {estado}.")

        becario.activo = data["activo"]

        try:
            db.session.commit()
            return becario
        except Exception:
            db.session.rollback()
            raise

    if not becario.activo:
        raise ValueError(
            "No se puede modificar un becario dado de baja. Reactívelo primero."
        )

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

    if "fuente_financiamiento_id" in data:
        if data["fuente_financiamiento_id"] and not FuenteFinanciamiento.query.get(data["fuente_financiamiento_id"]):
            raise ValueError("Fuente de financiamiento inválida.")
        becario.fuente_financiamiento_id = data["fuente_financiamiento_id"]

    # Reemplazar proyectos
    if "proyectos" in data:
        proyectos_ids = data["proyectos"]

        if not isinstance(proyectos_ids, list):
            raise ValueError("El campo 'proyectos' debe ser una lista de IDs.")

        proyectos = ProyectoInvestigacion.query.filter(
            ProyectoInvestigacion.id.in_(proyectos_ids)
        ).all()

        if len(proyectos) != len(proyectos_ids):
            raise ValueError("Uno o más proyectos son inválidos.")

        becario.proyectos = proyectos


    try:
        db.session.commit()
        return becario
    except Exception:
        db.session.rollback()
        raise


def eliminar_becario(id):
    becario = Becario.query.get(id)
    if not becario:
        raise ValueError("Becario no encontrado.")

    if not becario.activo:
        raise ValueError("El becario ya se encuentra dado de baja.")

    becario.activo = False

    try:
        db.session.commit()
    except Exception:
        db.session.rollback()
        raise

    return {
        "message": "Becario dado de baja correctamente.",
        "id": becario.id
    }




def listar_becarios(activos=None):
    query = Becario.query

    if activos == "true":
        query = query.filter_by(activo=True)
    elif activos == "false":
        query = query.filter_by(activo=False)
    elif activos == "all":
        pass  
    else:
        
        query = query.filter_by(activo=True)

    return query.all()



def obtener_becario_por_id(id):
    becario = Becario.query.get(id)
    if not becario:
        raise ValueError("Becario no encontrado.")
    return becario
