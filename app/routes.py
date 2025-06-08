from flask import Blueprint, jsonify, request
from app.models import SalesModel
from app.utils import validate_year, validate_order_params

api_bp = Blueprint("api", __name__, url_prefix="/api/v1")


@api_bp.errorhandler(404)
def not_found(error):
    return jsonify({"error": "Endpoint not found"}), 404


@api_bp.errorhandler(500)
def internal_error(error):
    return jsonify({"error": "Internal server error"}), 500


@api_bp.route("/sellers/<year>/top", methods=["GET"])
def get_top_seller_by_year(year):
    """Get top sales rep for a specific year"""
    # Validate year
    if not validate_year(year):
        return (
            jsonify(
                {"error": "Invalid year format. Please provide a valid 4-digit year."}
            ),
            400,
        )

    try:
        result = SalesModel.get_top_seller_by_year(int(year))

        if result is None:
            return jsonify({"error": f"No sales data found for year {year}"}), 404

        return jsonify(result), 200

    except Exception as e:
        return jsonify({"error": "Failed to retrieve data"}), 500


@api_bp.route("/sellers/top", methods=["GET"])
def get_all_top_sellers():
    """Get all top sales reps with optional ordering"""
    # Get query parameters
    order_by = request.args.get("order_by", "total_sales")
    order = request.args.get("order", "desc")

    # Validate parameters
    is_valid, error_msg = validate_order_params(order_by, order)
    if not is_valid:
        return jsonify({"error": error_msg}), 400

    try:
        results = SalesModel.get_all_top_sellers(order_by, order)
        return jsonify(results), 200

    except Exception as e:
        return jsonify({"error": "Failed to retrieve data"}), 500


@api_bp.route("/health", methods=["GET"])
def health_check():
    """Health check endpoint"""
    return jsonify({"status": "healthy"}), 200
