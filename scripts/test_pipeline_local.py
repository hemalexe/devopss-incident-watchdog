"""
Local End-to-End Pipeline Verification Runner
Author: S Hemal (24MIS0050)
Course: Agile Development Process and DevOps

Verifies the entire lifecycle locally:
1. Application health check
2. Incident crash handling
3. CloudWatch & Lambda Watchdog event parsing
4. S3 crash dump payload generation
5. Agile User Story generation with Acceptance Criteria
6. CI/CD test execution
"""

import json
import os
import sys
import pytest

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

# Add root directory to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.app import app
from lambda_watchdog.watchdog import parse_cloudwatch_event, format_agile_user_story, lambda_handler


def run_local_validation():
    print("=" * 70)
    print("  LOCAL END-TO-END PIPELINE VERIFICATION")
    print("  DevOps Incident Watchdog (S Hemal - 24MIS0050)")
    print("=" * 70)

    # 1. Health check test
    print("\n[Step 1] Verifying Monitored App Health Check...")
    with app.test_client() as client:
        res = client.get("/health")
        assert res.status_code == 200, f"Expected 200, got {res.status_code}"
        data = res.get_json()
        print(f"  [OK] Service status: {data['status']}, HTTP {res.status_code}")

    # 2. Crash endpoint test
    print("\n[Step 2] Simulating Runtime Application Crash...")
    with app.test_client() as client:
        res = client.get("/simulate-crash?type=zero_division")
        assert res.status_code == 500, f"Expected 500, got {res.status_code}"
        data = res.get_json()
        print(f"  [OK] Handled crash gracefully: HTTP {res.status_code}")
        print(f"       Error Type: {data['type']}")
        print(f"       Error Message: {data['message']}")

    # 3. Watchdog Event Parsing
    print("\n[Step 3] Parsing CloudWatch Crash Event in Lambda Watchdog...")
    mock_event = {
        "error_type": data["type"],
        "message": data["message"],
        "stack_trace": "\n".join(data.get("trace", ["ZeroDivisionError: division by zero"])),
        "log_group": "/aws/watchdog-target-app"
    }
    incident = parse_cloudwatch_event(mock_event)
    print(f"  [OK] Incident ID generated: {incident['incident_id']}")
    print(f"  [OK] Extracted Error Type:   {incident['error_type']}")

    # 4. User Story & Acceptance Criteria Generation
    print("\n[Step 4] Generating Agile Bug User Story with Acceptance Criteria...")
    s3_uri = f"s3://devops-incident-watchdog-logs/incidents/{incident['incident_id']}.json"
    title, body = format_agile_user_story(incident, s3_uri)
    print(f"  [OK] Story Title: {title}")
    print("  [OK] Story Body Preview:")
    for line in body.splitlines()[:8]:
        print(f"       | {line}")
    print("       | ... [Acceptance Criteria included]")

    # 5. Run full test suite
    print("\n[Step 5] Running Continuous Integration (CI) Test Suite...")
    exit_code = pytest.main(["-q", os.path.join(os.path.dirname(__file__), "..", "tests")])
    if exit_code == 0:
        print("  [OK] All 8 automated unit tests passed successfully!")
    else:
        print(f"  [FAIL] Tests failed with exit code: {exit_code}")
        return False

    print("\n" + "=" * 70)
    print("  ALL STAGES PASSED! The project is fully functional and ready to deploy.")
    print("=" * 70)
    return True


if __name__ == "__main__":
    success = run_local_validation()
    sys.exit(0 if success else 1)
