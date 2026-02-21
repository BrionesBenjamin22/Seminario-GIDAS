from core.models.personal import Personal, Becario, Investigador


def listar_personal_completo():
    resultado = []

    # --------------------
    # PERSONAL (solo activos)
    # --------------------
    for p in Personal.query.filter(Personal.activo == True).all():
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
    # BECARIOS (solo activos)
    # --------------------
    for b in Becario.query.filter(Becario.activo == True).all():
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
    # INVESTIGADORES (solo activos)
    # --------------------
    for i in Investigador.query.filter(Investigador.activo == True).all():
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
            }
        })

    return resultado


def obtener_personal_por_tipo(rol, id):
    rol = rol.lower()

    if rol == "personal":
        p = Personal.query.filter_by(id=id, activo=True).first()
        if not p:
            return None

        return {
            "id": p.id,
            "nombre_apellido": p.nombre_apellido,
            "horas_semanales": p.horas_semanales,
            "rol": "personal",
            "tipo_de_personal": p.tipo_personal.nombre if p.tipo_personal else None
        }

    if rol == "becario":
        b = Becario.query.filter_by(id=id, activo=True).first()
        if not b:
            return None

        return {
        "id": b.id,
        "nombre_apellido": b.nombre_apellido,
        "horas_semanales": b.horas_semanales,
        "activo": b.activo,
        "tipo_formacion": b.tipo_formacion.nombre if b.tipo_formacion else None,
        "fuente_financiamiento": b.fuente_financiamiento.nombre if b.fuente_financiamiento else None
    }

    if rol == "investigador":
        i = Investigador.query.filter_by(id=id, activo=True).first()
        if not i:
            return None

        return {
        "id": i.id,
        "nombre_apellido": i.nombre_apellido,
        "horas_semanales": i.horas_semanales,
        "activo": i.activo,
        "tipo_dedicacion": i.tipo_dedicacion.nombre if i.tipo_dedicacion else None,
        "categoria_utn": i.categoria_utn.nombre if i.categoria_utn else None,
        "programa_incentivos": i.programa_incentivos.nombre if i.programa_incentivos else None
    }

    return None
