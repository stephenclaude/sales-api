import sqlite3
from typing import List, Dict, Any
import os


class Database:
    def __init__(self, db_path: str = "data.db"):
        self.db_path = db_path
        if not os.path.exists(db_path):
            raise FileNotFoundError(f"Database file {db_path} not found")

    def get_connection(self) -> sqlite3.Connection:
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn

    def execute_query(self, query: str, params: tuple = ()) -> List[Dict[str, Any]]:
        """Execute a query and return results as a list of dictionaries"""
        with self.get_connection() as conn:
            cursor = conn.execute(query, params)
            return [dict(row) for row in cursor.fetchall()]

    def get_top_seller_by_year(self, year: int) -> Dict[str, Any]:
        """Get the top sales rep for a specific year"""
        query = """
        SELECT 
            e.FirstName || ' ' || e.LastName AS "Sales Rep", 
            ROUND(SUM(i.Total), 2) AS "Total Sales"
        FROM Invoice i
        JOIN Customer c ON i.CustomerId = c.CustomerId
        JOIN Employee e ON c.SupportRepId = e.EmployeeId
        WHERE STRFTIME('%Y', i.InvoiceDate) = ?
        GROUP BY e.EmployeeId
        ORDER BY "Total Sales" DESC
        LIMIT 1
        """
        results = self.execute_query(query, (str(year),))
        return results[0] if results else {}

    def get_all_top_sellers(
        self, order_by: str = "total_sales", order: str = "desc"
    ) -> List[Dict[str, Any]]:
        """Get top sales rep for each year"""
        # Base query to get sales per rep per year
        base_query = """
        SELECT 
            e.FirstName || ' ' || e.LastName AS "Sales Rep", 
            ROUND(SUM(i.Total), 2) AS "Total Sales", 
            STRFTIME('%Y', i.InvoiceDate) AS "Year"
        FROM Invoice i
        JOIN Customer c ON i.CustomerId = c.CustomerId
        JOIN Employee e ON c.SupportRepId = e.EmployeeId
        GROUP BY e.EmployeeId, STRFTIME('%Y', i.InvoiceDate)
        """

        # Map order_by parameter to actual column names
        order_by_map = {
            "sales_rep": '"Sales Rep"',
            "total_sales": '"Total Sales"',
            "year": '"Year"',
        }

        order_column = order_by_map.get(order_by, '"Total Sales"')
        order_direction = "DESC" if order.lower() == "desc" else "ASC"

        query = f"{base_query} ORDER BY {order_column} {order_direction}"

        return self.execute_query(query)
