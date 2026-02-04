from flask import jsonify, request
from core.services.search_service import SearchService


class SearchController:

    @staticmethod
    def search():
        try:
            query = request.args.get("q", "").strip()

            if len(query) < 2:
                return jsonify([]), 200

            results = SearchService.search(query)

            return jsonify(results), 200

        except Exception as e:
            return jsonify({"error": str(e)}), 400
