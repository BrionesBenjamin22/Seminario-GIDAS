from core.models.actividad_docencia import ActividadDocencia, GradoAcademico, RolActividad, InvestigadorActividadGrado
from core.models.personal import Investigador
from extension import db
from datetime import datetime, date


class ActividadDocenciaService:

    # -------------------------------------------------
    # Helpers
    # -------------------------------------------------

    @staticmethod
    def _get_or_404(model, obj_id, message):
        obj = db.session.get(model, obj_id)
        if not obj or getattr(obj, "deleted_at", None) is not None:
            raise Exception(message)
        return obj

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
    # Queries
    # -------------------------------------------------

    @staticmethod
    def get_all(filters: dict = None):
        query = ActividadDocencia.query.filter(
            ActividadDocencia.deleted_at.is_(None)
        )

        if filters:
            investigador_id = filters.get("investigador_id")
            if investigador_id:
                query = query.filter(
                    ActividadDocencia.investigador_id == investigador_id
                )

            orden = filters.get("orden")
            if orden == "asc":
                query = query.order_by(ActividadDocencia.fecha_inicio.asc())
            else:
                query = query.order_by(ActividadDocencia.fecha_inicio.desc())
        else:
            query = query.order_by(ActividadDocencia.fecha_inicio.desc())

        return [a.serialize() for a in query.all()]

    @staticmethod
    def get_by_id(actividad_id: int):
        actividad = db.session.get(ActividadDocencia, actividad_id)

        if not actividad or actividad.deleted_at is not None:
            raise Exception("Actividad de docencia no encontrada")

        return actividad.serialize()

    # -------------------------------------------------
    # Create
    # -------------------------------------------------

    @staticmethod
    def create(data: dict, user_id: int):

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

        curso = ActividadDocenciaService._validar_texto(
            data.get("curso"), "curso", min_len=3
        )

        institucion = ActividadDocenciaService._validar_texto(
            data.get("institucion"), "institucion", min_len=3
        )

        grado = ActividadDocenciaService._get_or_404(
            GradoAcademico,
            data.get("grado_academico_id"),
            "Grado Académico inválido"
        )

        rol = ActividadDocenciaService._get_or_404(
            RolActividad,
            data.get("rol_actividad_id"),
            "Rol de actividad inválido"
        )

        investigador = ActividadDocenciaService._get_or_404(
            Investigador,
            data.get("investigador_id"),
            "Investigador inválido"
        )

        actividad = ActividadDocencia(
            curso=curso,
            institucion=institucion,
            fecha_inicio=fecha_inicio,
            fecha_fin=fecha_fin,
            rol_actividad_id=rol.id,
            investigador_id=investigador.id,
            created_by=user_id
        )

        db.session.add(actividad)
        db.session.flush()  

        historial = InvestigadorActividadGrado(
            investigador_id=investigador.id,
            actividad_docencia_id=actividad.id,
            grado_academico_id=grado.id,
            fecha_inicio=fecha_inicio,
            fecha_fin=None,
            created_by=user_id
        )

        db.session.add(historial)

        try:
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise e

        return actividad.serialize()

    # -------------------------------------------------
    # Update
    # -------------------------------------------------

    @staticmethod
    def update(actividad_id: int, data: dict):
        actividad = db.session.get(ActividadDocencia, actividad_id)

        if not actividad or actividad.deleted_at is not None:
            raise Exception("Actividad de docencia no encontrada")

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

            nuevo_grado = ActividadDocenciaService._get_or_404(
                GradoAcademico,
                data["grado_academico_id"],
                "Grado Académico inválido"
            )

            # Buscar grado activo actual
            historial_activo = InvestigadorActividadGrado.query.filter_by(
                investigador_id=actividad.investigador_id,
                actividad_docencia_id=actividad.id,
                fecha_fin=None
            ).first()

            # Si existe y es distinto → cerrar y abrir nuevo
            if historial_activo and historial_activo.grado_academico_id != nuevo_grado.id:

                historial_activo.fecha_fin = date.today()

                nuevo_historial = InvestigadorActividadGrado(
                    investigador_id=actividad.investigador_id,
                    actividad_docencia_id=actividad.id,
                    grado_academico_id=nuevo_grado.id,
                    fecha_inicio=date.today(),
                    fecha_fin=None,
                    created_by=data.get("user_id")
                )

                db.session.add(nuevo_historial)

        if "rol_actividad_id" in data:
            rol = ActividadDocenciaService._get_or_404(
                RolActividad,
                data["rol_actividad_id"],
                "Rol de actividad inválido"
            )
            actividad.rol_actividad_id = rol.id

        if "investigador_id" in data:
            investigador = ActividadDocenciaService._get_or_404(
                Investigador,
                data["investigador_id"],
                "Investigador inválido"
            )
            actividad.investigador_id = investigador.id

        db.session.commit()
        return actividad.serialize()

    # -------------------------------------------------
    # Soft Delete
    # -------------------------------------------------

    @staticmethod
    def delete(actividad_id: int, user_id: int):
        actividad = db.session.get(ActividadDocencia, actividad_id)

        if not actividad or actividad.deleted_at is not None:
            raise Exception("Actividad de docencia no encontrada")

        actividad.soft_delete(user_id)

        db.session.commit()

        return {"message": "Actividad de docencia eliminada correctamente"}