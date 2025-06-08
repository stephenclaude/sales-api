from flask import Flask, jsonify, request
from flask_restful import Api, Resource
from typing import Union, Tuple, Dict, Any
import logging
from .database import Database

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class TopSellerByYear(Resource):
    def __init__(self):
        self.db = Database()

    def get(self, year: int) -> Dict[str, Any]:
        """Get top sales rep for a specific year"""
        try:
            # Validate year
            if year < 2000 or year > 2030:
                return {
                    "error": "Invalid year",
                    "message": "Year must be between 2000 and 2030",
                }, 400

            result = self.db.get_top_seller_by_year(year)

            if not result:
                return {
                    "error": "No data found",
                    "message": f"No sales data found for year {year}",
                }, 404

            return result, 200

        except FileNotFoundError as e:
            logger.error(f"Database error: {e}")
            return {
                "error": "Database not found",
                "message": "Please ensure the database file exists",
            }, 500
        except Exception as e:
            logger.error(f"Unexpected error: {e}")
            return {
                "error": "Internal server error",
                "message": "An unexpected error occurred",
            }, 500


class TopSellers(Resource):
    def __init__(self):
        self.db = Database()

    def get(self) -> Dict[str, Any]:
        """Get all top sales reps with optional ordering"""
        try:
            # Get query parameters
            order_by = request.args.get("order_by", "total_sales")
            order = request.args.get("order", "desc")

            # Validate parameters
            valid_order_by = ["sales_rep", "total_sales", "year"]
            valid_order = ["asc", "desc"]

            if order_by not in valid_order_by:
                return {
                    "error": "Invalid order_by parameter",
                    "message": f"order_by must be one of: {', '.join(valid_order_by)}",
                }, 400

            if order.lower() not in valid_order:
                return {
                    "error": "Invalid order parameter",
                    "message": f"order must be one of: {', '.join(valid_order)}",
                }, 400

            results = self.db.get_all_top_sellers(order_by, order)

            if not results:
                return {"error": "No data found", "message": "No sales data found"}, 404

            return results, 200

        except FileNotFoundError as e:
            logger.error(f"Database error: {e}")
            return {
                "error": "Database not found",
                "message": "Please ensure the database file exists",
            }, 500
        except Exception as e:
            logger.error(f"Unexpected error: {e}")
            return {
                "error": "Internal server error",
                "message": "An unexpected error occurred",
            }, 500


def create_app() -> Flask:
    """Application factory pattern"""
    app = Flask(__name__)
    api = Api(app)

    # Add API routes
    api.add_resource(TopSellerByYear, "/api/v1/sellers/<int:year>/top")
    api.add_resource(TopSellers, "/api/v1/sellers/top")

    # Health check endpoint
    @app.route("/health")
    def health_check():
        return jsonify({"status": "healthy"}), 200

    return app
