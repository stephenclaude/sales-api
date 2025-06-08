import sqlite3
from typing import List, Dict, Any, Optional
from app.utils import get_db_connection


class SalesModel:
    @staticmethod
    def get_top_seller_by_year(year: int) -> Optional[Dict[str, Any]]:
        """Get the top sales rep for a specific year"""
        conn = get_db_connection()
        cursor = conn.cursor()

        query = """
        SELECT e.FirstName || ' ' || e.LastName AS "Sales Rep", 
               ROUND(SUM(i.Total), 2) AS "Total Sales"
        FROM Invoice i 
        JOIN Customer c ON i.CustomerId = c.CustomerId 
        JOIN Employee e ON c.SupportRepId = e.EmployeeId 
        WHERE STRFTIME('%Y', i.InvoiceDate) = ?
        GROUP BY e.EmployeeId
        ORDER BY SUM(i.Total) DESC
        LIMIT 1
        """

        cursor.execute(query, (str(year),))
        result = cursor.fetchone()
        conn.close()

        if result:
            return {"Sales Rep": result[0], "Total Sales": result[1]}
        return None

    @staticmethod
    def get_all_top_sellers(
        order_by: str = "total_sales", order: str = "desc"
    ) -> List[Dict[str, Any]]:
        """Get all top sales reps with their totals by year"""
        conn = get_db_connection()
        cursor = conn.cursor()

        # Base query
        query = """
        SELECT e.FirstName || ' ' || e.LastName AS "Sales Rep",
               ROUND(SUM(i.Total), 2) AS "Total Sales",
               STRFTIME('%Y', i.InvoiceDate) AS "Year"
        FROM Invoice i 
        JOIN Customer c ON i.CustomerId = c.CustomerId 
        JOIN Employee e ON c.SupportRepId = e.EmployeeId 
        GROUP BY e.EmployeeId, STRFTIME('%Y', i.InvoiceDate)
        """

        # Add ordering
        order_map = {
            "sales_rep": '"Sales Rep"',
            "total_sales": '"Total Sales"',
            "year": '"Year"',
        }

        order_column = order_map.get(order_by, '"Total Sales"')
        order_direction = "ASC" if order.lower() == "asc" else "DESC"

        query += f" ORDER BY {order_column} {order_direction}"

        cursor.execute(query)
        results = cursor.fetchall()
        conn.close()

        return [
            {"Sales Rep": row[0], "Total Sales": row[1], "Year": row[2]}
            for row in results
        ]
