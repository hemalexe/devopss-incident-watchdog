"""
Comprehensive Application Features Test Suite
Student: S Hemal (24MIS0050)
Course: ISWE406 Agile Development Process and DevOps
Verifies all 12-item catalog, categories, campus fulfillment hubs, coupon vouchers,
live order tracking, payment methods, crash simulation, and defensive fix.
"""

import pytest
from app.app import app

@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client

def test_root_html_serves_full_features(client):
    """Verifies root endpoint serves HTML with all 12 products, categories, search, and tracking."""
    res = client.get('/', headers={'Accept': 'text/html'})
    assert res.status_code == 200
    data = res.data
    assert b"FlashMart" in data
    assert b"OnePlus 11R" in data
    assert b"MacBook Air M3" in data
    assert b"Sony WH-1000XM5" in data
    assert b"Apple Watch" in data
    assert b"Samsung Galaxy S24" in data
    assert b"iPhone 15 Pro" in data
    assert b"Anker 737" in data
    assert b"VITFEST50" in data
    assert b"Live 10-Min Delivery Tracking" in data

def test_expanded_catalog_endpoint(client):
    """Verifies catalog endpoint returns exactly 12 items across 6 categories."""
    res = client.get('/api/catalog')
    assert res.status_code == 200
    json_data = res.get_json()
    items = json_data.get("items", [])
    assert len(items) == 12
    categories = set(item.get("category") for item in items)
    assert len(categories) >= 5

def test_delivery_hubs_endpoint(client):
    """Verifies delivery hubs endpoint returns all 6 VIT campus fulfillment nodes."""
    res = client.get('/api/hubs')
    assert res.status_code == 200
    json_data = res.get_json()
    assert json_data.get("count") == 6
    hubs = json_data.get("hubs", [])
    hub_names = [h["name"] for h in hubs]
    assert any("Men's Hostel" in h or "VIT Vellore" in h for h in hub_names)
    assert any("Ladies Hostel" in h for h in hub_names)
    assert any("Technology Tower" in h for h in hub_names)

def test_categories_endpoint(client):
    """Verifies categories endpoint returns full list of product verticals."""
    res = client.get('/api/categories')
    assert res.status_code == 200
    cats = res.get_json().get("categories", [])
    assert len(cats) >= 6

def test_coupon_validation_valid(client):
    """Verifies promo coupon validation for VIT student discounts."""
    res = client.post('/api/coupon', json={"code": "VITFEST50"})
    assert res.status_code == 200
    assert res.get_json()["valid"] is True
    assert res.get_json()["coupon"]["discount_percent"] == 10

def test_coupon_validation_invalid(client):
    """Verifies coupon validation rejects bogus codes."""
    res = client.post('/api/coupon', json={"code": "FAKECODE99"})
    assert res.status_code == 400
    assert res.get_json()["valid"] is False

def test_live_order_tracking(client):
    """Verifies order tracking endpoint returns 4-stage timeline and driver details."""
    res = client.get('/api/order/track?order_id=FM-94812')
    assert res.status_code == 200
    data = res.get_json()
    assert data["order_id"] == "FM-94812"
    assert data["rider"]["name"] == "Ramesh Kumar"
    assert data["rider"]["otp"] == "4921"
    assert len(data["timeline"]) == 4

def test_zero_stock_crash_and_defensive_fix_lifecycle(client):
    """Verifies full incident simulation and remediation cycle."""
    # 1. Ensure buggy state
    client.post('/api/devops/reset')
    
    # 2. Checkout zero-stock item 3 -> must raise 500 ZeroDivisionError
    res_crash = client.post('/api/checkout', json={
        "product_id": 3,
        "quantity": 1,
        "address": "VIT Vellore Campus (Men's Hostel Q-Block)"
    })
    assert res_crash.status_code == 500
    assert res_crash.get_json()["type"] == "ZeroDivisionError"

    # 3. Apply DevOps fix
    res_fix = client.post('/api/devops/apply-fix')
    assert res_fix.status_code == 200
    assert res_fix.get_json()["bug_fixed"] is True

    # 4. Checkout item 3 -> must return clean 400 not_deliverable without crashing
    res_fixed_checkout = client.post('/api/checkout', json={
        "product_id": 3,
        "quantity": 1,
        "address": "VIT Vellore Campus (Men's Hostel Q-Block)"
    })
    assert res_fixed_checkout.status_code == 400
    assert res_fixed_checkout.get_json()["status"] == "not_deliverable"

    # Reset back to initial state
    client.post('/api/devops/reset')
