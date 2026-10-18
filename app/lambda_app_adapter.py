"""
AWS Lambda Serverless Handler
Author: S Hemal (24MIS0050)
Course: Agile Development Process and DevOps

Serves the Flash Sale Store, Health Check, and Checkout failure simulation
directly on AWS Lambda with Function URLs. Zero external dependencies required.
"""

import json
import os
import sys
import time
import traceback

BUG_FIXED = False
START_TIME = time.time()

CATALOG = [
    {"id": 1, "name": "Apple MacBook Air M3 (16GB, 256GB SSD)", "price": 45.0, "stock": 10},
    {"id": 2, "name": "Sony WH-1000XM5 ANC Headphones", "price": 25.0, "stock": 5},
    {"id": 3, "name": "OnePlus 11R 5G (Sonic Black, 16GB)", "price": 55.0, "stock": 0},
    {"id": 4, "name": "Apple Watch Series 9 GPS (45mm)", "price": 35.0, "stock": 6},
]


def get_html_page():
    """Loads the HTML store page."""
    base_dir = os.path.dirname(os.path.abspath(__file__))
    candidates = [
        os.path.join(base_dir, "templates", "index.html"),
        os.path.join(base_dir, "..", "templates", "index.html"),
        os.path.join(base_dir, "index.html"),
    ]
    for path in candidates:
        if os.path.exists(path):
            with open(path, "r", encoding="utf-8") as f:
                return f.read()
    return "<h1>Cloud Store (Flash Sale Service) - S Hemal (24MIS0050)</h1>"


def lambda_handler(event, context=None):
    """
    Main entry point for AWS Lambda Function URL or API Gateway.
    """
    global BUG_FIXED

    # Determine HTTP Method and Path
    http_method = event.get("requestContext", {}).get("http", {}).get("method") or event.get("httpMethod", "GET")
    raw_path = event.get("rawPath") or event.get("path", "/")

    print(f"[AWS Lambda App] Incoming request: {http_method} {raw_path}")

    # Root route: Serve HTML store
    if raw_path == "/" and http_method == "GET":
        html = get_html_page()
        return {
            "statusCode": 200,
            "headers": {"Content-Type": "text/html; charset=utf-8"},
            "body": html
        }

    # Health check route
    if raw_path in ("/health", "/api/health"):
        return {
            "statusCode": 200,
            "headers": {"Content-Type": "application/json"},
            "body": json.dumps({
                "status": "healthy",
                "service": "watchdog-target-app",
                "version": "1.0.0",
                "uptime_seconds": int(time.time() - START_TIME),
                "http_status": 200
            })
        }

    # Products route
    if raw_path == "/api/products":
        return {
            "statusCode": 200,
            "headers": {"Content-Type": "application/json"},
            "body": json.dumps({"count": len(CATALOG), "products": CATALOG})
        }

    # DevOps status
    if raw_path == "/api/devops/status":
        return {
            "statusCode": 200,
            "headers": {"Content-Type": "application/json"},
            "body": json.dumps({"bug_fixed": BUG_FIXED})
        }

    # DevOps apply-fix
    if raw_path == "/api/devops/apply-fix":
        BUG_FIXED = True
        return {
            "statusCode": 200,
            "headers": {"Content-Type": "application/json"},
            "body": json.dumps({
                "status": "deployed",
                "message": "CI/CD Pipeline: Patch deployed successfully. Zero-touch ticket closed as Done.",
                "bug_fixed": True
            })
        }

    # DevOps reset
    if raw_path == "/api/devops/reset":
        BUG_FIXED = False
        return {
            "statusCode": 200,
            "headers": {"Content-Type": "application/json"},
            "body": json.dumps({"status": "reset", "bug_fixed": False})
        }

    # Checkout route
    if raw_path == "/api/checkout" and http_method == "POST":
        body_str = event.get("body", "{}")
        if event.get("isBase64Encoded", False):
            import base64
            body_str = base64.b64decode(body_str).decode("utf-8")
        try:
            data = json.loads(body_str) if body_str else {}
        except Exception:
            data = {}

        product_id = data.get("product_id")
        product = next((p for p in CATALOG if p["id"] == product_id), None)

        if product and product["stock"] <= 0:
            if not BUG_FIXED:
                # The flash sale crash!
                print("[CRITICAL_ALERT] Incident simulation triggered! Item has stock=0")
                print("[INCIDENT_DETECTED] Type=ZeroDivisionError | Message=division by zero in delivery worker")
                try:
                    _ = 100 / product["stock"]  # Divide by zero!
                except Exception as e:
                    trace = traceback.format_exc()
                    print(f"--- STACK TRACE ---\n{trace}\n--- END TRACE ---")
                    return {
                        "statusCode": 500,
                        "headers": {"Content-Type": "application/json"},
                        "body": json.dumps({
                            "error": "InternalServerError",
                            "type": "ZeroDivisionError",
                            "message": "division by zero in delivery routing worker"
                        })
                    }
            else:
                return {
                    "statusCode": 400,
                    "headers": {"Content-Type": "application/json"},
                    "body": json.dumps({
                        "status": "out_of_stock",
                        "message": f"Sorry, '{product['name']}' is out of stock / isn't available!"
                    })
                }

        return {
            "statusCode": 200,
            "headers": {"Content-Type": "application/json"},
            "body": json.dumps({
                "status": "order_confirmed",
                "product": product["name"] if product else "Item",
                "message": "Order placed successfully"
            })
        }

    # Direct simulate-crash endpoint
    if raw_path.startswith("/simulate-crash"):
        print("[CRITICAL_ALERT] Incident simulation triggered!")
        print("[INCIDENT_DETECTED] Type=ZeroDivisionError | Message=division by zero")
        return {
            "statusCode": 500,
            "headers": {"Content-Type": "application/json"},
            "body": json.dumps({
                "error": "InternalServerError",
                "type": "ZeroDivisionError",
                "message": "division by zero in calculation worker"
            })
        }

    return {
        "statusCode": 404,
        "headers": {"Content-Type": "application/json"},
        "body": json.dumps({"error": "Not Found"})
    }
