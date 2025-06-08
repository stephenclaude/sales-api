import sqlite3
import os
from flask import current_app


def get_db_connection():
    """Get database connection"""
    db_path = current_app.config["DATABASE"]
    if not os.path.exists(db_path):
        raise FileNotFoundError(f"Database file not found: {db_path}")

    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn


def validate_year(year_str: str) -> bool:
    """Validate if year string is a valid 4-digit year"""
    try:
        year = int(year_str)
        return 1900 <= year <= 2100
    except ValueError:
        return False


def validate_order_params(order_by: str, order: str) -> tuple[bool, str]:
    """Validate order parameters"""
    valid_order_by = ["sales_rep", "total_sales", "year"]
    valid_order = ["asc", "desc"]

    if order_by not in valid_order_by:
        return False, f"Invalid order_by. Must be one of: {', '.join(valid_order_by)}"

    if order not in valid_order:
        return False, f"Invalid order. Must be one of: {', '.join(valid_order)}"

    return True, ""
