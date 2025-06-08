import pytest
import json
from app import create_app
from app.database import Database
import os


@pytest.fixture
def app():
    """Create application for testing"""
    app = create_app()
    app.config["TESTING"] = True
    return app


@pytest.fixture
def client(app):
    """Create test client"""
    return app.test_client()


class TestAPI:
    def test_health_check(self, client):
        """Test health check endpoint"""
        response = client.get("/health")
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data["status"] == "healthy"

    def test_top_seller_by_year_valid(self, client):
        """Test getting top seller for a valid year"""
        # Skip if database doesn't exist
        if not os.path.exists("data.db"):
            pytest.skip("Database file not found")

        response = client.get("/api/v1/sellers/2009/top")
        assert response.status_code in [200, 404]  # 404 if no data for that year

        if response.status_code == 200:
            data = json.loads(response.data)
            assert "Sales Rep" in data
            assert "Total Sales" in data

    def test_top_seller_by_year_invalid(self, client):
        """Test getting top seller for invalid year"""
        response = client.get("/api/v1/sellers/1800/top")
        assert response.status_code == 400
        data = json.loads(response.data)
        assert "error" in data

    def test_all_top_sellers(self, client):
        """Test getting all top sellers"""
        # Skip if database doesn't exist
        if not os.path.exists("data.db"):
            pytest.skip("Database file not found")

        response = client.get("/api/v1/sellers/top")
        assert response.status_code in [200, 404]

        if response.status_code == 200:
            data = json.loads(response.data)
            assert isinstance(data, list)
            if data:  # If there's data
                assert "Sales Rep" in data[0]
                assert "Total Sales" in data[0]
                assert "Year" in data[0]

    def test_all_top_sellers_with_params(self, client):
        """Test getting all top sellers with query parameters"""
        # Skip if database doesn't exist
        if not os.path.exists("data.db"):
            pytest.skip("Database file not found")

        response = client.get("/api/v1/sellers/top?order_by=year&order=asc")
        assert response.status_code in [200, 404]

    def test_invalid_order_by_param(self, client):
        """Test invalid order_by parameter"""
        response = client.get("/api/v1/sellers/top?order_by=invalid")
        assert response.status_code == 400
        data = json.loads(response.data)
        assert "error" in data

    def test_invalid_order_param(self, client):
        """Test invalid order parameter"""
        response = client.get("/api/v1/sellers/top?order=invalid")
        assert response.status_code == 400
        data = json.loads(response.data)
        assert "error" in data


class TestDatabase:
    def test_database_connection(self):
        """Test database connection"""
        if not os.path.exists("data.db"):
            pytest.skip("Database file not found")

        db = Database()
        # This should not raise an exception
        conn = db.get_connection()
        conn.close()
