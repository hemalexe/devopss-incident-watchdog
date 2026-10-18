import subprocess
import os

edge_path = r'C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe'

# -------------------------------------------------------------
# 1. Figure 2: End-to-End Workflow Diagram
# -------------------------------------------------------------
fig2_html = """<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
body { margin: 0; padding: 15px; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; background: #ffffff; }
.flow-container { display: flex; align-items: center; justify-content: center; gap: 8px; max-width: 1100px; margin: 0 auto; }
.card { width: 130px; height: 100px; border-radius: 6px; padding: 8px; text-align: center; font-size: 10.5px; display: flex; flex-direction: column; justify-content: center; border: 1.5px solid #cbd5e1; box-shadow: 0 1px 3px rgba(0,0,0,0.05); }
.c1 { background: #eff6ff; border-color: #3b82f6; }
.c2 { background: #fef2f2; border-color: #ef4444; }
.c3 { background: #fff7ed; border-color: #f97316; }
.c4 { background: #faf5ff; border-color: #a855f7; }
.c5 { background: #fefce8; border-color: #eab308; }
.c6 { background: #f0fdf4; border-color: #22c55e; }
.c7 { background: #ecfeff; border-color: #06b6d4; }
.title { font-weight: bold; font-size: 11px; margin-bottom: 4px; }
.arrow { font-size: 16px; color: #64748b; font-weight: bold; }
</style>
</head>
<body>
<div style="text-align:center; font-weight:bold; font-size:13px; margin-bottom:12px; text-transform:uppercase; color:#1e293b;">Figure 2: End-to-End Autonomous Incident-to-Agile Remediation Workflow</div>
<div class="flow-container">
  <div class="card c1">
    <div class="title" style="color:#1d4ed8;">1. Order Dispatch</div>
    <div>Customer checkout on FlashMart Storefront (VIT Hub)</div>
  </div>
  <div class="arrow">&rarr;</div>
  <div class="card c2">
    <div class="title" style="color:#b91c1c;">2. Fault Execution</div>
    <div>Zero-stock division (100/stock) throws HTTP 500</div>
  </div>
  <div class="arrow">&rarr;</div>
  <div class="card c3">
    <div class="title" style="color:#c2410c;">3. Filter Ingestion</div>
    <div>CloudWatch pattern [CRITICAL_ALERT] fires alarm</div>
  </div>
  <div class="arrow">&rarr;</div>
  <div class="card c4">
    <div class="title" style="color:#7e22ce;">4. SRE Triage</div>
    <div>Lambda Watchdog parses gzip traceback &amp; mints ID</div>
  </div>
  <div class="arrow">&rarr;</div>
  <div class="card c5">
    <div class="title" style="color:#a16207;">5. S3 Forensic Vault</div>
    <div>Stores immutable JSON dump (11 9's durability)</div>
  </div>
  <div class="arrow">&rarr;</div>
  <div class="card c6">
    <div class="title" style="color:#15803d;">6. Agile Story Creator</div>
    <div>Mints GitHub Issue #1 with DoD checkboxes &amp; labels</div>
  </div>
  <div class="arrow">&rarr;</div>
  <div class="card c7">
    <div class="title" style="color:#0e7490;">7. CI/CD &amp; Close</div>
    <div>Smart Commit Fixes #1 runs 9 pytest tests &amp; auto-closes</div>
  </div>
</div>
</body>
</html>"""

# -------------------------------------------------------------
# 2. Figure 3: Safety Gate Architecture Diagram
# -------------------------------------------------------------
fig3_html = """<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
body { margin: 0; padding: 15px; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; background: #ffffff; }
.gates-container { display: flex; justify-content: center; gap: 10px; max-width: 1100px; margin: 0 auto; flex-wrap: wrap; }
.gate-box { width: 145px; border-radius: 6px; padding: 10px; font-size: 10px; text-align: center; border: 1.5px solid #0284c7; background: #f0f9ff; }
.gate-num { font-weight: 800; font-size: 11px; color: #0369a1; margin-bottom: 4px; text-transform: uppercase; }
.gate-title { font-weight: bold; color: #0f172a; margin-bottom: 4px; font-size: 10.5px; }
.gate-desc { color: #475569; line-height: 1.3; }
</style>
</head>
<body>
<div style="text-align:center; font-weight:bold; font-size:13px; margin-bottom:12px; text-transform:uppercase; color:#0f172a;">Figure 3: Closed-Loop Telemetry and GitOps Security Safety Gate Architecture</div>
<div class="gates-container">
  <div class="gate-box">
    <div class="gate-num">Gate 1: Ingestion</div>
    <div class="gate-title">Read-Only Telemetry</div>
    <div class="gate-desc">Non-invasive CloudWatch log subscriptions; zero write access to app state.</div>
  </div>
  <div class="gate-box">
    <div class="gate-num">Gate 2: Isolation</div>
    <div class="gate-title">Serverless Sandbox</div>
    <div class="gate-desc">Isolated AWS Lambda execution environment with ephemeral /tmp storage.</div>
  </div>
  <div class="gate-box">
    <div class="gate-num">Gate 3: Durability</div>
    <div class="gate-title">S3 Immutable Vault</div>
    <div class="gate-desc">Private bucket with Block Public Access and cryptographic JSON payload hashing.</div>
  </div>
  <div class="gate-box">
    <div class="gate-num">Gate 4: Security</div>
    <div class="gate-title">Least-Privilege IAM</div>
    <div class="gate-desc">Role restricted strictly to S3 PutObject and CloudWatch logging.</div>
  </div>
  <div class="gate-box">
    <div class="gate-num">Gate 5: Backlog</div>
    <div class="gate-title">Sanitized User Story</div>
    <div class="gate-desc">GitHub REST API token masked; zero PII or credentials in ticket body.</div>
  </div>
  <div class="gate-box">
    <div class="gate-num">Gate 6: Verification</div>
    <div class="gate-title">Automated Pytest CI</div>
    <div class="gate-desc">GitHub Actions enforces 9 regression unit tests before deployment approval.</div>
  </div>
  <div class="gate-box">
    <div class="gate-num">Gate 7: Traceability</div>
    <div class="gate-title">Smart Commit Linking</div>
    <div class="gate-desc">Commit SHA explicitly linked to Issue #1 via GitOps Fixes syntax.</div>
  </div>
</div>
</body>
</html>"""

