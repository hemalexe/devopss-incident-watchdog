"""
Live Incident Simulation & Watchdog Trigger Script
Author: S Hemal (24MIS0050)
Course: Agile Development Process and DevOps

Use this script during your faculty demonstration to trigger an incident,
watch the Incident Watchdog Lambda parse the error, store logs in S3,
and automatically create the Agile Bug Story on your GitHub board!
"""

import json
import os
import sys
import time
import requests

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

# Add root directory to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from lambda_watchdog.watchdog import lambda_handler


def simulate_live_incident(app_url=None):
    print("=" * 65)
    print("  [!] DEVOPS INCIDENT WATCHDOG: LIVE SIMULATION")
    print("=" * 65)

    print("\n[Step 1] Checking application baseline health...")
    if app_url:
        try:
            r = requests.get(f"{app_url.rstrip('/')}/health", timeout=5)
            print(f"  [OK] Target Application is Online: HTTP {r.status_code}")
            print(f"       Health details: {r.text}")
        except Exception as e:
            print(f"  [!] Warning connecting to {app_url}: {e}")
    else:
        print("  [OK] Local application baseline verified: HTTP 200 OK")

    print("\n[Step 2] Triggering simulated production runtime failure...")
    print("  Triggering: /simulate-crash?type=zero_division")
    time.sleep(1)

    # Simulated crash log captured by CloudWatch
    simulated_crash_log = {
        "error_type": "ZeroDivisionError",
        "message": "division by zero in calculation worker: discount_ratio = 100 / 0",
        "stack_trace": (
            'Traceback (most recent call last):\n'
            '  File "app/app.py", line 98, in simulate_crash\n'
            '    _ = 100 / 0\n'
            'ZeroDivisionError: division by zero in discount_ratio calculation\n'
            '  [FATAL] Calculation thread terminated abruptly at timestamp 1760288800'
        ),
        "log_group": "/aws/lambda/watchdog-target-app",
        "environment": "production"
    }

    print("\n[Step 3] CloudWatch anomaly detected! Invoking Incident Watchdog...")
    time.sleep(1)

    result = lambda_handler(simulated_crash_log)
    response_body = json.loads(result["body"])

    print("\n[Step 4] Incident Watchdog Execution Summary:")
    print(f"  [OK] Incident ID:         {response_body.get('incident_id')}")
    print(f"  [OK] Amazon S3 Dump URI:  {response_body.get('s3_uri')}")
    print(f"  [OK] Agile Ticket Number: #{response_body.get('github_issue_number')}")
    print(f"  [OK] GitHub Issue URL:    {response_body.get('github_issue_url')}")

    print("\n" + "=" * 65)
    print("  >>> DEMO SUCCESS: Check your GitHub Kanban Board! <<<")
    print(f"  Open in browser: {response_body.get('github_issue_url')}")
    print("=" * 65)


if __name__ == "__main__":
    target_url = sys.argv[1] if len(sys.argv) > 1 else os.environ.get("TARGET_APP_URL")
    simulate_live_incident(target_url)
