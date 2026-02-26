from datetime import datetime
from sqlalchemy import extract, or_
from extension import db
from core.models.becas import Beca, Beca_Becario
from core.models.personal import Becario


# =====================================================
# HELPERS
# =====================================================

def _get_beca_activa_or_404(beca_id: int):
    beca = db.session.get(Beca, beca_id)
    if not beca or beca.deleted_at is not None:
        raise ValueError("Beca no encontrada.")
    return beca


def _get_relacion_activa(beca_id: int, becario_id: int):
    return Beca_Becario.query.filter(
        Beca_Becario.id_beca == beca_id,
        Beca_Becario.id_becario == becario_id,
        Beca_Becario.deleted_at.is_(None)
    ).first()


# =====================================================
# CRUD BECA
# =====================================================

class BecaService:

    @staticmethod
    def get_all():
        becas = Beca.query.filter(Beca.deleted_at.is_(None)).all()
        return [b.serialize() for b in becas]

    @staticmethod
    def get_by_id(beca_id):
        beca = _get_beca_activa_or_404(beca_id)
        return beca.serialize()

    @staticmethod
    def create(data, user_id):

        if not data.get("nombre_beca"):
            raise ValueError("El nombre de la beca es obligatorio.")

        nueva_beca = Beca(
            nombre_beca=data["nombre_beca"],
            descripcion=data.get("descripcion"),
            fuente_financiamiento_id=data.get("fuente_financiamiento_id"),
            created_by=user_id
        )

        db.session.add(nueva_beca)
        db.session.commit()

        return nueva_beca.serialize()

    @staticmethod
    def update(beca_id, data):
        beca = _get_beca_activa_or_404(beca_id)

        if "nombre_beca" in data:
            beca.nombre_beca = data["nombre_beca"]

        if "descripcion" in data:
            beca.descripcion = data["descripcion"]

        if "fuente_financiamiento_id" in data:
            beca.fuente_financiamiento_id = data["fuente_financiamiento_id"]

        db.session.commit()
        return beca.serialize()

    @staticmethod
    def delete(beca_id, user_id):
        beca = _get_beca_activa_or_404(beca_id)

        beca.soft_delete(user_id)
        db.session.commit()

        return {"message": "Beca eliminada correctamente."}


# =====================================================
# VINCULAR BECARIO
# =====================================================

    @staticmethod
    def vincular_becario(beca_id, data, user_id):

        beca = _get_beca_activa_or_404(beca_id)

        becario = db.session.get(Becario, data.get("id_becario"))
        if not becario or becario.deleted_at is not None:
            raise ValueError("Becario no encontrado.")

        try:
            fecha_inicio = datetime.strptime(data["fecha_inicio"], "%Y-%m-%d").date()
        except:
            raise ValueError("Formato de fecha_inicio inválido.")

        fecha_fin = None
        if data.get("fecha_fin"):
            fecha_fin = datetime.strptime(data["fecha_fin"], "%Y-%m-%d").date()

        existe = _get_relacion_activa(beca.id, becario.id)
        if existe:
            raise ValueError("El becario ya está vinculado a esta beca.")

        relacion = Beca_Becario(
            id_beca=beca.id,
            id_becario=becario.id,
            fecha_inicio=fecha_inicio,
            fecha_fin=fecha_fin,
            monto_percibido=data.get("monto_percibido"),
            created_by=user_id
        )

        db.session.add(relacion)
        db.session.commit()

        return {"message": "Becario vinculado correctamente."}


# =====================================================
# DESVINCULAR (SOFT DELETE)
# =====================================================

    @staticmethod
    def desvincular_becario(beca_id, becario_id, user_id):

        relacion = _get_relacion_activa(beca_id, becario_id)

        if not relacion:
            raise ValueError("La relación no existe.")

        relacion.soft_delete(user_id)
        db.session.commit()

        return {"message": "Becario desvinculado correctamente."}


# =====================================================
# LISTAR BECARIOS DE UNA BECA
# =====================================================

    @staticmethod
    def get_becarios_de_beca(beca_id):

        beca = _get_beca_activa_or_404(beca_id)

        resultado = []
        for r in beca.becarios:
            if r.deleted_at is None:
                resultado.append({
                    "id_becario": r.becario.id,
                    "nombre": r.becario.nombre_apellido,
                    "fecha_inicio": r.fecha_inicio,
                    "fecha_fin": r.fecha_fin,
                    "monto_percibido": r.monto_percibido
                })

        return resultado
    
    
    # =========================
    # DASHBOARD POR AÑO (AUDITORÍA)
    # =========================
    @staticmethod
    def dashboard_por_anio(anio: int):

        if not anio:
            raise ValueError("Debe proporcionar un año.")

        relaciones = (
            Beca_Becario.query
            .join(Beca, Beca.id == Beca_Becario.id_beca)
            .join(Becario, Becario.id == Beca_Becario.id_becario)
            .filter(
                # SOLO registros activos
                Beca.deleted_at.is_(None),
                Becario.deleted_at.is_(None),
                Beca_Becario.deleted_at.is_(None),

                # Rango temporal
                extract("year", Beca_Becario.fecha_inicio) <= anio,
                or_(
                    Beca_Becario.fecha_fin == None,
                    extract("year", Beca_Becario.fecha_fin) >= anio
                )
            )
            .all()
        )

        if not relaciones:
            return {
                "anio": anio,
                "total_becarios_activos": 0,
                "monto_total_invertido": 0,
                "promedio_monto": 0,
                "por_tipo_formacion": {},
                "por_grupo": {}
            }

        total_becarios = len(relaciones)

        monto_total = sum(
            r.monto_percibido or 0
            for r in relaciones
        )

        promedio = monto_total / total_becarios if total_becarios else 0

        # Agrupar por tipo de formación
        por_tipo = {}
        for r in relaciones:
            tipo = r.becario.tipo_formacion.nombre
            por_tipo[tipo] = por_tipo.get(tipo, 0) + 1

        # Agrupar por grupo
        por_grupo = {}
        for r in relaciones:
            grupo = r.becario.grupo_utn.nombre_sigla_grupo
            por_grupo[grupo] = por_grupo.get(grupo, 0) + 1

        return {
            "anio": anio,
            "total_becarios_activos": total_becarios,
            "monto_total_invertido": monto_total,
            "promedio_monto": round(promedio, 2),
            "por_tipo_formacion": por_tipo,
            "por_grupo": por_grupo
        }