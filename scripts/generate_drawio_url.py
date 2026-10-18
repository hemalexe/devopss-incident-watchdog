import zlib
import base64
import urllib.parse
import os

with open('DevOps_Incident_Watchdog_Architecture.drawio', 'r', encoding='utf-8') as f:
    xml_str = f.read()

# Raw DEFLATE compression compatible with Draw.io #R parameter
compressed = zlib.compress(xml_str.encode('utf-8'))[2:-4]
b64 = base64.b64encode(compressed).decode('ascii')
drawio_url = 'https://app.diagrams.net/#R' + urllib.parse.quote(b64)

print('Generated Draw.io URL length:', len(drawio_url))

# Write internet shortcut
with open('Open_Architecture_In_Drawio.url', 'w', encoding='utf-8') as f:
    f.write(f'[InternetShortcut]\nURL={drawio_url}\n')

# Write HTML launcher
html_page = f"""<!DOCTYPE html>
<html>
<head>
<title>Open Architecture Diagram in Draw.io</title>
<meta http-equiv="refresh" content="1;url={drawio_url}">
<style>
body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; display: flex; align-items: center; justify-content: center; height: 100vh; margin: 0; background: #0f172a; color: #f8fafc; }}
.card {{ background: #1e293b; padding: 40px; border-radius: 12px; border: 1px solid #334155; text-align: center; max-width: 520px; box-shadow: 0 10px 25px rgba(0,0,0,0.5); }}
h1 {{ font-size: 20px; margin-bottom: 12px; color: #38bdf8; }}
p {{ font-size: 14px; color: #94a3b8; line-height: 1.5; margin-bottom: 24px; }}
.btn {{ display: inline-block; background: #2563eb; color: #ffffff; padding: 12px 28px; border-radius: 8px; text-decoration: none; font-weight: 600; font-size: 15px; transition: background 0.2s; }}
.btn:hover {{ background: #1d4ed8; }}
</style>
</head>
<body>
<div class="card">
  <h1>DevOps Incident Watchdog</h1>
  <p>Redirecting you to the 3-Layer 7-Module Architecture Diagram in Draw.io...</p>
  <a class="btn" href="{drawio_url}" target="_blank">Open Diagram in Draw.io</a>
</div>
</body>
</html>"""

with open('OPEN_ARCHITECTURE_IN_DRAWIO.html', 'w', encoding='utf-8') as f:
    f.write(html_page)

brain_dir = 'C:/Users/Sailaja C/.gemini/antigravity/brain/71480885-46c8-4d82-82dc-24b0fd8be342'
if os.path.exists(brain_dir):
    with open(os.path.join(brain_dir, 'OPEN_ARCHITECTURE_IN_DRAWIO.html'), 'w', encoding='utf-8') as f:
        f.write(html_page)
    with open(os.path.join(brain_dir, 'Open_Architecture_In_Drawio.url'), 'w', encoding='utf-8') as f:
        f.write(f'[InternetShortcut]\nURL={drawio_url}\n')

print('SUCCESS: Created Draw.io launcher and direct shortcut!')
