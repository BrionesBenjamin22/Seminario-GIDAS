from extension import db
from core.models.visita_grupo import VisitaAcademica
from core.models.grupo import GrupoInvestigacionUtn
from datetime import  datetime


def crear_visita_academica(data):
    if not data:
        raise ValueError("Los datos no pueden estar vacíos.")

    tipo_visita = data.get("tipo_visita")
    razon = data.get("razon")
    procedencia = data.get("procedencia")
    fecha_str = data.get("fecha")
    grupo_utn_id = data.get("grupo_utn_id")

    if not tipo_visita or not isinstance(tipo_visita, str):
        raise ValueError("El tipo de visita es obligatorio.")

    if not razon or not isinstance(razon, str):
        raise ValueError("La razón es obligatoria.")

    if not procedencia or not isinstance(procedencia, str):
        raise ValueError("La procedencia es obligatoria.")

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
        tipo_visita=tipo_visita.strip(),
        razon=razon.strip(),
        procedencia=procedencia.strip(),
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

    if "tipo_visita" in data:
        visita.tipo_visita = data["tipo_visita"].strip()

    if "razon" in data:
        visita.razon = data["razon"].strip()

    if "procedencia" in data:
        visita.procedencia = data["procedencia"].strip()

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
