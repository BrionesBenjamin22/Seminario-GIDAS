from core.models.personal import Personal, Becario, Investigador


def listar_personal_completo():
    resultado = []

    # --------------------
    # PERSONAL (solo activos)
    # --------------------
    for p in Personal.query.all():
        resultado.append({
            "id": p.id,
            "nombre_apellido": p.nombre_apellido,
            "horas_semanales": p.horas_semanales,
            "activo": p.activo,
            "rol": "personal",

            "grupo": {
                "id": p.grupo_utn.id,
                "nombre": p.grupo_utn.nombre_sigla_grupo
            } if p.grupo_utn else None,

            "relaciones": {
                "tipo_personal": {
                    "id": p.tipo_personal.id,
                    "nombre": p.tipo_personal.nombre
                } if p.tipo_personal else None
            },

            # Auditoría
            "created_at": p.created_at.isoformat() if p.created_at else None,
            "creator_name": p.creator_name,
            "deleted_at": p.deleted_at.isoformat() if p.deleted_at else None,
            "deleter_name": p.deleter_name
        })

    # --------------------
    # BECARIOS (solo activos)
    # --------------------
    for b in Becario.query.all():
        resultado.append({
            "id": b.id,
            "nombre_apellido": b.nombre_apellido,
            "horas_semanales": b.horas_semanales,
            "activo": b.activo,
            "rol": "becario",

            "grupo": {
                "id": b.grupo_utn.id,
                "nombre": b.grupo_utn.nombre_sigla_grupo
            } if b.grupo_utn else None,

            "relaciones": {
                "tipo_formacion": {
                    "id": b.tipo_formacion.id,
                    "nombre": b.tipo_formacion.nombre
                } if b.tipo_formacion else None,

                "proyectos": [
                    {
                        "id": p.proyecto.id,
                        "codigo": p.proyecto.codigo_proyecto,
                        "nombre": p.proyecto.nombre_proyecto
                    }
                    for p in b.participaciones_proyecto
                ]
            },

            # Auditoría
            "created_at": b.created_at.isoformat() if b.created_at else None,
            "creator_name": b.creator_name,
            "deleted_at": b.deleted_at.isoformat() if b.deleted_at else None,
            "deleter_name": b.deleter_name
        })

    # --------------------
    # INVESTIGADORES (solo activos)
    # --------------------
    for i in Investigador.query.all():
        resultado.append({
            "id": i.id,
            "nombre_apellido": i.nombre_apellido,
            "horas_semanales": i.horas_semanales,
            "activo": i.activo,
            "rol": "investigador",

            "grupo": {
                "id": i.grupo_utn.id,
                "nombre": i.grupo_utn.nombre_sigla_grupo
            } if i.grupo_utn else None,

            "relaciones": {
                "categoria_utn": {
                    "id": i.categoria_utn.id,
                    "nombre": i.categoria_utn.nombre
                } if i.categoria_utn else None,

                "programa_incentivos": {
                    "id": i.programa_incentivos.id,
                    "nombre": i.programa_incentivos.nombre
                } if i.programa_incentivos else None,

                "tipo_dedicacion": {
                    "id": i.tipo_dedicacion.id,
                    "nombre": i.tipo_dedicacion.nombre
                } if i.tipo_dedicacion else None,

                "proyectos": [
                    {
                        "id": p.proyecto.id,
                        "codigo": p.proyecto.codigo_proyecto,
                        "nombre": p.proyecto.nombre_proyecto
                    }
                    for p in i.participaciones_proyecto
                ],

                "actividades_docencia": [
                    {
                        "id": a.id,
                        "curso": a.curso
                    }
                    for a in i.actividades_docencia
                ],

                "participaciones_relevantes": [
                    {
                        "id": p.id,
                        "evento": p.nombre_evento
                    }
                    for p in i.participaciones_relevantes
                ],

                "trabajos_reunion_cientifica": [
                    {
                        "id": t.id,
                        "titulo": t.titulo_trabajo
                    }
                    for t in i.trabajos_reunion_cientifica
                ]
            },

            # Auditoría
            "created_at": i.created_at.isoformat() if i.created_at else None,
            "creator_name": i.creator_name,
            "deleted_at": i.deleted_at.isoformat() if i.deleted_at else None,
            "deleter_name": i.deleter_name
        })

    return resultado


