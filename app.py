"""
DevOps Incident Watchdog Entry Point
Student: S Hemal (24MIS0050)
Course: Agile Development Process and DevOps
"""

import os
from app.app import app

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    print(f"Starting DevOps Incident Watchdog Target App on http://localhost:{port}...")
    app.run(host="0.0.0.0", port=port, debug=True)
