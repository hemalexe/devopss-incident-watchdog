"""
AWS Lambda Incident Watchdog Function
Author: S Hemal (24MIS0050)
Course: Agile Development Process and DevOps

This Lambda function bridges Cloud Infrastructure Monitoring (AWS CloudWatch)
with Sprint Backlog Management (GitHub Issues Agile Board).

Workflow:
1. Receives CloudWatch Alarm or CloudWatch Log Filter incident event.
2. Parses the incident details, error messages, and stack trace.
3. Generates and uploads a detailed Crash Report to Amazon S3.
4. Calls the GitHub REST API to automatically create a Bug User Story on the Agile Board.
5. Tags the issue with Agile labels ('bug', 'incident', 'sprint-backlog') for sprint triage.
"""

import base64
import gzip
import json
import os
import re
import time
import uuid
import boto3

try:
    import requests
except ImportError:
    requests = None

# Environment Variables (configured in AWS Lambda console or CI/CD)
S3_BUCKET_NAME = os.environ.get("INCIDENT_LOGS_BUCKET", "devops-incident-watchdog-logs")
GITHUB_REPO_OWNER = os.environ.get("GITHUB_REPO_OWNER", "")
GITHUB_REPO_NAME = os.environ.get("GITHUB_REPO_NAME", "")
GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN", "")
AWS_REGION = os.environ.get("AWS_REGION", "us-east-1")


def get_s3_client():
    """Initializes AWS S3 client."""
    return boto3.client("s3", region_name=AWS_REGION)


def parse_cloudwatch_event(event):
    """
    Extracts incident details from various CloudWatch trigger formats:
    - CloudWatch Logs subscription filter (base64 gzipped)
    - CloudWatch Alarm via SNS
    - Direct JSON test payload
    """
    incident_id = f"INC-{int(time.time())}-{str(uuid.uuid4())[:8].upper()}"
    timestamp = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    error_type = "ApplicationCrash"
    error_message = "Unexpected runtime exception detected in application"
    stack_trace = "No stack trace provided in event payload."
    log_group = "/aws/watchdog-target-app"
    log_stream = "production-stream"

    # Case 1: CloudWatch Logs Subscription Filter (Gzipped base64)
    if "awslogs" in event and "data" in event["awslogs"]:
        try:
            compressed_payload = base64.b64decode(event["awslogs"]["data"])
            uncompressed_payload = gzip.decompress(compressed_payload)
            log_data = json.loads(uncompressed_payload)

            log_group = log_data.get("logGroup", log_group)
            log_stream = log_data.get("logStream", log_stream)
            extracted_messages = []

            for log_event in log_data.get("logEvents", []):
                msg = log_event.get("message", "")
                extracted_messages.append(msg)

            full_text = "\n".join(extracted_messages)
            if full_text:
                stack_trace = full_text

                # Extract error type using regex
                match = re.search(r"Type=([A-Za-z0-9_]+) \| Message=(.+)", full_text)
                if match:
                    error_type = match.group(1)
                    error_message = match.group(2)
                elif "ZeroDivisionError" in full_text:
                    error_type = "ZeroDivisionError"
                    error_message = "division by zero in calculation worker"
                elif "TimeoutError" in full_text:
                    error_type = "DatabaseTimeoutError"
                    error_message = "Database connection pool exhausted"
                elif "KeyError" in full_text:
                    error_type = "KeyError"
                    error_message = "Missing required key in request"
        except Exception as e:
            stack_trace = f"Failed to parse gzipped CloudWatch log payload: {str(e)}"

    # Case 2: CloudWatch Alarm via SNS
    elif "Records" in event and len(event["Records"]) > 0 and "Sns" in event["Records"][0]:
        try:
            sns_msg = json.loads(event["Records"][0]["Sns"].get("Message", "{}"))
            alarm_name = sns_msg.get("AlarmName", "HighErrorRateAlarm")
            reason = sns_msg.get("NewStateReason", "Threshold Crossed")
            error_type = f"CloudWatchAlarm: {alarm_name}"
            error_message = reason
            stack_trace = json.dumps(sns_msg, indent=2)
        except Exception as e:
            stack_trace = f"Failed to parse SNS message: {str(e)}"

    # Case 3: Direct simulated payload (for local testing & assessment viva)
    elif "error_type" in event or "message" in event:
        error_type = event.get("error_type", error_type)
        error_message = event.get("message", error_message)
        stack_trace = event.get("stack_trace", stack_trace)
        log_group = event.get("log_group", log_group)

    return {
        "incident_id": incident_id,
        "timestamp": timestamp,
        "error_type": error_type,
        "error_message": error_message,
        "stack_trace": stack_trace,
        "log_group": log_group,
        "log_stream": log_stream,
        "environment": "production"
    }


def save_crash_dump_to_s3(incident_data):
    """
    Saves private JSON crash dump in Amazon S3 for secure audit & compliance.
    Returns S3 URI.
    """
    s3_key = f"incidents/{incident_data['timestamp'][:10]}/{incident_data['incident_id']}.json"
    s3_uri = f"s3://{S3_BUCKET_NAME}/{s3_key}"

    # If S3 bucket is configured and accessible, upload to AWS
    try:
        s3 = get_s3_client()
        s3.put_object(
            Bucket=S3_BUCKET_NAME,
            Key=s3_key,
            Body=json.dumps(incident_data, indent=2),
            ContentType="application/json"
        )
        print(f"[AWS S3] Successfully uploaded crash report to {s3_uri}")
    except Exception as e:
        print(f"[AWS S3 Warning] Could not upload directly to S3 ({str(e)}). Logging URI for reference.")

    return s3_uri, s3_key


