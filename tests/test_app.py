"""
Unit Tests for Target Web Application
Runs automatically in GitHub Actions CI pipeline on developer commits.
"""

import sys
import os
import json
import pytest

# Add parent directory to sys.path so app can be imported
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.app import app


@pytest.fixture
def client():
    """Test client fixture for Flask app."""
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


def test_index_endpoint(client):
    """Test root endpoint returns service info."""
    response = client.get("/")
    assert response.status_code == 200
    data = response.get_json()
    assert data["service"] == "DevOps Incident Watchdog Monitored App"
    assert data["status"] == "online"


def test_health_check_endpoint(client):
    """
    Test proactive monitoring health check endpoint.
    Crucial for DevOps uptime monitoring & automated rollouts.
    """
    response = client.get("/health")
    assert response.status_code == 200
    data = response.get_json()
    assert data["status"] == "healthy"
    assert "uptime_seconds" in data
    assert data["http_status"] == 200


def test_product_catalog(client):
    """Test product listing API."""
    response = client.get("/api/products")
    assert response.status_code == 200
    data = response.get_json()
    assert "products" in data
    assert len(data["products"]) > 0


def test_checkout_valid(client):
    """Test valid checkout calculation."""
    payload = {"product_id": 1, "quantity": 2}
    response = client.post(
        "/api/checkout",
        data=json.dumps(payload),
        content_type="application/json"
    )
    assert response.status_code == 200
    data = response.get_json()
    assert data["status"] == "order_confirmed"
    assert data["total_amount"] == 90.0  # 45.0 * 2


def test_checkout_invalid_product(client):
    """Test checkout with invalid product ID returns 404."""
    payload = {"product_id": 9999, "quantity": 1}
    response = client.post(
        "/api/checkout",
        data=json.dumps(payload),
        content_type="application/json"
    )
    assert response.status_code == 404


def test_simulate_crash_handled(client):
    """Test that crash endpoint produces 500 status code with formatted error response."""
    response = client.get("/simulate-crash?type=zero_division")
    assert response.status_code == 500
    data = response.get_json()
    assert data["error"] == "InternalServerError"
    assert "type" in data
