from flask import Blueprint
from core.controllers.search_controller import SearchController

search_bp = Blueprint(
    "search",
    __name__,
    url_prefix="/search"
)

search_bp.route("/", methods=["GET"])(
    SearchController.search
)