# -------------------------------------------------------------
# 3. Figure 4: AWS Serverless Production Topology
# -------------------------------------------------------------
fig4_html = """<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
body { margin: 0; padding: 15px; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; background: #ffffff; }
.topo-box { border: 2px dashed #0284c7; background: #f8fafc; border-radius: 8px; padding: 15px; max-width: 1050px; margin: 0 auto; }
.topo-title { font-weight: bold; font-size: 13px; color: #0369a1; margin-bottom: 12px; display: flex; justify-content: space-between; }
.grid { display: grid; grid-template-columns: repeat(4, 1fr); gap: 12px; }
.node { background: #ffffff; border: 1.5px solid #cbd5e1; border-radius: 6px; padding: 12px; font-size: 10.5px; }
.node-title { font-weight: bold; font-size: 11.5px; margin-bottom: 4px; }
</style>
</head>
<body>
<div class="topo-box">
  <div class="topo-title">
    <span>AWS CLOUD PRODUCTION TOPOLOGY (ap-southeast-2 Sydney &bull; Account: 401537512022)</span>
    <span style="color:#16a34a;">Status: 100% Active &amp; Verified</span>
  </div>
  <div class="grid">
    <div class="node" style="border-top: 3px solid #3b82f6;">
      <div class="node-title" style="color:#1d4ed8;">watchdog-target-app</div>
      <div style="color:#64748b;">AWS Lambda (Python 3.12)</div>
      <div style="margin-top:6px;">&bull; 128 MB RAM &bull; Function URL<br>&bull; Hosts FlashMart Storefront<br>&bull; Multi-Address Campus Routing</div>
    </div>
    <div class="node" style="border-top: 3px solid #f97316;">
      <div class="node-title" style="color:#c2410c;">CloudWatch Logs</div>
      <div style="color:#64748b;">Log Group: /aws/lambda/...</div>
      <div style="margin-top:6px;">&bull; Real-time stdout capture<br>&bull; Metric Filter: [CRITICAL_ALERT]<br>&bull; CloudWatch Alarm Trigger</div>
    </div>
    <div class="node" style="border-top: 3px solid #a855f7;">
      <div class="node-title" style="color:#7e22ce;">watchdog-incident-creator</div>
      <div style="color:#64748b;">AWS Lambda (Python 3.12)</div>
      <div style="margin-top:6px;">&bull; Serverless Triage Orchestrator<br>&bull; Gzip Traceback Decompressor<br>&bull; Boto3 S3 &amp; GitHub REST API</div>
    </div>
    <div class="node" style="border-top: 3px solid #eab308;">
      <div class="node-title" style="color:#a16207;">Amazon S3 Forensic Vault</div>
      <div style="color:#64748b;">devops-incident-watchdog-logs</div>
      <div style="margin-top:6px;">&bull; S3 Standard (Private Bucket)<br>&bull; Key: incidents/YYYY-MM-DD/...<br>&bull; 11 9's Durability Audit Store</div>
    </div>
  </div>
</div>
</body>
</html>"""

os.makedirs('scratch', exist_ok=True)
files = [
    ('scratch/fig2_render.html', fig2_html, 'figure2_workflow.png', 1150, 180),
    ('scratch/fig3_render.html', fig3_html, 'figure3_safety_gates.png', 1150, 180),
    ('scratch/fig4_render.html', fig4_html, 'figure4_aws_topology.png', 1150, 200)
]

for html_p, content, out_png, w, h in files:
    with open(html_p, 'w', encoding='utf-8') as f:
        f.write(content)
    out_abs = os.path.abspath(out_png)
    html_abs = os.path.abspath(html_p)
    subprocess.run([edge_path, '--headless', '--disable-gpu', f'--window-size={w},{h}', f'--screenshot={out_abs}', f'file:///{html_abs}'])
    print(f'{out_png} generated:', os.path.exists(out_abs), os.path.getsize(out_abs) if os.path.exists(out_abs) else 0)

print('All 3 diagrams rendered successfully!')
