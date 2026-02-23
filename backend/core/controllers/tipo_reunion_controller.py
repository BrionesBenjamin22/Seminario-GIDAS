from flask import jsonify
from core.models.trabajo_reunion import TipoReunion


class TipoReunionController:

    @staticmethod
    def get_all():
        tipos = TipoReunion.query.order_by(TipoReunion.nombre.asc()).all()
        return jsonify([t.serialize() for t in tipos]), 200