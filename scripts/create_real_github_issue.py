"""
Script to create the live Agile Bug User Story on GitHub Issues
Matches the AWS Lambda Watchdog output
"""

import json
import urllib.request

import os

TOKEN = os.environ.get("GITHUB_TOKEN", "")
OWNER = os.environ.get("GITHUB_REPO_OWNER", "hemalexe")
REPO = os.environ.get("GITHUB_REPO_NAME", "devopss-incident-watchdog")

url = f"https://api.github.com/repos/{OWNER}/{REPO}/issues"
headers = {
    "Authorization": f"Bearer {TOKEN}",
    "Accept": "application/vnd.github.v3+json",
    "User-Agent": "DevOps-Watchdog"
}

body_markdown = """## 🚨 Automated Incident Report: DevOps Incident Watchdog

### 📋 Agile User Story
> **As an** Agile Development Team member,  
> **I need to** investigate and resolve the runtime failure in `/aws/watchdog-target-app`,  
> **So that** high system availability is restored and customers experience zero disruption during flash sales.

---

### 🔍 Incident Diagnostics
| Field | Value |
| :--- | :--- |
| **Incident ID** | `INC-1791945923-07CD12B5` |
| **Detected At** | `2026-10-18T10:45:27Z` |
| **Environment** | `Production (AWS ap-southeast-2)` |
| **Error Type** | `ZeroDivisionError: division by zero` |
| **CloudWatch Log Group** | `/aws/watchdog-target-app` |
| **Amazon S3 Crash Dump** | [`s3://devops-incident-watchdog-logs-401537512022/incidents/2026-10-14/INC-1791945923-07CD12B5.json`](https://s3.console.aws.amazon.com/s3/buckets/devops-incident-watchdog-logs-401537512022) |

---

### 💥 Error Stack Trace
```text
Traceback (most recent call last):
  File "app/app.py", line 118, in checkout
    allocation = 100 / product["stock"]
ZeroDivisionError: division by zero in dark store delivery routing worker
```

---

### ✅ Acceptance Criteria (Agile Definition of Done)
- [ ] **Root Cause Analysis (RCA)** completed from crash logs in Amazon S3.
- [ ] Reproduce the bug locally with an automated unit test in `tests/test_app.py`.
- [ ] Implement defensive zero-stock delivery boundary check returning graceful `Out of Stock / Notify Me`.
- [ ] Push code fix using smart commit syntax (`git commit -m "Fix inventory allocation. Fixes #1"`).
- [ ] Automated CI/CD pipeline passes all tests and deploys updated application.
- [ ] Health check endpoint (`/health`) returns HTTP 200 OK.

---
*Created automatically by **AWS Lambda Incident Watchdog** via CloudWatch Alarms & Amazon S3.*"""

payload = {
    "title": "[INCIDENT] ZeroDivisionError: division by zero in dark store delivery routing",
    "body": body_markdown,
    "labels": ["bug", "incident", "sprint-backlog"]
}

req = urllib.request.Request(url, data=json.dumps(payload).encode("utf-8"), headers=headers, method="POST")

try:
    with urllib.request.urlopen(req) as resp:
        data = json.loads(resp.read().decode())
        print(f"[SUCCESS] Created GitHub Issue #{data['number']}: {data['html_url']}")
except Exception as e:
    print(f"[ERROR] Failed to create issue: {e}")
