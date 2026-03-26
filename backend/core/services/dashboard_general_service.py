from sqlalchemy import func
from extension import db

from core.models.personal import Personal, Becario, Investigador
from core.models.proyecto_investigacion import ProyectoInvestigacion, TipoProyecto
from core.models.becas import Beca_Becario


class DashboardGeneralService:

    @staticmethod
    def get_resumen():
        # =========================
        # PERSONAL
        # =========================
        total_personal_ptaa = Personal.query.filter(
            Personal.deleted_at.is_(None)
        ).count()

        total_becarios = Becario.query.filter(
            Becario.deleted_at.is_(None)
        ).count()

        total_investigadores = Investigador.query.filter(
            Investigador.deleted_at.is_(None)
        ).count()

        # Si más adelante tenés Profesional separado, acá lo sumás
        total_profesionales = 0

        total_personal = (
            total_personal_ptaa
            + total_becarios
            + total_investigadores
            + total_profesionales
        )

        # =========================
        # PROYECTOS
        # =========================
        total_proyectos = ProyectoInvestigacion.query.filter(
            ProyectoInvestigacion.deleted_at.is_(None)
        ).count()

        proyectos_activos = ProyectoInvestigacion.query.filter(
            ProyectoInvestigacion.deleted_at.is_(None),
            ProyectoInvestigacion.fecha_fin.is_(None)
        ).count()

        proyectos_cerrados = ProyectoInvestigacion.query.filter(
            ProyectoInvestigacion.deleted_at.is_(None),
            ProyectoInvestigacion.fecha_fin.isnot(None)
        ).count()

        # =========================
        # BECARIOS CON / SIN BECA
        # =========================
        subquery_becarios_con_beca = (
            db.session.query(Beca_Becario.id_becario)
            .filter(Beca_Becario.deleted_at.is_(None))
            .distinct()
            .subquery()
        )

        becarios_con_beca = db.session.query(func.count()).select_from(
            subquery_becarios_con_beca
        ).scalar() or 0

        becarios_sin_beca = max(total_becarios - becarios_con_beca, 0)

        # =========================
        # PROYECTOS POR TIPO
        # =========================
        proyectos_por_tipo_query = (
            db.session.query(
                TipoProyecto.nombre,
                func.count(ProyectoInvestigacion.id)
            )
            .outerjoin(
                ProyectoInvestigacion,
                (ProyectoInvestigacion.tipo_proyecto_id == TipoProyecto.id)
                & (ProyectoInvestigacion.deleted_at.is_(None))
            )
            .group_by(TipoProyecto.nombre)
            .order_by(TipoProyecto.nombre.asc())
            .all()
        )

        proyectos_por_tipo = [
            {
                "label": nombre,
                "value": cantidad
            }
            for nombre, cantidad in proyectos_por_tipo_query
        ]

        return {
            "kpis": {
                "total_personal": total_personal,
                "total_investigadores": total_investigadores,
                "total_becarios": total_becarios,
                "total_ptaa": total_personal_ptaa,
                "total_profesionales": total_profesionales,
                "total_proyectos": total_proyectos,
                "proyectos_activos": proyectos_activos,
                "proyectos_cerrados": proyectos_cerrados,
                "becarios_con_beca": becarios_con_beca,
                "becarios_sin_beca": becarios_sin_beca,
            },
            "charts": {
                "personal_por_rol": [
                    {
                        "label": "Investigadores",
                        "value": total_investigadores
                    },
                    {
                        "label": "Becarios",
                        "value": total_becarios
                    },
                    {
                        "label": "PTAA",
                        "value": total_personal_ptaa
                    },
                    {
                        "label": "Profesionales",
                        "value": total_profesionales
                    }
                ],
                "proyectos_por_estado": [
                    {
                        "label": "Activos",
                        "value": proyectos_activos
                    },
                    {
                        "label": "Cerrados",
                        "value": proyectos_cerrados
                    }
                ],
                "proyectos_por_tipo": proyectos_por_tipo,
                "becarios_por_beca": [
                    {
                        "label": "Con beca",
                        "value": becarios_con_beca
                    },
                    {
                        "label": "Sin beca",
                        "value": becarios_sin_beca
                    }
                ]
            }
        }