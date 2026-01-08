from core.models.personal import Personal, Becario, Investigador


def listar_personal_completo():
    personal = Personal.query.all()
    becarios = Becario.query.all()
    investigadores = Investigador.query.all()

    resultado = []

    for p in personal:
        resultado.append({
            "id": p.id,
            "nombre_apellido": p.nombre_apellido,
            "horas_semanales": p.horas_semanales,
            "rol": "personal",
            "detalle": p.tipo_personal.nombre if p.tipo_personal else None
        })

    for b in becarios:
        resultado.append({
            "id": b.id,
            "nombre_apellido": b.nombre_apellido,
            "horas_semanales": b.horas_semanales,
            "rol": "becario",
            "detalle": b.tipo_formacion.nombre if b.tipo_formacion else None
        })

    for i in investigadores:
        resultado.append({
            "id": i.id,
            "nombre_apellido": i.nombre_apellido,
            "horas_semanales": i.horas_semanales,
            "rol": "investigador",
            "detalle": i.categoria_utn.nombre if i.categoria_utn else None
        })

    return resultado
