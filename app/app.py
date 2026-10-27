"""
Production Web Application - DevOps Incident Watchdog Target Service
Author: S Hemal (24MIS0050)
Course: Agile Development Process and DevOps

This application serves as the monitored service on AWS. It includes:
- Live health check endpoints (/health)
- Business logic endpoints (/api/products, /api/checkout)
- Simulated fault endpoints (/simulate-crash) to demonstrate CloudWatch alarm triggering
"""

import logging
import os
import sys
import time
import traceback
from flask import Flask, jsonify, request

app = Flask(__name__)

# Configure structured logging for AWS CloudWatch
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] [SERVICE: watchdog-target-app] %(message)s',
    handlers=[logging.StreamHandler(sys.stdout)]
)
logger = logging.getLogger("watchdog-target-app")

APP_VERSION = os.environ.get("APP_VERSION", "1.0.0")
START_TIME = time.time()

BUG_FIXED = False

# Catalog of items (Expanded 12-item catalog across 6 categories; Item 3 has 0 stock for incident simulation)
CATALOG = [
    {
        "id": 1,
        "name": "Apple MacBook Air M3 (16GB, 256GB SSD)",
        "price": 45.0,
        "display_price": 114990,
        "mrp": 134990,
        "category": "laptops",
        "category_label": "Laptops & Computing",
        "stock": 10,
        "rating": 4.9,
        "reviews": 4210,
        "delivery_mins": 10,
        "image": "https://images.unsplash.com/photo-1517336714731-489689fd1ca8?w=500&auto=format&fit=crop&q=60"
    },
    {
        "id": 2,
        "name": "Sony WH-1000XM5 ANC Headphones",
        "price": 25.0,
        "display_price": 24990,
        "mrp": 34990,
        "category": "audio",
        "category_label": "Audio & Sound",
        "stock": 5,
        "rating": 4.8,
        "reviews": 9850,
        "delivery_mins": 10,
        "image": "https://images.unsplash.com/photo-1505740420928-5e560c06d30e?w=500&auto=format&fit=crop&q=60"
    },
    {
        "id": 3,
        "name": "OnePlus 11R 5G (Sonic Black, 16GB)",
        "price": 55.0,
        "display_price": 34999,
        "mrp": 44999,
        "category": "smartphones",
        "category_label": "Promotional Flash Sale Deal",
        "stock": 0,  # Zero stock to reproduce runtime division-by-zero!
        "rating": 4.6,
        "reviews": 18420,
        "delivery_mins": 10,
        "flash_deal": True,
        "image": "https://images.unsplash.com/photo-1598327105666-5b89351aff97?w=500&auto=format&fit=crop&q=60"
    },
    {
        "id": 4,
        "name": "Apple Watch Series 9 GPS (45mm)",
        "price": 35.0,
        "display_price": 41900,
        "mrp": 44900,
        "category": "wearables",
        "category_label": "Wearables",
        "stock": 6,
        "rating": 4.7,
        "reviews": 3120,
        "delivery_mins": 10,
        "image": "https://images.unsplash.com/photo-1546868871-7041f2a55e12?w=500&auto=format&fit=crop&q=60"
    },
    {
        "id": 5,
        "name": "Samsung Galaxy S24 Ultra (Titanium Gray, 256GB)",
        "price": 120.0,
        "display_price": 129999,
        "mrp": 139999,
        "category": "smartphones",
        "category_label": "Smartphones",
        "stock": 4,
        "rating": 4.9,
        "reviews": 7650,
        "delivery_mins": 10,
        "image": "https://images.unsplash.com/photo-1610945265064-0e34e5519bbf?w=500&auto=format&fit=crop&q=60"
    },
    {
        "id": 6,
        "name": "Apple iPhone 15 Pro (Natural Titanium, 128GB)",
        "price": 115.0,
        "display_price": 124900,
        "mrp": 134900,
        "category": "smartphones",
        "category_label": "Smartphones",
        "stock": 7,
        "rating": 4.9,
        "reviews": 11200,
        "delivery_mins": 10,
        "image": "https://images.unsplash.com/photo-1695048133142-1a20484d2569?w=500&auto=format&fit=crop&q=60"
    },
    {
        "id": 7,
        "name": "Apple AirPods Pro 2 (USB-C with MagSafe)",
        "price": 22.0,
        "display_price": 21900,
        "mrp": 24900,
        "category": "audio",
        "category_label": "Audio & Sound",
        "stock": 12,
        "rating": 4.8,
        "reviews": 15800,
        "delivery_mins": 10,
        "image": "https://images.unsplash.com/photo-1600294037681-c80b4cb5b434?w=500&auto=format&fit=crop&q=60"
    },
    {
        "id": 8,
        "name": "ASUS ROG Zephyrus G14 (Ryzen 9, RTX 4060)",
        "price": 140.0,
        "display_price": 149990,
        "mrp": 174990,
        "category": "laptops",
        "category_label": "Laptops & Computing",
        "stock": 3,
        "rating": 4.8,
        "reviews": 1840,
        "delivery_mins": 15,
        "image": "https://images.unsplash.com/photo-1593642632823-8f785ba67e45?w=500&auto=format&fit=crop&q=60"
    },
    {
        "id": 9,
        "name": "Samsung Galaxy Watch 6 Classic LTE (47mm)",
        "price": 32.0,
        "display_price": 36999,
        "mrp": 42999,
        "category": "wearables",
        "category_label": "Wearables",
        "stock": 8,
        "rating": 4.6,
        "reviews": 2940,
        "delivery_mins": 10,
        "image": "https://images.unsplash.com/photo-1508685096489-7aacd43bd3b1?w=500&auto=format&fit=crop&q=60"
    },
    {
        "id": 10,
        "name": "Keychron K2 Wireless Mechanical Keyboard (RGB)",
        "price": 8.0,
        "display_price": 8499,
        "mrp": 10999,
        "category": "gaming",
        "category_label": "Gaming Gear & Peripherals",
        "stock": 14,
        "rating": 4.7,
        "reviews": 4620,
        "delivery_mins": 10,
        "image": "https://images.unsplash.com/photo-1587829741301-dc798b83add3?w=500&auto=format&fit=crop&q=60"
    },
    {
        "id": 11,
        "name": "Marshall Emberton II Bluetooth Speaker",
        "price": 14.0,
        "display_price": 14999,
        "mrp": 19999,
        "category": "audio",
        "category_label": "Audio & Sound",
        "stock": 9,
        "rating": 4.7,
        "reviews": 3410,
        "delivery_mins": 10,
        "image": "https://images.unsplash.com/photo-1545454675-3531b543be5d?w=500&auto=format&fit=crop&q=60"
    },
    {
        "id": 12,
        "name": "Anker 737 GaN 140W 24,000mAh Power Bank",
        "price": 11.0,
        "display_price": 11999,
        "mrp": 14999,
        "category": "gaming",
        "category_label": "Tech Essentials & Power",
        "stock": 18,
        "rating": 4.9,
        "reviews": 6120,
        "delivery_mins": 10,
        "image": "https://images.unsplash.com/photo-1609592424369-026c483a9032?w=500&auto=format&fit=crop&q=60"
    }
]

