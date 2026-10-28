"""
Comprehensive Application Health & Integrity Verification Script
Student: S Hemal (24MIS0050) | Course: ISWE406 Agile Development Process and DevOps
"""

import filecmp
import sys
import os

base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if base_dir not in sys.path:
    sys.path.insert(0, base_dir)
os.chdir(base_dir)

# 1. Verify template files are 100% identical
t1 = 'templates/index.html'
t2 = 'app/templates/index.html'
are_identical = filecmp.cmp(t1, t2)
print("1. Template Synchronization Check:", "[PASS] Both templates are identical" if are_identical else "[FAIL] Mismatch")
if not are_identical:
    sys.exit(1)

# 2. Test Flask client endpoints
from app.app import app
client = app.test_client()

# Check HTML rendering
res = client.get('/', headers={'Accept': 'text/html'})
assert res.status_code == 200, f"Root returned status {res.status_code}"
html = res.data.decode('utf-8')

# Verify student info & presentation banner
assert '24MIS0050' in html, "Missing student registration number 24MIS0050"
assert 'S Hemal' in html, "Missing student name S Hemal"
assert 'VIT Vellore' in html, "Missing campus name VIT Vellore"
print("2. Viva Presentation & Student Identification:", "[PASS] S Hemal (24MIS0050) verified")

# Verify all 12 items
items = [
    'OnePlus 11R 5G', 'Apple MacBook Air M3', 'Sony WH-1000XM5', 'Apple Watch Series 9',
    'Samsung Galaxy S24 Ultra', 'Apple iPhone 15 Pro', 'Apple AirPods Pro 2',
    'ASUS ROG Zephyrus G14', 'Samsung Galaxy Watch 6 Classic', 'Keychron K2',
    'Marshall Emberton II', 'Anker 737'
]
for item in items:
    assert item in html, f"Missing item in HTML: {item}"
print(f"3. 12-Item Multi-Category Catalog: [PASS] All {len(items)} items rendered in HTML")

# Verify 6 hubs in HTML
hubs = [
    "VIT Vellore (Men's Hostel Q-Block)", "VIT Ladies Hostel (Block L Complex)",
    "Technology Tower (TT Academic Hub)", "Anna Auditorium & Food Court Hub",
    "Katpadi Railway Junction Hub", "Vellore Fort Town (Gandhi Nagar)"
]
for hub in hubs:
    assert hub in html, f"Missing hub in HTML: {hub}"
print(f"4. 6 Campus Fulfillment Dark Store Hubs: [PASS] All {len(hubs)} hubs active")

# Verify tracking modal and partner info
assert 'Ramesh Kumar' in html, "Missing delivery partner Ramesh Kumar"
assert 'TN-23-AB-1024' in html, "Missing vehicle TN-23-AB-1024"
assert '4921' in html, "Missing delivery OTP 4921"
assert 'Live 10-Min Delivery Tracking' in html, "Missing tracking modal title"
print("5. 4-Stage 10-Minute Live Order Tracking: [PASS] Rider details and OTP 4921 verified")

# Verify coupons
assert 'VITFEST50' in html
assert 'FLASHTECH2000' in html
assert 'CAMPUSFREE' in html
print("6. Promotional Voucher Engine: [PASS] VITFEST50, FLASHTECH2000, and CAMPUSFREE active")

# Verify payment methods
assert 'UPI (GPay/PhonePe)' in html
assert 'VIT Smart Card' in html
assert 'Debit/Credit Card' in html
assert 'Cash on Delivery' in html
print("7. Campus Multi-Payment Gateway: [PASS] UPI, VIT RFID Smart Card, Cards, COD verified")

# Verify REST endpoints
res_cat = client.get('/api/products')
assert res_cat.status_code == 200 and len(res_cat.get_json()['products']) == 12
res_hubs = client.get('/api/hubs')
assert res_hubs.status_code == 200 and res_hubs.get_json()['count'] == 6
res_track = client.get('/api/order/track')
assert res_track.status_code == 200 and res_track.get_json()['rider']['name'] == 'Ramesh Kumar'
res_coupon = client.post('/api/coupon', json={'code': 'VITFEST50'})
assert res_coupon.status_code == 200 and res_coupon.get_json()['valid'] is True
print("8. REST API Endpoints: [PASS] /api/products, /api/hubs, /api/coupon, /api/order/track verified")

# Verify Incident Reproduction & Defensive Shield
client.post('/api/devops/reset')
res_crash = client.post('/api/checkout', json={'product_id': 3, 'quantity': 1})
assert res_crash.status_code == 500
assert res_crash.get_json()['type'] == 'ZeroDivisionError'
print("9. SRE Zero-Stock Fault Trigger: [PASS] Authentic ZeroDivisionError (HTTP 500) reproduced")

# Verify DevOps automated fix
client.post('/api/devops/apply-fix')
res_fixed = client.post('/api/checkout', json={'product_id': 3, 'quantity': 1})
assert res_fixed.status_code == 400
assert res_fixed.get_json()['status'] == 'not_deliverable'
print("10. Automated Defensive Fix: [PASS] Clean 400 not_deliverable returned without crash")

# Reset back
client.post('/api/devops/reset')
print("\n=======================================================")
print(">>> ALL APPLICATION SYSTEMS VERIFIED & 100% OPERATIONAL! <<<")
print("=======================================================")