def obtener_personal_por_tipo(rol, id):
    rol = rol.lower()

    if rol == "personal":
        p = Personal.query.filter_by(id=id).first()
        if not p:
            return None

        return {
            "id": p.id,
            "nombre_apellido": p.nombre_apellido,
            "horas_semanales": p.horas_semanales,
            "activo": p.activo,
            "rol": "personal",
            "grupo": {
                "id": p.grupo_utn.id,
                "nombre": p.grupo_utn.nombre_sigla_grupo
            } if p.grupo_utn else None,
            "relaciones": {
                "tipo_personal": {
                    "id": p.tipo_personal.id,
                    "nombre": p.tipo_personal.nombre
                } if p.tipo_personal else None
            },
            # Auditoría
            "created_at": p.created_at.isoformat() if p.created_at else None,
            "creator_name": p.creator_name,
            "deleted_at": p.deleted_at.isoformat() if p.deleted_at else None,
            "deleter_name": p.deleter_name
        }

    if rol == "becario":
        b = Becario.query.filter_by(id=id).first()
        if not b:
            return None

        return {
            "id": b.id,
            "nombre_apellido": b.nombre_apellido,
            "horas_semanales": b.horas_semanales,
            "activo": b.activo,
            "rol": "becario",
            "grupo": {
                "id": b.grupo_utn.id,
                "nombre": b.grupo_utn.nombre_sigla_grupo
            } if b.grupo_utn else None,
            "relaciones": {
                "tipo_formacion": {
                    "id": b.tipo_formacion.id,
                    "nombre": b.tipo_formacion.nombre
                } if b.tipo_formacion else None,
                "proyectos": [
                    {
                        "id": p.proyecto.id,
                        "codigo": p.proyecto.codigo_proyecto,
                        "nombre": p.proyecto.nombre_proyecto
                    }
                    for p in b.participaciones_proyecto
                ]
            },
            "becas": [
                {
                    "id": bex.beca.id,
                    "nombre_beca": bex.beca.nombre_beca,
                    "descripcion": bex.beca.descripcion,
                    "fuente_financiamiento": {
                        "id": bex.beca.fuente_financiamiento.id,
                        "nombre": bex.beca.fuente_financiamiento.nombre
                    } if bex.beca.fuente_financiamiento else None,
                    "fecha_inicio": str(bex.fecha_inicio) if bex.fecha_inicio else None,
                    "fecha_fin": str(bex.fecha_fin) if bex.fecha_fin else None,
                    "monto_percibido": bex.monto_percibido
                }
                for bex in b.becas
            ] if hasattr(b, "becas") else [],
            # Auditoría
            "created_at": b.created_at.isoformat() if b.created_at else None,
            "creator_name": b.creator_name,
            "deleted_at": b.deleted_at.isoformat() if b.deleted_at else None,
            "deleter_name": b.deleter_name
        }

    if rol == "investigador":
        i = Investigador.query.filter_by(id=id).first()
        if not i:
            return None

        return {
            "id": i.id,
            "nombre_apellido": i.nombre_apellido,
            "horas_semanales": i.horas_semanales,
            "activo": i.activo,
            "rol": "investigador",
            "grupo": {
                "id": i.grupo_utn.id,
                "nombre": i.grupo_utn.nombre_sigla_grupo
            } if i.grupo_utn else None,
            "relaciones": {
                "categoria_utn": {
                    "id": i.categoria_utn.id,
                    "nombre": i.categoria_utn.nombre
                } if i.categoria_utn else None,

                "programa_incentivos": {
                    "id": i.programa_incentivos.id,
                    "nombre": i.programa_incentivos.nombre
                } if i.programa_incentivos else None,

                "tipo_dedicacion": {
                    "id": i.tipo_dedicacion.id,
                    "nombre": i.tipo_dedicacion.nombre
                } if i.tipo_dedicacion else None,

                "proyectos": [
                    {
                        "id": p.proyecto.id,
                        "codigo": p.proyecto.codigo_proyecto,
                        "nombre": p.proyecto.nombre_proyecto
                    }
                    for p in i.participaciones_proyecto
                ],

                "actividades_docencia": [
                    {
                        "id": a.id,
                        "curso": a.curso
                    }
                    for a in i.actividades_docencia
                ],

                "participaciones_relevantes": [
                    {
                        "id": p.id,
                        "evento": p.nombre_evento
                    }
                    for p in i.participaciones_relevantes
                ],

                "trabajos_reunion_cientifica": [
                    {
                        "id": t.id,
                        "titulo": t.titulo_trabajo
                    }
                    for t in i.trabajos_reunion_cientifica
                ]
            },

            # Auditoría
            "created_at": i.created_at.isoformat() if i.created_at else None,
            "creator_name": i.creator_name,
            "deleted_at": i.deleted_at.isoformat() if i.deleted_at else None,
            "deleter_name": i.deleter_name
        }

    return None
