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

# Catalog of items (Item 3 has 0 stock to demonstrate the Zepto flash sale crash)
CATALOG = [
    {"id": 1, "name": "Apple MacBook Air M3 (16GB, 256GB SSD)", "price": 45.0, "stock": 10},
    {"id": 2, "name": "Sony WH-1000XM5 ANC Headphones", "price": 25.0, "stock": 5},
    {"id": 3, "name": "OnePlus 11R 5G (Sonic Black, 16GB)", "price": 55.0, "stock": 0},
    {"id": 4, "name": "Apple Watch Series 9 GPS (45mm)", "price": 35.0, "stock": 6},
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
def get_products():
    """Returns catalog of products."""
    logger.info("Fetched product catalog successfully.")
    return jsonify({
        "count": len(CATALOG),
        "products": CATALOG
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
