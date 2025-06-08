import pytest
import tempfile
import os
import shutil
from app import create_app


@pytest.fixture
def client():
    # Create a test app
    app = create_app()
    app.config["TESTING"] = True

    with app.test_client() as client:
        with app.app_context():
            yield client


def test_health_check(client):
    """Test the health check endpoint"""
    response = client.get("/api/v1/health")
    assert response.status_code == 200
    assert response.json["status"] == "healthy"


def test_get_top_seller_by_year_valid(client):
    """Test getting top seller for a valid year"""
    response = client.get("/api/v1/sellers/2009/top")
    assert response.status_code == 200
    data = response.json
    assert "Sales Rep" in data
    assert "Total Sales" in data


def test_get_top_seller_by_year_invalid_year(client):
    """Test getting top seller with invalid year"""
    response = client.get("/api/v1/sellers/abc/top")
    assert response.status_code == 400
    assert "error" in response.json


def test_get_all_top_sellers_default(client):
    """Test getting all top sellers with default parameters"""
    response = client.get("/api/v1/sellers/top")
    assert response.status_code == 200
    data = response.json
    assert isinstance(data, list)
    if data:  # If there's data
        assert "Sales Rep" in data[0]
        assert "Total Sales" in data[0]
        assert "Year" in data[0]


def test_get_all_top_sellers_with_params(client):
    """Test getting all top sellers with query parameters"""
    response = client.get("/api/v1/sellers/top?order_by=year&order=asc")
    assert response.status_code == 200


def test_get_all_top_sellers_invalid_params(client):
    """Test getting all top sellers with invalid parameters"""
    response = client.get("/api/v1/sellers/top?order_by=invalid&order=desc")
    assert response.status_code == 400
    assert "error" in response.json


def test_not_found_endpoint(client):
    """Test 404 for non-existent endpoint"""
    response = client.get("/api/v1/nonexistent")
    assert response.status_code == 404
