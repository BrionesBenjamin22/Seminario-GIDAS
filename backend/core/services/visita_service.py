from extension import db
from core.models.visita_grupo import VisitaAcademica
from core.models.grupo import GrupoInvestigacionUtn
from datetime import  datetime


def crear_visita_academica(data):
    if not data:
        raise ValueError("Los datos no pueden estar vacíos.")

    razon = data.get("razon")
    fecha_str = data.get("fecha")
    procedencia_visita_id = data.get("procedencia_visita_id")
    tipo_visita_id = data.get("tipo_visita_id")
    grupo_utn_id = data.get("grupo_utn_id")

    if not tipo_visita_id:
        raise ValueError("El tipo de visita es obligatorio.")

    if not procedencia_visita_id:
        raise ValueError("La procedencia de la visita es obligatoria.")
    
    if not razon or not isinstance(razon, str):
        raise ValueError("La razón es obligatoria.")

    if not fecha_str:
        raise ValueError("La fecha es obligatoria.")

    
    try:
        fecha = datetime.strptime(fecha_str, "%Y-%m-%d").date()
    except ValueError:
        raise ValueError("El formato de la fecha debe ser YYYY-MM-DD.")

    if not grupo_utn_id:
        raise ValueError("El grupo UTN es obligatorio.")

    grupo = GrupoInvestigacionUtn.query.get(grupo_utn_id)
    if not grupo:
        raise ValueError("Grupo UTN inválido.")

    visita = VisitaAcademica(
        tipo_visita_id=tipo_visita_id,
        razon=razon.strip(),
        procedencia_visita_id=procedencia_visita_id,
        fecha=fecha,  
        grupo_utn_id=grupo_utn_id
    )

    db.session.add(visita)
    try:
        db.session.commit()
        return visita
    except Exception:
        db.session.rollback()
        raise


def actualizar_visita_academica(id, data):
    visita = VisitaAcademica.query.get(id)
    if not visita:
        raise ValueError("Visita académica no encontrada.")

    if "tipo_visita_id" in data:
        visita.tipo_visita_id = data["tipo_visita_id"]

    if "razon" in data:
        visita.razon = data["razon"].strip()

    if "procedencia_visita_id" in data:
        visita.procedencia_visita_id = data["procedencia_visita_id"]

    if "fecha" in data:
        visita.fecha = data["fecha"]

    try:
        db.session.commit()
        return visita
    except Exception:
        db.session.rollback()
        raise


def eliminar_visita_academica(id):
    visita = VisitaAcademica.query.get(id)
    if not visita:
        raise ValueError("Visita académica no encontrada.")

    db.session.delete(visita)
    db.session.commit()


def listar_visitas():
    return VisitaAcademica.query.all()


def obtener_visita_por_id(id):
    visita = VisitaAcademica.query.get(id)
    if not visita:
        raise ValueError("Visita académica no encontrada.")
    return visita
