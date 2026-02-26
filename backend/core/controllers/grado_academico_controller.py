from core.models.actividad_docencia import GradoAcademico
from flask import jsonify, request
from extension import db

class GradoAcademicoController:

    @staticmethod
    def get_all():
        try:
            grados = GradoAcademico.query.all()
            return jsonify([g.serialize() for g in grados]), 200
        except Exception as e:
            return jsonify({"error": str(e)}), 400

    @staticmethod
    def get_by_id(grado_id):
        try:
            grado = GradoAcademico.query.get(grado_id)
            if not grado:
                return jsonify({"error": "Grado Académico no encontrado"}), 404
            return jsonify(grado.serialize()), 200
        except Exception as e:
            return jsonify({"error": str(e)}), 404

    @staticmethod
    def create():
        data = request.get_json()
        try:
            grado = GradoAcademico(nombre=data["nombre"])
            db.session.add(grado)
            db.session.commit()
            return jsonify(grado.serialize()), 201
        except Exception as e:
            db.session.rollback()
            return jsonify({"error": str(e)}), 400

    @staticmethod
    def update(grado_id):
        data = request.get_json()
        try:
            grado = GradoAcademico.query.get(grado_id)
            if not grado:
                return jsonify({"error": "Grado Académico no encontrado"}), 404
            grado.nombre = data.get("nombre", grado.nombre)
            db.session.commit()
            return jsonify(grado.serialize()), 200
        except Exception as e:
            db.session.rollback()
            return jsonify({"error": str(e)}), 400

    @staticmethod
    def delete(grado_id):
        try:
            grado = GradoAcademico.query.get(grado_id)
            if not grado:
                return jsonify({"error": "Grado Académico no encontrado"}), 404
            db.session.delete(grado)
            db.session.commit()
            return jsonify({"message": "Eliminado correctamente"}), 200
        except Exception as e:
            db.session.rollback()
            return jsonify({"error": str(e)}), 400