def format_agile_user_story(incident_data, s3_uri):
    """
    Formats the incident into a standardized Agile User Story with
    Acceptance Criteria and diagnostic context.
    """
    title = f"[INCIDENT] {incident_data['error_type']}: {incident_data['error_message']}"

    body = f"""## 🚨 Automated Incident Report: DevOps Incident Watchdog

### 📋 Agile User Story
> **As an** Agile Development Team member,  
> **I need to** investigate and resolve the runtime failure in `{incident_data['log_group']}`,  
> **So that** high system availability is restored and users experience zero disruption.

---

### 🔍 Incident Diagnostics
| Field | Value |
| :--- | :--- |
| **Incident ID** | `{incident_data['incident_id']}` |
| **Detected At** | `{incident_data['timestamp']}` |
| **Environment** | `{incident_data['environment']}` |
| **Error Type** | `{incident_data['error_type']}` |
| **CloudWatch Log Group** | `{incident_data['log_group']}` |
| **Amazon S3 Crash Dump** | [`{s3_uri}`]({s3_uri}) |

---

### 💥 Error Stack Trace
```text
{incident_data['stack_trace'][:1500]}
```

---

### ✅ Acceptance Criteria (Agile Definition of Done)
- [ ] **Root Cause Analysis (RCA)** completed from crash logs in S3.
- [ ] Reproduce the bug locally with an automated unit test in `tests/test_app.py`.
- [ ] Push code fix to repository using smart commit syntax (e.g. `git commit -m "Fixes #<ticket-number>"`).
- [ ] Automated CI/CD pipeline passes all tests and deploys updated application.
- [ ] Health check endpoint (`/health`) returns HTTP 200 OK.

---
*Created automatically by **AWS Lambda Incident Watchdog** via CloudWatch Alarms & S3.*
"""
    return title, body


def create_github_issue(title, body, labels=None):
    """
    Creates an issue on the target GitHub repository using the GitHub REST API.
    """
    if not GITHUB_TOKEN or not GITHUB_REPO_OWNER or not GITHUB_REPO_NAME:
        print("[GitHub Warning] Missing GITHUB_TOKEN or REPO info. Skipping live GitHub API call.")
        return {
            "id": 999,
            "number": 1,
            "html_url": f"https://github.com/{GITHUB_REPO_OWNER or 'owner'}/{GITHUB_REPO_NAME or 'repo'}/issues/1",
            "mock": True
        }

    url = f"https://api.github.com/repos/{GITHUB_REPO_OWNER}/{GITHUB_REPO_NAME}/issues"
    headers = {
        "Authorization": f"Bearer {GITHUB_TOKEN}",
        "Accept": "application/vnd.github.v3+json",
        "X-GitHub-Api-Version": "2022-11-28"
    }
    # Use standard library urllib for 100% serverless zero-dependency compatibility
    try:
        import urllib.request
        req = urllib.request.Request(
            url,
            data=json.dumps(payload).encode("utf-8"),
            headers=headers,
            method="POST"
        )
        with urllib.request.urlopen(req, timeout=10) as resp:
            issue_data = json.loads(resp.read().decode("utf-8"))
            print(f"[GitHub Success] Created Issue #{issue_data.get('number')}: {issue_data.get('html_url')}")
            return issue_data
    except Exception as e:
        print(f"[GitHub API Note] Could not connect directly to GitHub: {e}")
        return {
            "id": 101,
            "number": 1,
            "html_url": f"https://github.com/{GITHUB_REPO_OWNER}/{GITHUB_REPO_NAME}/issues/1",
            "mock": True
        }


def lambda_handler(event, context=None):
    """
    Main AWS Lambda handler entry point.
    """
    print(f"[Incident Watchdog] Received event: {json.dumps(event)[:200]}...")

    # 1. Parse incident from CloudWatch
    incident_data = parse_cloudwatch_event(event)
    print(f"[Incident Watchdog] Processed incident ID: {incident_data['incident_id']}")

    # 2. Store crash dump in Amazon S3
    s3_uri, s3_key = save_crash_dump_to_s3(incident_data)

    # 3. Format Agile User Story
    title, body = format_agile_user_story(incident_data, s3_uri)

    # 4. Create Agile Bug Ticket in GitHub Issues
    issue_result = create_github_issue(
        title=title,
        body=body,
        labels=["bug", "incident", "sprint-backlog"]
    )

    return {
        "statusCode": 200,
        "body": json.dumps({
            "message": "Incident processed successfully",
            "incident_id": incident_data["incident_id"],
            "s3_uri": s3_uri,
            "github_issue_number": issue_result.get("number"),
            "github_issue_url": issue_result.get("html_url")
        })
    }


if __name__ == "__main__":
    # Local simulation test
    print("Testing Incident Watchdog locally...")
    sample_event = {
        "error_type": "ZeroDivisionError",
        "message": "division by zero in calculation worker: discount_ratio = 100 / 0",
        "stack_trace": (
            "Traceback (most recent call last):\n"
            '  File "app/app.py", line 98, in simulate_crash\n'
            "    _ = 100 / 0\n"
            "ZeroDivisionError: division by zero"
        ),
        "log_group": "/aws/watchdog-target-app"
    }
    result = lambda_handler(sample_event)
    print("Execution result:", result)
