"""
Unit Tests for Incident Watchdog Lambda
Validates log parsing, S3 dump formatting, and Agile User Story generation.
"""

import sys
import os
import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from lambda_watchdog.watchdog import parse_cloudwatch_event, format_agile_user_story


def test_parse_cloudwatch_direct_event():
    """Test parsing simulated direct incident event."""
    sample_event = {
        "error_type": "ZeroDivisionError",
        "message": "division by zero",
        "stack_trace": "line 98, in simulate_crash\n  _ = 100 / 0",
        "log_group": "/aws/watchdog-target-app"
    }
    parsed = parse_cloudwatch_event(sample_event)
    assert parsed["error_type"] == "ZeroDivisionError"
    assert "division by zero" in parsed["error_message"]
    assert "INC-" in parsed["incident_id"]
    assert parsed["log_group"] == "/aws/watchdog-target-app"


def test_format_agile_user_story():
    """Test formatting incident into an Agile User Story with acceptance criteria."""
    incident_data = {
        "incident_id": "INC-TEST-123",
        "timestamp": "2026-10-12T16:00:00Z",
        "environment": "production",
        "error_type": "DatabaseTimeoutError",
        "error_message": "RDS connection pool exhausted",
        "log_group": "/aws/watchdog-target-app",
        "stack_trace": "TimeoutError: connection timed out after 30000ms"
    }
    s3_uri = "s3://devops-incident-watchdog-logs/incidents/2026-10-12/INC-TEST-123.json"

    title, body = format_agile_user_story(incident_data, s3_uri)

    # Validate title formatting
    assert "[INCIDENT] DatabaseTimeoutError: RDS connection pool exhausted" == title

    # Validate Agile structure
    assert "Agile User Story" in body
    assert "Acceptance Criteria" in body
    assert s3_uri in body
    assert "INC-TEST-123" in body
    assert "TimeoutError" in body
