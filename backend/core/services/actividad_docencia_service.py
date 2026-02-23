from core.models.actividad_docencia import ActividadDocencia, GradoAcademico, RolActividad
from core.models.personal import Investigador
from extension import db
from datetime import datetime, date


class ActividadDocenciaService:

    # -------------------------------------------------
    # Validadores internos
    # -------------------------------------------------

    @staticmethod
    def _validar_texto(valor, campo, min_len=2, max_len=255):
        if valor is None:
            raise Exception(f"El campo '{campo}' es obligatorio")

        if not isinstance(valor, str):
            raise Exception(f"El campo '{campo}' debe ser texto")

        valor = valor.strip()

        if not valor:
            raise Exception(f"El campo '{campo}' no puede estar vacío")

        if len(valor) < min_len:
            raise Exception(
                f"El campo '{campo}' debe tener al menos {min_len} caracteres"
            )

        if len(valor) > max_len:
            raise Exception(
                f"El campo '{campo}' no puede superar los {max_len} caracteres"
            )

        return valor

    @staticmethod
    def _validar_fechas(fecha_inicio, fecha_fin):
        if fecha_inicio > date.today():
            raise Exception("La fecha de inicio no puede ser futura")

        if fecha_fin < fecha_inicio:
            raise Exception("La fecha de fin no puede ser anterior a la fecha de inicio")

    # -------------------------------------------------
    # CRUD
    # -------------------------------------------------

    @staticmethod
    def get_all(filters: dict = None):
        query = ActividadDocencia.query

        investigador_id = filters.get("investigador_id") if filters else None
        if investigador_id:
            query = query.filter(
                ActividadDocencia.investigador_id == investigador_id
            )
        orden = filters.get("orden") if filters else None
        if orden == "asc":
            query = query.order_by(ActividadDocencia.fecha_inicio.asc())
        else:
            query = query.order_by(ActividadDocencia.fecha_inicio.desc())

        return [a.serialize() for a in query.all()]

    @staticmethod
    def get_by_id(actividad_id: int):
        actividad = ActividadDocencia.query.get(actividad_id)
        if not actividad:
            raise Exception("Actividad de docencia no encontrada")
        return actividad.serialize()

    @staticmethod
    def create(data: dict):
        # ---- Validar fechas ----
        try:
            fecha_inicio = datetime.strptime(
                data["fecha_inicio"], "%Y-%m-%d"
            ).date()
            fecha_fin = datetime.strptime(
                data["fecha_fin"], "%Y-%m-%d"
            ).date()
        except (KeyError, ValueError):
            raise Exception(
                "Las fechas son obligatorias y deben tener formato YYYY-MM-DD"
            )

        ActividadDocenciaService._validar_fechas(fecha_inicio, fecha_fin)

        # ---- Validar textos ----
        curso = ActividadDocenciaService._validar_texto(
            data.get("curso"), "curso", min_len=3
        )

        institucion = ActividadDocenciaService._validar_texto(
            data.get("institucion"), "institucion", min_len=3
        )

        grado_academico_id = data.get("grado_academico_id")
        if not grado_academico_id or not GradoAcademico.query.get(grado_academico_id):
            raise Exception("Grado Academico Inválido")
        

        rol_actividad_id = data.get("rol_actividad_id")
        if not rol_actividad_id or not RolActividad.query.get(rol_actividad_id):
            raise Exception("Rol de Actividad Inválido")

        # ---- Validar relación ----
        investigador_id = data.get("investigador_id")
        if not investigador_id or not Investigador.query.get(investigador_id):
            raise Exception("Investigador inválido")

        actividad = ActividadDocencia(
            curso=curso,
            institucion=institucion,
            fecha_inicio=fecha_inicio,
            fecha_fin=fecha_fin,
            grado_academico_id=grado_academico_id,
            rol_actividad_id=rol_actividad_id,
            investigador_id=investigador_id
        )

        db.session.add(actividad)
        try:        
            db.session.commit()
        except Exception:
            db.session.rollback()
            raise Exception("Error al guardar la actividad")
        return actividad.serialize()

    @staticmethod
    def update(actividad_id: int, data: dict):
        actividad = ActividadDocencia.query.get(actividad_id)
        if not actividad:
            raise Exception("Actividad de docencia no encontrada")

        # ---- Update parcial ----
        if "fecha_inicio" in data or "fecha_fin" in data:
            try:
                fecha_inicio = datetime.strptime(
                    data.get("fecha_inicio", actividad.fecha_inicio.strftime("%Y-%m-%d")),
                    "%Y-%m-%d"
                ).date()
                fecha_fin = datetime.strptime(
                    data.get("fecha_fin", actividad.fecha_fin.strftime("%Y-%m-%d")),
                    "%Y-%m-%d"
                ).date()
            except ValueError:
                raise Exception("Las fechas deben tener formato YYYY-MM-DD")

            ActividadDocenciaService._validar_fechas(fecha_inicio, fecha_fin)

            actividad.fecha_inicio = fecha_inicio
            actividad.fecha_fin = fecha_fin

        if "curso" in data:
            actividad.curso = ActividadDocenciaService._validar_texto(
                data["curso"], "curso", min_len=3
            )

        if "institucion" in data:
            actividad.institucion = ActividadDocenciaService._validar_texto(
                data["institucion"], "institucion", min_len=3
            )

        if "grado_academico_id" in data:
            if not GradoAcademico.query.get(data["grado_academico_id"]):
                raise Exception("Grado Academico Inválido")
            actividad.grado_academico_id = data["grado_academico_id"]

        if "rol_actividad_id" in data:
            if not RolActividad.query.get(data["rol_actividad_id"]):
                raise Exception("Rol de Actividad Inválido")
            actividad.rol_actividad_id = data["rol_actividad_id"]

        if "investigador_id" in data:
            if not Investigador.query.get(data["investigador_id"]):
                raise Exception("Investigador inválido")
            actividad.investigador_id = data["investigador_id"]

        db.session.commit()
        return actividad.serialize()

    @staticmethod
    def delete(actividad_id: int):
        actividad = ActividadDocencia.query.get(actividad_id)
        if not actividad:
            raise Exception("Actividad de docencia no encontrada")

        db.session.delete(actividad)
        db.session.commit()
        return {"message": "Actividad de docencia eliminada correctamente"}
