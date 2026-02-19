from sqlalchemy import or_
from sqlalchemy.orm import joinedload
from datetime import datetime
from extension import db
from core.models.personal import Personal, Becario, Investigador
from core.models.proyecto_investigacion import ProyectoInvestigacion, BecarioProyecto, InvestigadorProyecto, TipoProyecto
from core.models.actividad_docencia import ActividadDocencia
from core.models.equipamiento import Equipamiento
import unicodedata


class SearchService:

    # ==================================================
    # FUNCIÓN DE NORMALIZACIÓN (quita acentos)
    # ==================================================
    @staticmethod
    def normalize_text(text: str) -> str:
        if not text:
            return ""
        return ''.join(
            c for c in unicodedata.normalize('NFD', text)
            if unicodedata.category(c) != 'Mn'
        ).lower()

    # ==================================================
    # SEARCH PRINCIPAL
    # ==================================================
    @staticmethod
    def search(query_text: str, orden: str = "alf_asc"):

        if not query_text or len(query_text.strip()) < 2:
            raise ValueError("El texto debe tener al menos 2 caracteres")

        query_normalized = SearchService.normalize_text(query_text.strip())
        resultados = []

        # ==================================================
        # PERSONAL
        # ==================================================
        personal_results = db.session.query(Personal)\
            .options(joinedload(Personal.tipo_personal))\
            .all()

        for p in personal_results:
            nombre_normalizado = SearchService.normalize_text(p.nombre_apellido)

            if query_normalized in nombre_normalizado:
                resultados.append({
                    "tipo": "Persona",
                    "id": p.id,
                    "titulo": p.nombre_apellido,
                    "subtitulo": p.tipo_personal.nombre if p.tipo_personal else None,
                    "fecha": None,
                    "url": f"/personal/{p.id}"
                })

        # ==================================================
        # BECARIOS
        # ==================================================
        becario_results = db.session.query(Becario)\
        .options(
            joinedload(Becario.tipo_formacion),
            joinedload(Becario.fuente_financiamiento),
            joinedload(Becario.participaciones_proyecto)
                .joinedload(BecarioProyecto.proyecto)
        )\
        .all()


        for b in becario_results:
            nombre_normalizado = SearchService.normalize_text(b.nombre_apellido)

            if query_normalized in nombre_normalizado:
                resultados.append({
                    "tipo": "Becario",
                    "id": b.id,
                    "titulo": b.nombre_apellido,
                    "subtitulo": b.tipo_formacion.nombre if b.tipo_formacion else None,
                    "fecha": None,
                    "url": f"/becarios/{b.id}",
                    "extra": {
                        "fuente_financiamiento": b.fuente_financiamiento.nombre
                            if b.fuente_financiamiento else None,
                        "proyectos": [
                            {
                                "id": p.proyecto.id,
                                "nombre": p.proyecto.nombre_proyecto,
                                "fecha_inicio": str(p.fecha_inicio),
                                "fecha_fin": str(p.fecha_fin) if p.fecha_fin else None
                            }
                            for p in b.participaciones_proyecto
                        ]

                    }
                })

        # ==================================================
        # INVESTIGADORES
        # ==================================================
        investigador_results = db.session.query(Investigador)\
        .options(
            joinedload(Investigador.tipo_dedicacion),
            joinedload(Investigador.categoria_utn),
            joinedload(Investigador.programa_incentivos),
            joinedload(Investigador.grupo_utn),
            joinedload(Investigador.participaciones_proyecto)
                .joinedload(InvestigadorProyecto.proyecto),
            joinedload(Investigador.participaciones_relevantes),
            joinedload(Investigador.trabajos_reunion_cientifica)
        )\
        .all()

        for i in investigador_results:
            nombre_normalizado = SearchService.normalize_text(i.nombre_apellido)

            if query_normalized in nombre_normalizado:
                resultados.append({
                    "tipo": "Investigador",
                    "id": i.id,
                    "titulo": i.nombre_apellido,
                    "subtitulo": i.tipo_dedicacion.nombre if i.tipo_dedicacion else None,
                    "fecha": None,
                    "url": f"/investigadores/{i.id}",
                    "extra": {
                        "categoria_utn": i.categoria_utn.nombre if i.categoria_utn else None,
                        "programa_incentivos": i.programa_incentivos.nombre if i.programa_incentivos else None,
                        "grupo": i.grupo_utn.nombre_sigla_grupo if i.grupo_utn else None,
                        "proyectos": [
                            {
                                "id": p.proyecto.id,
                                "nombre": p.proyecto.nombre_proyecto,
                                "fecha_inicio": str(p.fecha_inicio),
                                "fecha_fin": str(p.fecha_fin) if p.fecha_fin else None
                            }
                            for p in i.participaciones_proyecto
                        ],
                        
                        "participaciones_relevantes": [
                            {"id": pr.id, "evento": pr.nombre_evento}
                            for pr in i.participaciones_relevantes
                        ],
                        "trabajos_reunion": [
                            {"id": tr.id, "titulo": tr.titulo_trabajo}
                            for tr in i.trabajos_reunion_cientifica
                        ]
                    }
                })

        # ==================================================
        # ACTIVIDADES DE DOCENCIA
        # ==================================================
        actividad_results = db.session.query(ActividadDocencia)\
            .options(
                joinedload(ActividadDocencia.investigador),
                joinedload(ActividadDocencia.grado_academico),
                joinedload(ActividadDocencia.rol_actividad)
            )\
            .all()

        for a in actividad_results:
            curso_norm = SearchService.normalize_text(a.curso)
            institucion_norm = SearchService.normalize_text(a.institucion)

            if query_normalized in curso_norm or query_normalized in institucion_norm:
                resultados.append({
                    "tipo": "Actividad de Docencia",
                    "id": a.id,
                    "titulo": a.curso,
                    "subtitulo": a.institucion,
                    "fecha": a.fecha_inicio,
                    "url": f"/actividades-docencia/{a.id}",
                    "extra": {
                        "fecha_inicio": str(a.fecha_inicio),
                        "fecha_fin": str(a.fecha_fin) if a.fecha_fin else None,
                        "investigador": a.investigador.nombre_apellido if a.investigador else None,
                        "grado_academico": {
                            "id": a.grado_academico.id,
                            "nombre": a.grado_academico.nombre
                        } if a.grado_academico else None,
                        "rol_actividad": {
                            "id": a.rol_actividad.id,
                            "nombre": a.rol_actividad.nombre
                        } if a.rol_actividad else None
                    }
                })
        # ==================================================
        # PROYECTOS DE INVESTIGACIÓN (por nombre)
        # ==================================================

        proyecto_results = db.session.query(ProyectoInvestigacion)\
            .options(
                joinedload(ProyectoInvestigacion.tipo_proyecto),
                joinedload(ProyectoInvestigacion.grupo_utn),
                joinedload(ProyectoInvestigacion.fuente_financiamiento),
                joinedload(ProyectoInvestigacion.participaciones_investigador)
                    .joinedload(InvestigadorProyecto.investigador),
                joinedload(ProyectoInvestigacion.participaciones_becario)
                    .joinedload(BecarioProyecto.becario)
            )\
            .all()

        for proyecto in proyecto_results:

            nombre_norm = SearchService.normalize_text(proyecto.nombre_proyecto)
            descripcion_norm = SearchService.normalize_text(proyecto.descripcion_proyecto)

            if query_normalized in nombre_norm or query_normalized in descripcion_norm:


                resultados.append({
                    "tipo": "Proyecto de Investigación",
                    "id": proyecto.id,
                    "titulo": proyecto.nombre_proyecto,
                    "subtitulo": proyecto.tipo_proyecto.nombre if proyecto.tipo_proyecto else None,
                    "fecha": proyecto.fecha_inicio,
                    "url": f"/proyectos/{proyecto.id}",
                    "extra": {
                        "codigo": proyecto.codigo_proyecto,
                        "descripcion": proyecto.descripcion_proyecto,
                        "grupo": proyecto.grupo_utn.nombre_sigla_grupo
                            if proyecto.grupo_utn else None,
                        "fuente_financiamiento": proyecto.fuente_financiamiento.nombre
                            if proyecto.fuente_financiamiento else None,
                        "investigadores": [
                            {
                                "id": p.investigador.id,
                                "nombre": p.investigador.nombre_apellido,
                                "fecha_inicio": str(p.fecha_inicio),
                                "fecha_fin": str(p.fecha_fin) if p.fecha_fin else None
                            }
                            for p in proyecto.participaciones_investigador
                        ],
                        "becarios": [
                            {
                                "id": p.becario.id,
                                "nombre": p.becario.nombre_apellido,
                                "fecha_inicio": str(p.fecha_inicio),
                                "fecha_fin": str(p.fecha_fin) if p.fecha_fin else None
                            }
                            for p in proyecto.participaciones_becario
                        ]
                    }
                })
                
        # ==================================================
        # TIPO DE PROYECTO (por nombre del tipo)
        # ==================================================

        tipos = db.session.query(TipoProyecto)\
            .options(joinedload(TipoProyecto.proyectos_investigacion))\
            .all()

        for tipo in tipos:

            tipo_norm = SearchService.normalize_text(tipo.nombre)

            if query_normalized in tipo_norm:

                for proyecto in tipo.proyectos_investigacion:
                    resultados.append({
                        "tipo": "Proyecto (por tipo)",
                        "id": proyecto.id,
                        "titulo": proyecto.nombre_proyecto,
                        "subtitulo": tipo.nombre,
                        "fecha": proyecto.fecha_inicio,
                        "url": f"/proyectos/{proyecto.id}"
                    })
                    
        # ==================================================
        # TIPO PROYECTO
        # ==================================================
        tipo_proyecto_results = db.session.query(TipoProyecto)\
            .options(joinedload(TipoProyecto.proyectos_investigacion))\
            .all()

        for tipo in tipo_proyecto_results:

            tipo_nombre_norm = SearchService.normalize_text(tipo.nombre)

            if query_normalized in tipo_nombre_norm:

                # ✅ Si tiene proyectos → devolver proyectos
                if tipo.proyectos_investigacion:

                    for proyecto in tipo.proyectos_investigacion:
                        resultados.append({
                            "tipo": "Proyecto (por tipo)",
                            "id": proyecto.id,
                            "titulo": proyecto.nombre_proyecto,
                            "subtitulo": f"Tipo: {tipo.nombre}",
                            "fecha": proyecto.fecha_inicio,
                            "url": f"/proyectos/{proyecto.id}"
                        })

                else:
                    resultados.append({
                        "tipo": "Tipo de Proyecto",
                        "id": tipo.id,
                        "titulo": tipo.nombre,
                        "subtitulo": "Sin proyectos asociados",
                        "fecha": None,
                        "url": f"/tipos-proyecto/{tipo.id}"
                    })
                    
        # ==================================================
        # EQUIPAMIENTO
        # ==================================================

        equipamiento_results = db.session.query(Equipamiento)\
            .options(joinedload(Equipamiento.grupo_utn))\
            .all()

        for e in equipamiento_results:

            denominacion_norm = SearchService.normalize_text(e.denominacion)

            if query_normalized in denominacion_norm:

                resultados.append({
                    "tipo": "Equipamiento",
                    "id": e.id,
                    "titulo": e.denominacion,
                    "subtitulo": e.descripcion_breve,
                    "fecha": e.fecha_incorporacion,
                    "url": f"/equipamiento/{e.id}",
                    "extra": {
                        "grupo": e.grupo_utn.nombre_sigla_grupo if e.grupo_utn else None,
                        "monto_invertido": e.monto_invertido,
                        "fecha_incorporacion": str(e.fecha_incorporacion)
                    }
                })




        # ==================================================
        # ORDENAMIENTO GLOBAL
        # ==================================================
        if orden == "alf_asc":
            resultados.sort(key=lambda x: x["titulo"].lower())

        elif orden == "alf_desc":
            resultados.sort(key=lambda x: x["titulo"].lower(), reverse=True)

        elif orden == "fecha_desc":
            resultados.sort(
                key=lambda x: x["fecha"] or datetime.min.date(),
                reverse=True
            )

        elif orden == "fecha_asc":
            resultados.sort(
                key=lambda x: x["fecha"] or datetime.min.date()
            )

        return resultados
