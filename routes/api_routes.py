from flask import Blueprint, jsonify, request

from services.google_sheet import get_name_by_series_id

api_bp = Blueprint("api", __name__)


@api_bp.route("/lookup-name", methods=["GET"])
def lookup_name():
    series_id = request.args.get("series_id")
    if not series_id:
        return jsonify({"error": "Missing series_id"}), 400

    name = get_name_by_series_id(series_id)
    if name:
        return jsonify({"name": name})
    else:
        return jsonify({"error": "Not found"}), 404