# Campus Delivery Fulfillment Nodes
DELIVERY_HUBS = [
    {"id": "hub-1", "name": "VIT Vellore Campus", "sub": "Men's Hostel Q-Block, Katpadi • 10 Mins", "eta": "10 Mins", "dark_store": "Alpha Dark Store"},
    {"id": "hub-2", "name": "VIT Ladies Hostel Block L", "sub": "LH Complex, Near Lake • 12 Mins", "eta": "12 Mins", "dark_store": "Beta Dark Store"},
    {"id": "hub-3", "name": "Technology Tower (TT)", "sub": "Academic Zone, Ground Floor • 8 Mins", "eta": "8 Mins", "dark_store": "Express Locker 01"},
    {"id": "hub-4", "name": "Anna Auditorium & Food Court", "sub": "Central Campus Hub • 10 Mins", "eta": "10 Mins", "dark_store": "Central Kiosk"},
    {"id": "hub-5", "name": "Katpadi Junction Hub", "sub": "Railway Station Road • 15 Mins", "eta": "15 Mins", "dark_store": "Peripheral Dark Store #4"},
    {"id": "hub-6", "name": "Vellore Fort Town Hub", "sub": "Gandhi Nagar, Fort View • 18 Mins", "eta": "18 Mins", "dark_store": "Town Fulfillment #7"},
]


@app.route("/", methods=["GET"])
def index():
    """Root endpoint with interactive UI or service metadata."""
    if "text/html" in request.headers.get("Accept", ""):
        try:
            from flask import render_template
            return render_template("index.html")
        except Exception:
            pass
    return jsonify({
        "service": "DevOps Incident Watchdog Monitored App",
        "student": "S Hemal (24MIS0050)",
        "version": APP_VERSION,
        "status": "online",
        "bug_fixed": BUG_FIXED,
        "endpoints": {
            "health": "/health",
            "products": "/api/products",
            "checkout": "/api/checkout (POST)",
            "simulate_crash": "/simulate-crash",
            "apply_fix": "/api/devops/apply-fix"
        }
    }), 200


