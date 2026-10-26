"""
Render Minimal, Ultra-Clean Architecture Diagram (Figure 1)
Only 6 essential components, minimal information, large bold typography.
"""

import os
import subprocess

base_dir = r"C:\Users\Sailaja C\Documents\New folder\DevOps-Incident-Watchdog"
edge_path = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
html_path = os.path.join(base_dir, "scratch", "fig1_minimal_render.html")
png_path = os.path.join(base_dir, "architecture_diagram.png")

FONT_FAMILY = "-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif"

html_content = f"""<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
* {{ box-sizing: border-box; }}
body {{
    margin: 0; padding: 20px; background: #ffffff;
    font-family: {FONT_FAMILY}; color: #0f172a;
}}
.canvas {{
    max-width: 1240px; margin: 0 auto;
    border: 2px solid #cbd5e1; border-radius: 12px;
    padding: 22px 24px; background: #f8fafc;
    box-shadow: 0 4px 15px rgba(0,0,0,0.05);
}}
.title-bar {{
    text-align: center; margin-bottom: 20px; padding-bottom: 12px;
    border-bottom: 2px solid #e2e8f0;
}}
.main-title {{
    font-size: 22px; font-weight: 800; color: #0f172a;
    text-transform: uppercase; letter-spacing: 0.5px;
}}
.sub-title {{
    font-size: 14.5px; color: #64748b; font-weight: 500; margin-top: 4px;
}}
.row-top {{
    display: flex; justify-content: space-between; align-items: center;
    gap: 8px; margin-bottom: 24px;
}}
.row-bottom {{
    display: flex; justify-content: center; align-items: center;
    gap: 24px;
}}
.card {{
    border-radius: 10px; padding: 14px 12px; text-align: center;
    border: 2px solid; background: #ffffff;
    box-shadow: 0 3px 8px rgba(0,0,0,0.04);
    flex: 1; max-width: 240px;
}}
.card-num {{
    font-size: 11.5px; font-weight: 800; text-transform: uppercase;
    letter-spacing: 0.5px; margin-bottom: 4px;
}}
.card-title {{
    font-size: 16px; font-weight: 800; margin-bottom: 4px;
    color: #0f172a;
}}
.card-sub {{
    font-size: 13px; color: #475569; font-weight: 500;
}}
.arrow-right {{
    font-size: 20px; font-weight: 900; color: #0284c7;
    display: flex; flex-direction: column; align-items: center;
    text-align: center; flex-shrink: 0; min-width: 75px;
}}
.arrow-label {{
    font-size: 11px; font-weight: 700; color: #0284c7;
    margin-bottom: 2px;
}}
.c-blue {{ border-color: #3b82f6; background: #eff6ff; }}
.c-blue .card-num {{ color: #1d4ed8; }}
.c-red {{ border-color: #ef4444; background: #fef2f2; }}
.c-red .card-num {{ color: #b91c1c; }}
.c-orange {{ border-color: #f97316; background: #fff7ed; }}
.c-orange .card-num {{ color: #c2410c; }}
.c-purple {{ border-color: #a855f7; background: #faf5ff; }}
.c-purple .card-num {{ color: #7e22ce; }}
.c-yellow {{ border-color: #eab308; background: #fefce8; }}
.c-yellow .card-num {{ color: #a16207; }}
.c-green {{ border-color: #22c55e; background: #f0fdf4; }}
.c-green .card-num {{ color: #15803d; }}

.connector-box {{
    background: #ffffff; border: 2px dashed #10b981; border-radius: 8px;
    padding: 10px 18px; font-size: 13px; font-weight: 700; color: #047857;
    text-align: center; margin-top: 18px;
}}
</style>
</head>
<body>
<div class="canvas">
    <div class="title-bar">
        <div class="main-title">DevOps Incident Watchdog: Minimal System Architecture</div>
        <div class="sub-title">High-Level Event-Driven Incident Detection, S3 Forensics, &amp; Zero-Touch Agile Remediation</div>
    </div>

    <!-- FORWARD PIPELINE -->
    <div class="row-top">
        <div class="card c-blue">
            <div class="card-num">Component 1</div>
            <div class="card-title">Client Storefront</div>
            <div class="card-sub">FlashMart SPA (VIT Hub)</div>
        </div>

        <div class="arrow-right">
            <span class="arrow-label">1. Order Request</span>
            <span>➔</span>
        </div>

        <div class="card c-red">
            <div class="card-num">Component 2</div>
            <div class="card-title">Flask Microservice</div>
            <div class="card-sub">AWS Lambda (Python 3.12)</div>
        </div>

        <div class="arrow-right">
            <span class="arrow-label" style="color:#dc2626;">2. Crash (HTTP 500)</span>
            <span style="color:#dc2626;">➔</span>
        </div>

        <div class="card c-orange">
            <div class="card-num">Component 3</div>
            <div class="card-title">Amazon CloudWatch</div>
            <div class="card-sub">Filter: [CRITICAL_ALERT]</div>
        </div>

        <div class="arrow-right">
            <span class="arrow-label" style="color:#d97706;">3. Log Trigger</span>
            <span style="color:#d97706;">➔</span>
        </div>

        <div class="card c-purple">
            <div class="card-num">Component 4</div>
            <div class="card-title">Watchdog Lambda</div>
            <div class="card-sub">Serverless SRE Triage</div>
        </div>
    </div>

    <!-- REMEDIATION & STORAGE ROW -->
    <div class="row-bottom">
        <div class="card c-green" style="max-width: 320px;">
            <div class="card-num">Component 6 &bull; Agile Board &amp; CI/CD</div>
            <div class="card-title">GitHub Issues &amp; Actions</div>
            <div class="card-sub">Bug Story #1 &bull; 9 Pytest Suite &bull; Auto-Close</div>
        </div>

        <div class="arrow-right" style="color:#7e22ce;">
            <span class="arrow-label" style="color:#7e22ce;">5. Mint Bug Story #1</span>
            <span>⬅</span>
        </div>

        <div class="arrow-right" style="color:#a16207;">
            <span class="arrow-label" style="color:#a16207;">4. S3 PutObject</span>
            <span>⬇</span>
        </div>

        <div class="card c-yellow" style="max-width: 280px;">
            <div class="card-num">Component 5 &bull; Audit Store</div>
            <div class="card-title">Amazon S3 Vault</div>
            <div class="card-sub">Immutable JSON Crash Dump</div>
        </div>
    </div>

    <div class="connector-box">
        🔁 GitOps Closed-Loop Feedback: Smart Commit "Fixes #1" passes 9 Pytest tests in GitHub Actions CI &amp; automatically closes Issue #1 in sprint backlog.
    </div>
</div>
</body>
</html>"""

with open(html_path, "w", encoding="utf-8") as f:
    f.write(html_content)

cmd = [
    edge_path,
    "--headless",
    "--disable-gpu",
    "--window-size=1280,480",
    f"--screenshot={png_path}",
    f"file:///{html_path}"
]

res = subprocess.run(cmd, capture_output=True)
if os.path.exists(png_path):
    print(f"[OK] Minimal architecture diagram generated: {os.path.getsize(png_path)} bytes")
else:
    print("[FAILED] Could not generate minimal architecture diagram")
