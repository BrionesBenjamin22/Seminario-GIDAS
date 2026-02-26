from core.models.personal import Personal, Becario, Investigador


# =====================================================
# LISTAR
# =====================================================

def listar_personal_completo():

    resultado = []

    # --------------------
    # PERSONAL
    # --------------------
    for p in Personal.query.all():

        base = p.serialize()

        resultado.append({
            **base,
            "rol": "personal"
        })

    # --------------------
    # BECARIOS
    # --------------------
    for b in Becario.query.all():

        base = b.serialize()

        resultado.append({
            **base,
            "rol": "becario"
        })

    # --------------------
    # INVESTIGADORES
    # --------------------
    for i in Investigador.query.all():

        base = i.serialize()

        resultado.append({
            **base,
            "rol": "investigador"
        })

    return resultado


# =====================================================
# OBTENER POR TIPO
# =====================================================

def obtener_personal_por_tipo(rol, id):

    rol = rol.lower()

    if rol == "personal":
        obj = Personal.query.get(id)

    elif rol == "becario":
        obj = Becario.query.get(id)

    elif rol == "investigador":
        obj = Investigador.query.get(id)

    else:
        return None

    if not obj:
        return None

    return obj.serialize()