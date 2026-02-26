from flask import Blueprint
from core.controllers.cargo_controller import CargoController

cargo_bp = Blueprint("cargo", __name__, url_prefix="/cargos")

cargo_bp.route("/", methods=["GET"])(CargoController.get_all)
cargo_bp.route("/<int:cargo_id>", methods=["GET"])(CargoController.get_by_id)
cargo_bp.route("/", methods=["POST"])(CargoController.create)
cargo_bp.route("/<int:cargo_id>", methods=["PUT"])(CargoController.update)
cargo_bp.route("/<int:cargo_id>", methods=["DELETE"])(CargoController.delete)