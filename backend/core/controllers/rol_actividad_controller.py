from core.models.actividad_docencia import RolActividad
from flask import jsonify, request
from extension import db

class RolActividadController:

    @staticmethod
    def get_all():
        try:
            roles = RolActividad.query.all()
            return jsonify([r.serialize() for r in roles]), 200
        except Exception as e:
            return jsonify({"error": str(e)}), 400

    @staticmethod
    def get_by_id(rol_id):
        try:
            rol = RolActividad.query.get(rol_id)
            if not rol:
                return jsonify({"error": "Rol de Actividad no encontrado"}), 404
            return jsonify(rol.serialize()), 200
        except Exception as e:
            return jsonify({"error": str(e)}), 404

    @staticmethod
    def create():
        data = request.get_json()
        try:
            rol = RolActividad(nombre=data["nombre"])
            db.session.add(rol)
            db.session.commit()
            return jsonify(rol.serialize()), 201
        except Exception as e:
            db.session.rollback()
            return jsonify({"error": str(e)}), 400

    @staticmethod
    def update(rol_id):
        data = request.get_json()
        try:
            rol = RolActividad.query.get(rol_id)
            if not rol:
                return jsonify({"error": "Rol de Actividad no encontrado"}), 404
            rol.nombre = data.get("nombre", rol.nombre)
            db.session.commit()
            return jsonify(rol.serialize()), 200
        except Exception as e:
            db.session.rollback()
            return jsonify({"error": str(e)}), 400

    @staticmethod
    def delete(rol_id):
        try:
            rol = RolActividad.query.get(rol_id)
            if not rol:
                return jsonify({"error": "Rol de Actividad no encontrado"}), 404
            db.session.delete(rol)
            db.session.commit()
            return jsonify({"message": "Eliminado correctamente"}), 200
        except Exception as e:
            db.session.rollback()
            return jsonify({"error": str(e)}), 400