@app.route("/health", methods=["GET"])
@app.route("/api/health", methods=["GET"])
def health_check():
    """
    Proactive health check endpoint.
    CloudWatch Synthetics or Route53 / ELB can poll this endpoint periodically.
    """
    uptime_seconds = int(time.time() - START_TIME)
    return jsonify({
        "status": "healthy",
        "service": "watchdog-target-app",
        "version": APP_VERSION,
        "uptime_seconds": uptime_seconds,
        "http_status": 200
    }), 200


@app.route("/api/products", methods=["GET"])
@app.route("/api/catalog", methods=["GET"])
def get_products():
    """Returns catalog of products."""
    logger.info("Fetched product catalog successfully.")
    return jsonify({
        "count": len(CATALOG),
        "products": CATALOG,
        "items": CATALOG
    }), 200


@app.route("/api/checkout", methods=["POST"])
def checkout():
    """
    Simulates a product purchase calculation.
    Demonstrates the Zepto flash sale crash vs clean stockout handling.
    """
    global BUG_FIXED
    data = request.get_json(silent=True) or {}
    product_id = data.get("product_id")
    quantity = data.get("quantity", 1)

    product = next((p for p in CATALOG if p["id"] == product_id), None)
    if not product:
        return jsonify({"error": "Product not found"}), 404

    # Delivery address from request
    address = data.get("address", "Flat 402, Tech Park Avenue, Bangalore")

    # Flash Sale Scenario: Customer checks out item with 0 stock
    if product["stock"] <= 0:
        if not BUG_FIXED:
            # BEFORE FIX: Bug in delivery router & stock calculation - crashes with HTTP 500!
            logger.error(f"[CRITICAL_ALERT] Incident simulation triggered! Item '{product['name']}' has stock=0 for address '{address}'")
            logger.error("[EXCEPTION] Unhandled ZeroDivisionError in delivery routing worker: allocation = 100 / stock")
            _ = 100 / product["stock"]  # Crashes with HTTP 500 ZeroDivisionError!
        else:
            # AFTER FIX: CI/CD deployed patch handles delivery check gracefully!
            logger.warning(f"[DELIVERY_NOTICE] '{product['name']}' not deliverable to '{address}'.")
            return jsonify({
                "status": "not_deliverable",
                "message": f"Sorry, this item is not deliverable to your address (Out of stock at your nearest fulfillment center)!",
                "product": product["name"],
                "address": address
            }), 400

    # Normal calculation logic
    total = product["price"] * quantity
    logger.info(f"Checkout processed for product_id={product_id}, qty={quantity}, total=${total}")
    return jsonify({
        "status": "order_confirmed",
        "product": product["name"],
        "quantity": quantity,
        "total_amount": total,
        "delivery_address": address
    }), 200


@app.route("/api/devops/apply-fix", methods=["POST", "GET"])
def apply_fix():
    """Simulates CI/CD pipeline deploying the bug fix to production."""
    global BUG_FIXED
    BUG_FIXED = True
    logger.info("[DEVOPS CI/CD] Automated bug fix deployed! Zero-touch ticket closed as Done.")
    return jsonify({
        "status": "deployed",
        "message": "CI/CD Pipeline: Patch deployed successfully. Zero-touch ticket closed as Done.",
        "bug_fixed": True
    }), 200


@app.route("/api/devops/reset", methods=["POST", "GET"])
def reset_demo():
    """Resets demo back to initial buggy state."""
    global BUG_FIXED
    BUG_FIXED = False
    return jsonify({"status": "reset", "bug_fixed": False}), 200


@app.route("/api/devops/status", methods=["GET"])
def devops_status():
    """Returns current fix status."""
    global BUG_FIXED
    return jsonify({"bug_fixed": BUG_FIXED}), 200


@app.route("/api/hubs", methods=["GET"])
def get_hubs():
    """Returns list of campus dark store fulfillment hubs."""
    return jsonify({"count": len(DELIVERY_HUBS), "hubs": DELIVERY_HUBS}), 200


@app.route("/api/categories", methods=["GET"])
def get_categories():
    """Returns distinct product categories."""
    cats = [
        {"id": "all", "name": "All Products", "icon": "fa-layer-group"},
        {"id": "mega-deals", "name": "Mega Flash Deals", "icon": "fa-fire", "hot": True},
        {"id": "smartphones", "name": "Smartphones", "icon": "fa-mobile-screen"},
        {"id": "laptops", "name": "Laptops & PCs", "icon": "fa-laptop"},
        {"id": "audio", "name": "Audio & Sound", "icon": "fa-headphones"},
        {"id": "wearables", "name": "Wearables", "icon": "fa-clock"},
        {"id": "gaming", "name": "Gaming & Gear", "icon": "fa-gamepad"},
    ]
    return jsonify({"categories": cats}), 200


