from sqlalchemy import or_
from sqlalchemy.orm import joinedload
from datetime import datetime
from extension import db
from core.models.fuente_financiamiento import FuenteFinanciamiento
from core.models.participacion_relevante import ParticipacionRelevante
from core.models.personal import Personal, Becario, Investigador
from core.models.proyecto_investigacion import ProyectoInvestigacion, BecarioProyecto, InvestigadorProyecto, TipoProyecto
from core.models.actividad_docencia import ActividadDocencia
from core.models.equipamiento import Equipamiento
from core.models.transferencia_socio import TipoContrato, TransferenciaSocioProductiva
from core.models.erogacion import Erogacion, TipoErogacion
from core.models.registro_patente import RegistrosPropiedad, TipoRegistroPropiedad
from core.models.documentacion_autores import DocumentacionBibliografica, Autor
from core.models.tipo_personal import TipoPersonal
from core.models.trabajo_reunion import TrabajoReunionCientifica
from core.models.trabajo_revista import TrabajosRevistasReferato
from core.models.directivos import Directivo, DirectivoGrupo, Cargo
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
        # TIPO PROYECTO
        # ==================================================
        tipo_proyecto_results = db.session.query(TipoProyecto)\
            .options(joinedload(TipoProyecto.proyectos_investigacion))\
            .all()

        for tipo in tipo_proyecto_results:

            tipo_nombre_norm = SearchService.normalize_text(tipo.nombre)

            if query_normalized in tipo_nombre_norm:


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
        # DOCUMENTACIÓN BIBLIOGRÁFICA
        # ==================================================

        documentos = db.session.query(DocumentacionBibliografica)\
            .options(
                joinedload(DocumentacionBibliografica.autores),
                joinedload(DocumentacionBibliografica.grupo_utn)
            )\
            .all()

        for doc in documentos:

            titulo_norm = SearchService.normalize_text(doc.titulo)
            editorial_norm = SearchService.normalize_text(doc.editorial)

            if (
                query_normalized in titulo_norm
                or query_normalized in editorial_norm
            ):

                resultados.append({
                    "tipo": "Documentación",
                    "id": doc.id,
                    "titulo": doc.titulo,
                    "subtitulo": doc.editorial,
                    "fecha": doc.fecha,
                    "url": f"/documentacion-bibliografica/{doc.id}",
                    "extra": {
                        "anio": doc.anio,
                        "grupo": doc.grupo_utn.nombre_unidad_academica if doc.grupo_utn else None,
                        "autores": [
                            {
                                "id": a.id,
                                "nombre_apellido": a.nombre_apellido
                            }
                            for a in doc.autores
                        ]
                    }
                })

        # ==================================================
        # AUTORES
        # ==================================================

        autores = db.session.query(Autor)\
            .options(joinedload(Autor.libros))\
            .all()

        for autor in autores:

            nombre_norm = SearchService.normalize_text(autor.nombre_apellido)

            if query_normalized in nombre_norm:

                resultados.append({
                    "tipo": "Autor",
                    "id": autor.id,
                    "titulo": autor.nombre_apellido,
                    "subtitulo": "Autor bibliográfico",
                    "fecha": None,
                    "url": f"/autores/{autor.id}",
                    "extra": {
                        "libros": [
                            {
                                "id": l.id,
                                "titulo": l.titulo,
                                "editorial": l.editorial,
                                "anio": l.anio
                            }
                            for l in autor.libros
                        ]
                    }
                })
                
        # ==================================================
        # TIPO EROGACIÓN
        # ==================================================

        tipos_erogacion = db.session.query(TipoErogacion)\
            .options(joinedload(TipoErogacion.erogaciones))\
            .all()

        for tipo in tipos_erogacion:

            tipo_norm = SearchService.normalize_text(tipo.nombre)

            if query_normalized in tipo_norm:


                if tipo.erogaciones:

                    for erogacion in tipo.erogaciones:
                        resultados.append({
                            "tipo": "Erogación (por tipo)",
                            "id": erogacion.id,
                            "titulo": tipo.nombre,
                            "subtitulo": f"Erogación ID: {erogacion.id}",
                            "fecha": erogacion.fecha if hasattr(erogacion, "fecha") else None,
                            "url": f"/erogaciones/{erogacion.id}"
                        })


                else:
                    resultados.append({
                        "tipo": "Tipo de Erogación",
                        "id": tipo.id,
                        "titulo": tipo.nombre,
                        "subtitulo": "Sin erogaciones asociadas",
                        "fecha": None,
                        "url": f"/tipos-erogacion/{tipo.id}"
                    })
                    
        # ==================================================
        # FUENTE DE FINANCIAMIENTO
        # ==================================================

        fuentes = db.session.query(FuenteFinanciamiento)\
            .options(joinedload(FuenteFinanciamiento.erogaciones))\
            .all()

        for fuente in fuentes:

            nombre_norm = SearchService.normalize_text(fuente.nombre)

            if query_normalized in nombre_norm:

                becarios = fuente.becarios.all()  # porque lazy="dynamic"
                proyectos = fuente.proyectos_investigacion.all()

                if becarios or proyectos or fuente.erogaciones:

                    resultados.append({
                        "tipo": "Fuente de Financiamiento",
                        "id": fuente.id,
                        "titulo": fuente.nombre,
                        "subtitulo": "Fuente activa",
                        "fecha": None,
                        "url": f"/fuentes-financiamiento/{fuente.id}",
                        "extra": {
                            "total_becarios": len(becarios),
                            "total_proyectos": len(proyectos),
                            "total_erogaciones": len(fuente.erogaciones),
                            "becarios": [
                                {
                                    "id": b.id,
                                    "nombre": b.nombre_apellido
                                }
                                for b in becarios
                            ],
                            "proyectos": [
                                {
                                    "id": p.id,
                                    "nombre": p.nombre_proyecto
                                }
                                for p in proyectos
                            ],
                            "erogaciones": [
                                {
                                    "id": e.id
                                }
                                for e in fuente.erogaciones
                            ]
                        }
                    })

                
                else:
                    resultados.append({
                        "tipo": "Fuente de Financiamiento",
                        "id": fuente.id,
                        "titulo": fuente.nombre,
                        "subtitulo": "Sin registros asociados",
                        "fecha": None,
                        "url": f"/fuentes-financiamiento/{fuente.id}"
                    })
        # ==================================================
        # PARTICIPACIÓN RELEVANTE
        # ==================================================

        participaciones = db.session.query(ParticipacionRelevante)\
            .options(joinedload(ParticipacionRelevante.investigador))\
            .all()

        for pr in participaciones:

            evento_norm = SearchService.normalize_text(pr.nombre_evento)
            forma_norm = SearchService.normalize_text(pr.forma_participacion)

            if (
                query_normalized in evento_norm
                or query_normalized in forma_norm
            ):

                resultados.append({
                    "tipo": "Participación Relevante",
                    "id": pr.id,
                    "titulo": pr.nombre_evento,
                    "subtitulo": pr.forma_participacion,
                    "fecha": pr.fecha,
                    "url": f"/participaciones-relevantes/{pr.id}",
                    "extra": {
                        "investigador": pr.investigador.nombre_apellido if pr.investigador else None
                    }
                })
                
        # ==================================================
        # REGISTROS DE PROPIEDAD
        # ==================================================

        registros = db.session.query(RegistrosPropiedad)\
            .options(
                joinedload(RegistrosPropiedad.tipo_registro),
                joinedload(RegistrosPropiedad.grupo_utn)
            )\
            .all()

        for r in registros:

            articulo_norm = SearchService.normalize_text(r.nombre_articulo)
            organismo_norm = SearchService.normalize_text(r.organismo_registrante)

            if (
                query_normalized in articulo_norm
                or query_normalized in organismo_norm
            ):

                resultados.append({
                    "tipo": "Registro de Propiedad",
                    "id": r.id,
                    "titulo": r.nombre_articulo,
                    "subtitulo": r.organismo_registrante,
                    "fecha": r.fecha_registro,
                    "url": f"/registros-propiedad/{r.id}",
                    "extra": {
                        "tipo_registro": r.tipo_registro.nombre if r.tipo_registro else None,
                        "grupo": r.grupo_utn.nombre_sigla_grupo if r.grupo_utn else None
                    }
                })
                
        # ==================================================
        # TIPO REGISTRO PROPIEDAD
        # ==================================================

        tipos_registro = db.session.query(TipoRegistroPropiedad)\
            .options(joinedload(TipoRegistroPropiedad.registros_propiedad))\
            .all()

        for tipo in tipos_registro:


            tipo_norm = SearchService.normalize_text(tipo.nombre)

            if query_normalized in tipo_norm:

                # Si tiene registros → devolver registros
                if tipo.registros_propiedad:

                    for registro in tipo.registros_propiedad:
                        resultados.append({
                            "tipo": "Registro (por tipo)",
                            "id": registro.id,
                            "titulo": registro.nombre_articulo,
                            "subtitulo": f"Tipo: {tipo.nombre}",
                            "fecha": registro.fecha_registro,
                            "url": f"/registros-propiedad/{registro.id}"
                        })

                # Si no tiene registros → devolver tipo solo
                else:
                    resultados.append({
                        "tipo": "Tipo Registro Propiedad",
                        "id": tipo.id,
                        "titulo": tipo.nombre,
                        "subtitulo": "Sin registros asociados",
                        "fecha": None,
                        "url": f"/tipos-registro-propiedad/{tipo.id}"
                    })

        # ==================================================
        # TRANSFERENCIA SOCIO PRODUCTIVA
        # ==================================================

        transferencias = db.session.query(TransferenciaSocioProductiva)\
            .options(
                joinedload(TransferenciaSocioProductiva.adoptantes),
                joinedload(TransferenciaSocioProductiva.tipo_contrato_transferencia),
                joinedload(TransferenciaSocioProductiva.grupo_utn)
            )\
            .all()

        for t in transferencias:

            descripcion_norm = SearchService.normalize_text(t.descripcion_actividad)
            demandante_norm = SearchService.normalize_text(t.demandante)

            if (
                query_normalized in descripcion_norm
                or query_normalized in demandante_norm
            ):

                resultados.append({
                    "tipo": "Transferencia Socio Productiva",
                    "id": t.id,
                    "titulo": t.descripcion_actividad,
                    "subtitulo": t.demandante,
                    "fecha": t.fecha_inicio,
                    "url": f"/transferencias/{t.id}",
                    "extra": {
                        "tipo_contrato": (
                            t.tipo_contrato_transferencia.nombre
                            if t.tipo_contrato_transferencia else None
                        ),
                        "grupo": (
                            t.grupo_utn.nombre_sigla_grupo
                            if t.grupo_utn else None
                        ),
                        "monto": t.monto,
                        "adoptantes": [
                            a.nombre for a in t.adoptantes
                        ]
                    }
                })
                
                
        # ==================================================
        # TIPO CONTRATO TRANSFERENCIA
        # ==================================================

        tipos_contrato = db.session.query(TipoContrato)\
            .options(joinedload(TipoContrato.transferencias))\
            .all()

        for tipo in tipos_contrato:

            tipo_norm = SearchService.normalize_text(tipo.nombre)

            if query_normalized in tipo_norm:

                # Si tiene transferencias → devolverlas
                if tipo.transferencias:

                    for transferencia in tipo.transferencias:
                        resultados.append({
                            "tipo": "Transferencia (por tipo de contrato)",
                            "id": transferencia.id,
                            "titulo": transferencia.descripcion_actividad,
                            "subtitulo": f"Contrato: {tipo.nombre}",
                            "fecha": transferencia.fecha_inicio,
                            "url": f"/transferencias/{transferencia.id}"
                        })

                # Si no tiene → devolver tipo solo
                else:
                    resultados.append({
                        "tipo": "Tipo de Contrato",
                        "id": tipo.id,
                        "titulo": tipo.nombre,
                        "subtitulo": "Sin transferencias asociadas",
                        "fecha": None,
                        "url": f"/tipos-contrato/{tipo.id}"
                    })

        # ==================================================
        # TIPO PERSONAL
        # ==================================================

        tipos_personal = db.session.query(TipoPersonal).all()
    
        for tipo in tipos_personal:

            tipo_norm = SearchService.normalize_text(tipo.nombre)

            if query_normalized in tipo_norm:

                personas = tipo.personal.all()  # porque lazy="dynamic"

                # Si tiene personas asociadas
                if personas:

                    for persona in personas:
                        resultados.append({
                            "tipo": "Persona (por tipo)",
                            "id": persona.id,
                            "titulo": persona.nombre_apellido,
                            "subtitulo": f"Tipo: {tipo.nombre}",
                            "fecha": None,
                            "url": f"/personal/{persona.id}"
                        })

                # Si no tiene personas asociadas
                else:
                    resultados.append({
                        "tipo": "Tipo Personal",
                        "id": tipo.id,
                        "titulo": tipo.nombre,
                        "subtitulo": "Sin personas asociadas",
                        "fecha": None,
                        "url": f"/tipos-personal/{tipo.id}"
                    })

        # ==================================================
        # TRABAJO REUNIÓN CIENTÍFICA
        # ==================================================

        trabajos_reunion = db.session.query(TrabajoReunionCientifica)\
            .options(
                joinedload(TrabajoReunionCientifica.tipo_reunion_cientifica),
                joinedload(TrabajoReunionCientifica.investigadores),
                joinedload(TrabajoReunionCientifica.grupo_utn)
            )\
            .all()

        for tr in trabajos_reunion:

            titulo_norm = SearchService.normalize_text(tr.titulo_trabajo)
            reunion_norm = SearchService.normalize_text(tr.nombre_reunion)
            procedencia_norm = SearchService.normalize_text(tr.procedencia)
            investigadores_norm = [
                SearchService.normalize_text(inv.nombre_apellido)
                for inv in tr.investigadores
            ]
            
            if (
                query_normalized in titulo_norm
                or query_normalized in reunion_norm
                or query_normalized in procedencia_norm
                or any(query_normalized in inv for inv in investigadores_norm)
            ):

                resultados.append({
                    "tipo": "Trabajo en Reunión Científica",
                    "id": tr.id,
                    "titulo": tr.titulo_trabajo,
                    "subtitulo": tr.nombre_reunion,
                    "fecha": tr.fecha_inicio,
                    "url": f"/trabajos-reunion/{tr.id}",
                    "extra": {
                        "tipo_reunion": (
                            tr.tipo_reunion_cientifica.nombre
                            if tr.tipo_reunion_cientifica else None
                        ),
                        "procedencia": tr.procedencia,
                        "grupo": (
                            tr.grupo_utn.nombre_unidad_academica
                            if tr.grupo_utn else None
                        ),
                        "investigadores": [
                            {
                                "id": inv.id,
                                "nombre": inv.nombre_apellido
                            }
                            for inv in tr.investigadores
                        ]
                    }
                })
                
                
        # ==================================================
        # TRABAJOS EN REVISTAS CON REFERATO
        # ==================================================

        trabajos_revista = db.session.query(TrabajosRevistasReferato)\
            .options(
                joinedload(TrabajosRevistasReferato.grupo_utn),
                joinedload(TrabajosRevistasReferato.tipo_reunion),
                joinedload(TrabajosRevistasReferato.investigadores)
            )\
            .all()

        for tr in trabajos_revista:

            titulo_norm = SearchService.normalize_text(tr.titulo_trabajo)
            revista_norm = SearchService.normalize_text(tr.nombre_revista)
            editorial_norm = SearchService.normalize_text(tr.editorial)
            issn_norm = SearchService.normalize_text(tr.issn)
            pais_norm = SearchService.normalize_text(tr.pais)
            investigadores_norm = [
                SearchService.normalize_text(inv.nombre_apellido)
                for inv in tr.investigadores
            ]

            if (
                query_normalized in titulo_norm
                or query_normalized in revista_norm
                or query_normalized in editorial_norm
                or query_normalized in issn_norm
                or query_normalized in pais_norm
                or any(query_normalized in inv for inv in investigadores_norm)
            ):

                resultados.append({
                    "tipo": "Trabajo en Revista con Referato",
                    "id": tr.id,
                    "titulo": tr.titulo_trabajo,
                    "subtitulo": tr.nombre_revista,
                    "fecha": tr.fecha,
                    "url": f"/trabajos-revistas/{tr.id}",
                    "extra": {
                        "editorial": tr.editorial,
                        "issn": tr.issn,
                        "pais": tr.pais,
                        "grupo": tr.grupo_utn.nombre_sigla_grupo if tr.grupo_utn else None,
                        "tipo_reunion": tr.tipo_reunion.nombre if tr.tipo_reunion else None,
                        "investigadores": [
                            {
                                "id": inv.id,
                                "nombre": inv.nombre_apellido
                            }
                            for inv in tr.investigadores
                        ]
                    }
                })



        # ==================================================
        # DIRECTIVOS
        # ==================================================

        directivo_results = db.session.query(Directivo)\
            .options(
                joinedload(Directivo.participaciones_grupo)
                    .joinedload(DirectivoGrupo.cargo),
                joinedload(Directivo.participaciones_grupo)
                    .joinedload(DirectivoGrupo.grupo_utn)
            )\
            .all()

        for d in directivo_results:

            nombre_norm = SearchService.normalize_text(d.nombre_apellido)

            # Buscar coincidencia por nombre
            coincide_nombre = query_normalized in nombre_norm

            # Buscar coincidencia por cargo
            coincide_cargo = any(
                query_normalized in SearchService.normalize_text(p.cargo.nombre)
                for p in d.participaciones_grupo
                if p.cargo
            )

            if coincide_nombre or coincide_cargo:

                participaciones = [
                    {
                        "grupo": p.grupo_utn.nombre_sigla_grupo if p.grupo_utn else None,
                        "cargo": p.cargo.nombre if p.cargo else None,
                        "fecha_inicio": str(p.fecha_inicio),
                        "fecha_fin": str(p.fecha_fin) if p.fecha_fin else None,
                        "activo": p.fecha_fin is None
                    }
                    for p in d.participaciones_grupo
                ]

                # Detectar si tiene algún cargo activo
                tiene_activo = any(p["activo"] for p in participaciones)

                resultados.append({
                    "tipo": "Directivo",
                    "id": d.id,
                    "titulo": d.nombre_apellido,
                    "subtitulo": "Directivo de Grupo",
                    "fecha": None,
                    "url": f"/directivos/{d.id}",
                    "activo": tiene_activo,   # 👈 bandera para ordenar
                    "extra": {
                        "participaciones": participaciones
                    }
                })







        # ==================================================
        # ORDENAMIENTO GLOBAL
        # ==================================================
        if orden == "alf_asc":
            resultados.sort(
                key=lambda x: (
                    0 if x.get("activo") else 1,
                    x["titulo"].lower()
                )
            )

        elif orden == "alf_desc":
            resultados.sort(
                key=lambda x: (
                    0 if x.get("activo") else 1,
                    x["titulo"].lower()
                ),
                reverse=True
            )
            
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
