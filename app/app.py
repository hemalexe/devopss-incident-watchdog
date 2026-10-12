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

# Mock in-memory database of items
CATALOG = [
    {"id": 1, "name": "Cloud DevOps Textbook", "price": 45.0, "stock": 10},
    {"id": 2, "name": "Agile Sprint Planner", "price": 25.0, "stock": 5},
    {"id": 3, "name": "AWS Architecture Handbook", "price": 55.0, "stock": 2},
]


@app.route("/", methods=["GET"])
def index():
    """Root endpoint with service metadata."""
    return jsonify({
        "service": "DevOps Incident Watchdog Monitored App",
        "student": "S Hemal (24MIS0050)",
        "version": APP_VERSION,
        "status": "online",
        "endpoints": {
            "health": "/health",
            "products": "/api/products",
            "checkout": "/api/checkout (POST)",
            "simulate_crash": "/simulate-crash"
        }
    }), 200


@app.route("/health", methods=["GET"])
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
    Can be used to test normal operation or deliberate edge case errors.
    """
    data = request.get_json(silent=True) or {}
    product_id = data.get("product_id")
    quantity = data.get("quantity", 1)

    product = next((p for p in CATALOG if p["id"] == product_id), None)
    if not product:
        return jsonify({"error": "Product not found"}), 404

    # Calculation logic
    total = product["price"] * quantity
    logger.info(f"Checkout processed for product_id={product_id}, qty={quantity}, total=${total}")
    return jsonify({
        "status": "order_confirmed",
        "product": product["name"],
        "quantity": quantity,
        "total_amount": total
    }), 200


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
