from core.models.personal import Personal, Becario, Investigador


def listar_personal_completo():
    resultado = []

    # --------------------
    # PERSONAL
    # --------------------
    for p in Personal.query.all():
        resultado.append({
            "id": p.id,
            "nombre_apellido": p.nombre_apellido,
            "horas_semanales": p.horas_semanales,
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
            }
        })

    # --------------------
    # BECARIOS
    # --------------------
    for b in Becario.query.all():
        resultado.append({
            "id": b.id,
            "nombre_apellido": b.nombre_apellido,
            "horas_semanales": b.horas_semanales,
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

                "fuente_financiamiento": {
                    "id": b.fuente_financiamiento.id,
                    "nombre": b.fuente_financiamiento.nombre
                } if b.fuente_financiamiento else None,

                "proyectos": [
                    {
                        "id": p.id,
                        "codigo": p.codigo_proyecto,
                        "nombre": p.nombre_proyecto
                    }
                    for p in b.proyectos
                ]
            }
        })

    # --------------------
    # INVESTIGADORES
    # --------------------
    for i in Investigador.query.all():
        resultado.append({
            "id": i.id,
            "nombre_apellido": i.nombre_apellido,
            "horas_semanales": i.horas_semanales,
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
                        "id": p.id,
                        "codigo": p.codigo_proyecto,
                        "nombre": p.nombre_proyecto
                    }
                    for p in i.proyectos
                ],

                "actividades_docencia": [
                    {
                        "id": a.id,
                        "curso": a.denominacion_curso_catedra
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
            }
        })

    return resultado


def obtener_personal_por_tipo(rol, id):

    if rol == "personal":
        p = Personal.query.get(id)
        if not p:
            return None

        return {
            "id": p.id,
            "rol": "personal",
            "nombre_apellido": p.nombre_apellido,
            "horas_semanales": p.horas_semanales,
            "grupo": {
                "id": p.grupo_utn.id,
                "nombre": p.grupo_utn.nombre_sigla_grupo
            } if p.grupo_utn else None
        }

    if rol == "becario":
        b = Becario.query.get(id)
        if not b:
            return None

        return {
            "id": b.id,
            "rol": "becario",
            "nombre_apellido": b.nombre_apellido,
            "horas_semanales": b.horas_semanales,
            "grupo": {
                "id": b.grupo_utn.id,
                "nombre": b.grupo_utn.nombre_sigla_grupo
            } if b.grupo_utn else None
        }

    if rol == "investigador":
        i = Investigador.query.get(id)
        if not i:
            return None

        return {
            "id": i.id,
            "rol": "investigador",
            "nombre_apellido": i.nombre_apellido,
            "horas_semanales": i.horas_semanales,
            "grupo": {
                "id": i.grupo_utn.id,
                "nombre": i.grupo_utn.nombre_sigla_grupo
            } if i.grupo_utn else None
        }

    return None
