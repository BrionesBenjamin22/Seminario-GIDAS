from core.models.actividad_docencia import RolActividad

class RolActividadService:

    @staticmethod
    def get_all():
        return [r.serialize() for r in RolActividad.query.all()]

    @staticmethod
    def get_by_id(rol_id: int):
        rol = RolActividad.query.get(rol_id)
        if not rol:
            raise Exception("Rol de Actividad no encontrado")
        return rol.serialize()
    
