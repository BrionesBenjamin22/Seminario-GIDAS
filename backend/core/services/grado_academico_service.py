from extension import db
from core.models.actividad_docencia import GradoAcademico

class GradoAcademicoService:

    @staticmethod
    def get_all():
        return [g.serialize() for g in GradoAcademico.query.all()]

    @staticmethod
    def get_by_id(grado_id: int):
        grado = GradoAcademico.query.get(grado_id)
        if not grado:
            raise Exception("Grado Académico no encontrado")
        return grado.serialize()
    
    
    