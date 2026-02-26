from datetime import datetime
from sqlalchemy import extract, or_
from extension import db
from core.models.becas import Beca, Beca_Becario
from core.models.personal import Becario


class BecaService:
    
    
    @staticmethod
    def get_becas_activas_en_anio(anio):
        if not anio:
            raise ValueError("Debe proporcionar un año.")

        relaciones = Beca_Becario.query.filter(
            extract("year", Beca_Becario.fecha_inicio) <= anio,
            (
                Beca_Becario.fecha_fin == None
            ) |
            (extract("year", Beca_Becario.fecha_fin) >= anio)
        ).all()

        resultado = []

        for r in relaciones:
            resultado.append({
                "beca_id": r.beca.id,
                "nombre_beca": r.beca.nombre_beca,
                "becario": r.becario.nombre_apellido,
                "anio_consultado": anio,
                "fecha_inicio": str(r.fecha_inicio),
                "fecha_fin": str(r.fecha_fin) if r.fecha_fin else None,
                "monto_percibido": r.monto_percibido
            })

        return resultado

    # =========================
    # CRUD BECA
    # =========================
    
    

    @staticmethod
    def get_all():
        becas = Beca.query.all()
        return [b.serialize() for b in becas]

    @staticmethod
    def get_by_id(beca_id):
        beca = Beca.query.get(beca_id)
        if not beca:
            raise ValueError("Beca no encontrada.")
        return beca.serialize()

    @staticmethod
    def create(data):
        if not data.get("nombre_beca"):
            raise ValueError("El nombre de la beca es obligatorio.")

        nueva_beca = Beca(
            nombre_beca=data["nombre_beca"],
            descripcion=data.get("descripcion"),
            fuente_financiamiento_id=data.get("fuente_financiamiento_id")
        )

        db.session.add(nueva_beca)
        db.session.commit()

        return nueva_beca.serialize()

    @staticmethod
    def update(beca_id, data):
        beca = Beca.query.get(beca_id)
        if not beca:
            raise ValueError("Beca no encontrada.")

        if "nombre_beca" in data:
            beca.nombre_beca = data["nombre_beca"]

        if "descripcion" in data:
            beca.descripcion = data["descripcion"]

        if "fuente_financiamiento_id" in data:
            beca.fuente_financiamiento_id = data["fuente_financiamiento_id"]

        db.session.commit()
        return beca.serialize()

    @staticmethod
    def delete(beca_id):
        beca = Beca.query.get(beca_id)
        if not beca:
            raise ValueError("Beca no encontrada.")

        db.session.delete(beca)
        db.session.commit()

        return {"message": "Beca eliminada correctamente."}


    # =========================
    # VINCULAR BECARIOS
    # =========================

    @staticmethod
    def vincular_becario(beca_id, data):
        """
        data esperado:
        {
            "id_becario": int,
            "fecha_inicio": "YYYY-MM-DD",
            "fecha_fin": "YYYY-MM-DD" (opcional),
            "monto_percibido": float (opcional)
        }
        """

        beca = Beca.query.get(beca_id)
        if not beca:
            raise ValueError("Beca no encontrada.")

        becario = Becario.query.get(data.get("id_becario"))
        if not becario:
            raise ValueError("Becario no encontrado.")

        # Convertir fechas
        try:
            fecha_inicio = datetime.strptime(data["fecha_inicio"], "%Y-%m-%d").date()
        except:
            raise ValueError("Formato de fecha_inicio inválido. Usar YYYY-MM-DD.")

        fecha_fin = None
        if data.get("fecha_fin"):
            try:
                fecha_fin = datetime.strptime(data["fecha_fin"], "%Y-%m-%d").date()
            except:
                raise ValueError("Formato de fecha_fin inválido. Usar YYYY-MM-DD.")
            
        existe = Beca_Becario.query.filter_by(
            id_beca=beca.id,
            id_becario=becario.id
        ).first()

        if existe:
            raise ValueError("El becario ya está vinculado a esta beca.")

        # Crear vínculo
        relacion = Beca_Becario(
            id_beca=beca.id,
            id_becario=becario.id,
            fecha_inicio=fecha_inicio,
            fecha_fin=fecha_fin,
            monto_percibido=data.get("monto_percibido")
        )

        db.session.add(relacion)
        db.session.commit()

        return {
            "message": "Becario vinculado correctamente a la beca."
        }


    # =========================
    # DESVINCULAR BECARIO
    # =========================

    @staticmethod
    def desvincular_becario(beca_id, becario_id):
        relacion = Beca_Becario.query.filter_by(
            id_beca=beca_id,
            id_becario=becario_id
        ).first()

        if not relacion:
            raise ValueError("La relación entre beca y becario no existe.")

        db.session.delete(relacion)
        db.session.commit()

        return {"message": "Becario desvinculado correctamente."}


    # =========================
    # LISTAR BECARIOS DE UNA BECA
    # =========================

    @staticmethod
    def get_becarios_de_beca(beca_id):
        beca = Beca.query.get(beca_id)
        if not beca:
            raise ValueError("Beca no encontrada.")

        resultado = []
        for relacion in beca.becarios:
            resultado.append({
                "id_becario": relacion.becario.id,
                "nombre": relacion.becario.nombre_apellido,
                "fecha_inicio": relacion.fecha_inicio,
                "fecha_fin": relacion.fecha_fin,
                "monto_percibido": relacion.monto_percibido
            })

        return resultado
    
    

    # =========================
    # DASHBOARD POR AÑO
    # =========================
    @staticmethod
    def dashboard_por_anio(anio):
        if not anio:
            raise ValueError("Debe proporcionar un año.")

        relaciones = Beca_Becario.query.join(Becario).filter(
            extract("year", Beca_Becario.fecha_inicio) <= anio,
            or_(
                Beca_Becario.fecha_fin == None,
                extract("year", Beca_Becario.fecha_fin) >= anio
            )
        ).all()

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