@app.route("/api/coupon", methods=["POST"])
def validate_coupon():
    """Validates promotional discount vouchers."""
    data = request.get_json(silent=True) or {}
    code = (data.get("code") or "").strip().upper()
    valid_coupons = {
        "VITFEST50": {"discount_percent": 10, "max_discount": 5000, "description": "10% Off for VIT Students"},
        "FLASHTECH2000": {"flat_discount": 2000, "min_cart": 15000, "description": "Flat ₹2,000 Off on Tech Deals"},
        "CAMPUSFREE": {"free_delivery": True, "description": "Free Delivery Fee Waiver across Campus Hubs"},
    }
    if code in valid_coupons:
        return jsonify({"valid": True, "code": code, "coupon": valid_coupons[code]}), 200
    return jsonify({"valid": False, "message": "Invalid or expired coupon code"}), 400


@app.route("/api/order/track", methods=["GET"])
def track_order():
    """Returns 4-stage 10-minute quick-commerce order status timeline."""
    order_id = request.args.get("order_id", "FM-94812")
    return jsonify({
        "order_id": order_id,
        "eta_minutes": 6,
        "delivery_hub": "VIT Vellore Campus (Men's Hostel Q-Block)",
        "rider": {
            "name": "Ramesh Kumar",
            "vehicle": "Electric Scooter (TN-23-AB-1024)",
            "contact": "+91 98765 43210",
            "rating": 4.95,
            "otp": "4921"
        },
        "timeline": [
            {"stage": "order_confirmed", "label": "Order Confirmed & Payment Verified", "status": "completed", "time": "Just now"},
            {"stage": "darkstore_packing", "label": "Dark Store Picking & Security Seal Check", "status": "completed", "time": "2 mins ago"},
            {"stage": "rider_dispatched", "label": "Out for Express Campus Delivery", "status": "active", "time": "In transit"},
            {"stage": "delivered", "label": "Delivered to Delivery Hub", "status": "pending", "time": "In 6 mins"}
        ]
    }), 200


@app.route("/report", methods=["GET"])
def view_report():
    """Serves the Architecture and Incident Lifecycle PDF report."""
    from flask import send_from_directory
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    pdf_name = "DevOps_Incident_Watchdog_Architecture_Report.pdf"
    if os.path.exists(os.path.join(base_dir, pdf_name)):
        return send_from_directory(base_dir, pdf_name, mimetype="application/pdf")
    # Also check current directory
    if os.path.exists(pdf_name):
        return send_from_directory(".", pdf_name, mimetype="application/pdf")
    return jsonify({"error": "Report PDF not found"}), 404


@app.route("/simulate-crash", methods=["GET", "POST"])
def simulate_crash():
    """
    Demonstration endpoint used during the Agile/DevOps assessment.
    Forces an unhandled server exception to generate CloudWatch error logs,
    triggering the Incident Watchdog Lambda function.
    """
    error_type = request.args.get("type", "zero_division")

    logger.error(f"[CRITICAL_ALERT] Incident simulation triggered! type={error_type}")

    if error_type == "zero_division":
        # Simulates a divide-by-zero calculation bug
        logger.error("[EXCEPTION] Unhandled ZeroDivisionError in calculation worker: discount_ratio = 100 / 0")
        _ = 100 / 0
    elif error_type == "db_timeout":
        # Simulates a database connection failure
        logger.error("[EXCEPTION] ConnectionTimeoutError: Failed to connect to RDS Postgres after 30000ms")
        raise TimeoutError("Database connection pool exhausted (Simulated DB Incident)")
    else:
        # Generic unhandled crash
        logger.error("[EXCEPTION] NullPointerException / KeyError: 'auth_token' missing from request payload")
        raise KeyError("auth_token key missing in secure session header")

    return jsonify({"status": "unexpected_success"}), 200


@app.errorhandler(Exception)
def handle_exception(e):
    """
    Global exception handler that logs full stack trace to CloudWatch standard output.
    Returns standard HTTP 500 response.
    """
    error_trace = traceback.format_exc()
    error_type = type(e).__name__
    error_msg = str(e)

    # Format structured incident log for CloudWatch ingestion
    logger.critical(
        f"[INCIDENT_DETECTED] Type={error_type} | Message={error_msg}\n"
        f"--- STACK TRACE ---\n{error_trace}\n--- END TRACE ---"
    )

    return jsonify({
        "error": "InternalServerError",
        "message": error_msg,
        "type": error_type,
        "status_code": 500,
        "timestamp": time.time(),
        "trace": error_trace.splitlines()[-3:] if error_trace else []
    }), 500


if __name__ == "__main__":
    # Local dev server
    port = int(os.environ.get("PORT", 5000))
    logger.info(f"Starting application on port {port}...")
    app.run(host="0.0.0.0", port=port, debug=False)
