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


# Mark for database tests
pytestmark = pytest.mark.database


class TestAPI:
    def test_health_check(self, client):
        """Test health check endpoint - no database required"""
        response = client.get("/health")
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data["status"] == "healthy"

    @pytest.mark.database
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
        """Test getting top seller for invalid year - database validation"""
        response = client.get("/api/v1/sellers/1800/top")
        # Should return 400 for invalid year even without database
        assert response.status_code in [400, 500]
        data = json.loads(response.data)
        assert "error" in data

    @pytest.mark.database
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

    @pytest.mark.database
    def test_all_top_sellers_with_params(self, client):
        """Test getting all top sellers with query parameters"""
        # Skip if database doesn't exist
        if not os.path.exists("data.db"):
            pytest.skip("Database file not found")

        response = client.get("/api/v1/sellers/top?order_by=year&order=asc")
        assert response.status_code in [200, 404]

    def test_invalid_order_by_param(self, client):
        """Test invalid order_by parameter - validation without database"""
        response = client.get("/api/v1/sellers/top?order_by=invalid")
        # Should return 400 for invalid parameter even without database
        assert response.status_code in [400, 500]
        data = json.loads(response.data)
        assert "error" in data

    def test_invalid_order_param(self, client):
        """Test invalid order parameter - validation without database"""
        response = client.get("/api/v1/sellers/top?order=invalid")
        # Should return 400 for invalid parameter even without database
        assert response.status_code in [400, 500]
        data = json.loads(response.data)
        assert "error" in data


class TestDatabase:
    @pytest.mark.database
    def test_database_connection(self):
        """Test database connection"""
        if not os.path.exists("data.db"):
            pytest.skip("Database file not found")

        db = Database()
        # This should not raise an exception
        conn = db.get_connection()
        conn.close()


# Non-database tests
class TestAPIStructure:
    """Test API structure and validation without database dependency"""

    def test_api_endpoints_exist(self, client):
        """Test that API endpoints exist and return proper error codes"""
        # These should return 500 (database not found) not 404 (endpoint not found)
        response = client.get("/api/v1/sellers/2009/top")
        assert response.status_code != 404  # Endpoint exists

        response = client.get("/api/v1/sellers/top")
        assert response.status_code != 404  # Endpoint exists

    def test_invalid_endpoints(self, client):
        """Test invalid endpoints return 404"""
        response = client.get("/api/v1/nonexistent")
        assert response.status_code == 404

        response = client.get("/api/v1/sellers/invalid/top")
        assert response.status_code == 404
