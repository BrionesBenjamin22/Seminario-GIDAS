from sqlalchemy import or_
from sqlalchemy.orm import joinedload
from datetime import datetime
from extension import db
from core.models.personal import Personal, Becario, Investigador
from core.models.actividad_docencia import ActividadDocencia
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
                joinedload(Becario.proyectos)
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
                            {"id": p.id, "nombre": p.nombre_proyecto}
                            for p in b.proyectos
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
                joinedload(Investigador.proyectos),
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
                            {"id": p.id, "nombre": p.nombre_proyecto}
                            for p in i.proyectos
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
                        "fecha_fin": str(a.fecha_fin),
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
