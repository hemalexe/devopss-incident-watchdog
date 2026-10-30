"""
Generate Formal Academic Walkthrough Presentation (16 Slides, 16:9 HD, Modern Professional Design)
Student: S Hemal (24MIS0050)
Course: ISWE406 Agile Development Process and DevOps
School: School of Computer Science Engineering and Information Systems (SCOPE)
Institution: Vellore Institute of Technology (VIT), Vellore Campus
"""

import os
from PIL import Image
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.enum.shapes import MSO_SHAPE

base_dir = r"C:\Users\Sailaja C\Documents\New folder\DevOps-Incident-Watchdog"
real_dir = os.path.join(base_dir, "real_outputs")
pptx_output = os.path.join(base_dir, "FlashMart_Incident_Watchdog_Application_Guide.pptx")
pdf_output = os.path.join(base_dir, "FlashMart_Incident_Watchdog_Application_Guide_Slides.pdf")

prs = Presentation()
prs.slide_width = Inches(13.333)
prs.slide_height = Inches(7.5)
blank_layout = prs.slide_layouts[6]

# Professional Palette
NAVY = RGBColor(15, 23, 42)         # #0F172A
SLATE = RGBColor(30, 41, 59)        # #1E293B
DARK_BLUE = RGBColor(3, 105, 161)   # #0369A1
BLUE = RGBColor(2, 132, 199)        # #0284C7
CYAN = RGBColor(56, 189, 248)       # #38BDF8
LIGHT_BG = RGBColor(248, 250, 252)  # #F8FAFC
CARD_BG = RGBColor(30, 41, 59)      # #1E293B
WHITE = RGBColor(255, 255, 255)
MUTED = RGBColor(100, 116, 139)     # #64748B
TEXT_DARK = RGBColor(51, 65, 85)    # #334155
RED = RGBColor(239, 68, 68)         # #EF4444
GREEN = RGBColor(34, 197, 94)       # #22C55E
BORDER_COLOR = RGBColor(203, 213, 225) # #CBD5E1

def add_header(slide, title_text, category_text=""):
    """Adds formal, branded academic header banner across top of slide."""
    shape = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), Inches(13.333), Inches(1.15))
    shape.fill.solid()
    shape.fill.fore_color.rgb = NAVY
    shape.line.fill.background()
    
    accent = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(1.15), Inches(13.333), Inches(0.05))
    accent.fill.solid()
    accent.fill.fore_color.rgb = BLUE
    accent.line.fill.background()
    
    txBox = slide.shapes.add_textbox(Inches(0.8), Inches(0.16), Inches(9.5), Inches(0.85))
    tf = txBox.text_frame
    tf.word_wrap = True
    
    if category_text:
        p0 = tf.paragraphs[0]
        p0.text = category_text.upper()
        p0.font.name = "Arial"
        p0.font.size = Pt(9.5)
        p0.font.bold = True
        p0.font.color.rgb = CYAN
        p1 = tf.add_paragraph()
    else:
        p1 = tf.paragraphs[0]
        
    p1.text = title_text
    p1.font.name = "Arial"
    p1.font.size = Pt(19)
    p1.font.bold = True
    p1.font.color.rgb = WHITE
    
    metaBox = slide.shapes.add_textbox(Inches(9.5), Inches(0.18), Inches(3.2), Inches(0.85))
    mtf = metaBox.text_frame
    mtf.word_wrap = True
    mp = mtf.paragraphs[0]
    mp.text = "S Hemal (24MIS0050) | ISWE406\nVIT Vellore Campus (SCOPE)"
    mp.font.name = "Arial"
    mp.font.size = Pt(10)
    mp.font.color.rgb = RGBColor(148, 163, 184)
    mp.alignment = PP_ALIGN.RIGHT

def add_bullet(tf, bold_prefix, text, pt_size=11.5, space_before=7):
    """Adds a structured bold-prefix bullet point."""
    p = tf.add_paragraph()
    p.space_before = Pt(space_before)
    p.line_spacing = 1.15
    
    r_b = p.add_run()
    r_b.text = bold_prefix + " "
    r_b.font.name = "Arial"
    r_b.font.size = Pt(pt_size + 0.5)
    r_b.font.bold = True
    r_b.font.color.rgb = SLATE
    
    r_t = p.add_run()
    r_t.text = text
    r_t.font.name = "Arial"
    r_t.font.size = Pt(pt_size)
    r_t.font.color.rgb = TEXT_DARK

def get_fitted_dimensions(img_path, max_w, max_h):
    """Calculates fitted width and height preserving aspect ratio."""
    with Image.open(img_path) as im:
        orig_w, orig_h = im.size
    aspect = orig_w / float(orig_h)
    
    w = max_w
    h = w / aspect
    if h > max_h:
        h = max_h
        w = h * aspect
    return w, h

def add_image_card(slide, img_path, left, top, max_w, max_h, badge_text=""):
    """Places an image with high-definition frame and optional badge."""
    if not os.path.exists(img_path):
        return
        
    w, h = get_fitted_dimensions(img_path, max_w, max_h)
    
    # Center within given boundaries
    actual_left = left + (max_w - w) / 2
    actual_top = top + (max_h - h) / 2
    
    if badge_text:
        badge = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, actual_left, actual_top - Inches(0.32), w, Inches(0.28))
        badge.fill.solid()
        badge.fill.fore_color.rgb = RGBColor(241, 245, 249)
        badge.line.color.rgb = RGBColor(203, 213, 225)
        badge.line.width = Pt(1)
        btf = badge.text_frame
        btf.word_wrap = True
        bp = btf.paragraphs[0]
        bp.text = badge_text.upper()
        bp.font.name = "Arial"
        bp.font.size = Pt(8.5)
        bp.font.bold = True
        bp.font.color.rgb = RGBColor(30, 41, 59)
        bp.alignment = PP_ALIGN.CENTER
    
    # Outer frame container
    frame = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, actual_left - Inches(0.04), actual_top - Inches(0.04), w + Inches(0.08), h + Inches(0.08))
    frame.fill.solid()
    frame.fill.fore_color.rgb = RGBColor(226, 232, 240)
    frame.line.color.rgb = RGBColor(148, 163, 184)
    frame.line.width = Pt(1.5)
    
    slide.shapes.add_picture(img_path, actual_left, actual_top, w, h)

# ==============================================================================
# SLIDE 1: TITLE SLIDE
# ==============================================================================
slide1 = prs.slides.add_slide(blank_layout)
bg1 = slide1.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), Inches(13.333), Inches(7.5))
bg1.fill.solid()
bg1.fill.fore_color.rgb = NAVY
bg1.line.fill.background()

tx1 = slide1.shapes.add_textbox(Inches(1.2), Inches(1.1), Inches(11.0), Inches(5.6))
tf1 = tx1.text_frame
tf1.word_wrap = True

p_pre = tf1.paragraphs[0]
p_pre.text = "PROJECT APPLICATION & TECHNICAL INCIDENT WALKTHROUGH GUIDE"
p_pre.font.name = "Arial"
p_pre.font.size = Pt(12.5)
p_pre.font.bold = True
p_pre.font.color.rgb = CYAN

p_title = tf1.add_paragraph()
p_title.text = "FlashMart Quick-Commerce &\nAutonomous DevOps Incident Watchdog"
p_title.font.name = "Arial"
p_title.font.size = Pt(32)
p_title.font.bold = True
p_title.font.color.rgb = WHITE
p_title.space_before = Pt(14)

p_sub = tf1.add_paragraph()
p_sub.text = "Autonomous SRE Telemetry Ingestion, Private S3 Cloud Forensics, and Zero-Touch Agile Sprint Backlog Automation"
p_sub.font.name = "Arial"
p_sub.font.size = Pt(15)
p_sub.font.color.rgb = RGBColor(203, 213, 225)
p_sub.space_before = Pt(12)

p_rule = tf1.add_paragraph()
p_rule.text = "―" * 45
p_rule.font.name = "Arial"
p_rule.font.size = Pt(16)
p_rule.font.color.rgb = BLUE
p_rule.space_before = Pt(10)

p_meta = tf1.add_paragraph()
p_meta.text = "Author: S Hemal (Registration No: 24MIS0050)\nCourse: ISWE406 Agile Development Process and DevOps\nSchool: School of Computer Science Engineering and Information Systems (SCOPE)\nInstitution: Vellore Institute of Technology (VIT), Vellore Campus"
p_meta.font.name = "Arial"
p_meta.font.size = Pt(13)
p_meta.font.color.rgb = RGBColor(226, 232, 240)
p_meta.space_before = Pt(14)

# ==============================================================================
# SLIDE 2: PROBLEM STATEMENT & PROJECT SCOPE
# ==============================================================================
slide2 = prs.slides.add_slide(blank_layout)
add_header(slide2, "Executive Problem Statement & Project Scope", "Project Overview")

tx2_l = slide2.shapes.add_textbox(Inches(0.8), Inches(1.45), Inches(5.6), Inches(5.4))
tf2_l = tx2_l.text_frame
tf2_l.word_wrap = True
tf2_l.paragraphs[0].text = "The Modern Microservice Paradox:"
tf2_l.paragraphs[0].font.name = "Arial"
tf2_l.paragraphs[0].font.size = Pt(16)
tf2_l.paragraphs[0].font.bold = True
tf2_l.paragraphs[0].font.color.rgb = RED

add_bullet(tf2_l, "Cloud-Native Scale:", "Modern distributed architectures generate thousands of log events per second, overwhelming human Site Reliability Engineering (SRE) operators.")
add_bullet(tf2_l, "On-Call Fatigue & MTTA Drag:", "Manual incident triage requires engineers to grep CloudWatch logs, reproduce crashes locally, and write bug tickets, driving Mean-Time-to-Acknowledge (MTTA) to 2-8 hours.")
add_bullet(tf2_l, "Ephemeral State Loss:", "Serverless container recycling wipes in-memory crash context before root-cause forensic data can be preserved.")
add_bullet(tf2_l, "Uninsulated User Experience:", "Unhandled runtime 500 exceptions crash browser tabs with blank screens, deteriorating customer trust.")

tx2_r = slide2.shapes.add_textbox(Inches(6.8), Inches(1.45), Inches(5.7), Inches(5.4))
tf2_r = tx2_r.text_frame
tf2_r.word_wrap = True
tf2_r.paragraphs[0].text = "Autonomous DevOps Watchdog Solution:"
tf2_r.paragraphs[0].font.name = "Arial"
tf2_r.paragraphs[0].font.size = Pt(16)
tf2_r.paragraphs[0].font.bold = True
tf2_r.paragraphs[0].font.color.rgb = GREEN

add_bullet(tf2_r, "Zero-Human Telemetry Routing:", "Real-time AWS CloudWatch Metric Filters detect critical runtime exceptions asynchronously in under 4.2 seconds.")
add_bullet(tf2_r, "Immutable Cloud Forensics:", "Mints cryptographic JSON dumps uploaded directly to private Amazon S3 with 11 9's durability and AES-256 encryption.")
add_bullet(tf2_r, "Zero-Touch Sprint Integration:", "Dispatches authenticated GitHub REST API calls to mint structured Bug User Stories with 6 Definition of Done criteria.")
add_bullet(tf2_r, "Defensive Client Shielding:", "SPA client intercepts HTTP 500 errors gracefully, displaying an informative stockout waitlist modal to insulate users.")

# ==============================================================================
# SLIDE 3: SYSTEM ARCHITECTURE
# ==============================================================================
slide3 = prs.slides.add_slide(blank_layout)
add_header(slide3, "Decoupled Three-Tier System Architecture & Boundary Separation", "System Architecture")

tx3 = slide3.shapes.add_textbox(Inches(0.8), Inches(1.4), Inches(4.8), Inches(5.5))
tf3 = tx3.text_frame
tf3.word_wrap = True
tf3.paragraphs[0].text = "Three-Tier Decoupled Pipeline:"
tf3.paragraphs[0].font.name = "Arial"
tf3.paragraphs[0].font.size = Pt(15)
tf3.paragraphs[0].font.bold = True
tf3.paragraphs[0].font.color.rgb = BLUE

add_bullet(tf3, "Tier 1 (Client Presentation):", "FlashMart Tech storefront with geofenced dark store selector, dynamic cart drawer, and defensive HTTP 500 interception shield.")
add_bullet(tf3, "Tier 2 (Compute & Execution):", "Decoupled AWS Lambda microservices (target app & watchdog incident creator) running in isolated serverless sandboxes.")
add_bullet(tf3, "Tier 3 (Cloud Services & Agile Backlog):", "AWS CloudWatch Metric Filters, Amazon S3 forensic vault (401537512022), and GitHub Issues Agile backlog.")
add_bullet(tf3, "Architectural Invariant:", "Total blast radius isolation: crashes in target application logic cannot degrade or block the watchdog telemetry pipeline.")

add_image_card(slide3, os.path.join(base_dir, "architecture_diagram.png"), Inches(5.8), Inches(1.45), Inches(6.8), Inches(5.4), "Figure 1: Decoupled Three-Tier System Topology")

# ==============================================================================
# SLIDE 4: MODULE 1A - STOREFRONT CATALOG & DARK STORES
# ==============================================================================
slide4 = prs.slides.add_slide(blank_layout)
add_header(slide4, "Module 1A: Storefront Catalog, Search & Campus Dark Stores", "Storefront Presentation")

tx4 = slide4.shapes.add_textbox(Inches(0.8), Inches(1.4), Inches(4.8), Inches(5.5))
tf4 = tx4.text_frame
tf4.word_wrap = True
tf4.paragraphs[0].text = "Catalog & Routing Architecture:"
tf4.paragraphs[0].font.name = "Arial"
tf4.paragraphs[0].font.size = Pt(15)
tf4.paragraphs[0].font.bold = True
tf4.paragraphs[0].font.color.rgb = BLUE

add_bullet(tf4, "12-Item Multi-Category Catalog:", "Covers Smartphones, Laptops, Audio, Wearables, Gaming, and Power Essentials with live stock numbers and zero framework bloat.")
add_bullet(tf4, "Dynamic Search & Category Chips:", "Client-side category filtering (⚡ Flash Deals, 💻 Laptops, 🎧 Audio, etc.) and instant real-time DOM query search matching.")
add_bullet(tf4, "6 Geofenced Dark Store Nodes:", "Simulates dynamic micro-fulfillment routing across VIT Vellore Hostels (Men's Q-Block, Ladies L-Block), Tech Tower, and Anna Auditorium.")
add_bullet(tf4, "Active Student Session Banner:", "Verified student header: S Hemal (24MIS0050) | ISWE406 Agile & DevOps | VIT Vellore Campus (SCOPE).")

add_image_card(slide4, os.path.join(real_dir, "real_storefront_catalog.png"), Inches(5.8), Inches(1.75), Inches(6.8), Inches(5.1), "Authentic Live System Capture: Storefront Browser View (Port 5000)")

# ==============================================================================
# SLIDE 5: MODULE 1B - INTERACTIVE CART & CAMPUS PAYMENTS
# ==============================================================================
slide5 = prs.slides.add_slide(blank_layout)
add_header(slide5, "Module 1B: Interactive Cart Drawer & Campus Payment Gateways", "Checkout Engine")

tx5 = slide5.shapes.add_textbox(Inches(0.8), Inches(1.4), Inches(4.8), Inches(5.5))
tf5 = tx5.text_frame
tf5.word_wrap = True
tf5.paragraphs[0].text = "Cart & Transaction Management:"
tf5.paragraphs[0].font.name = "Arial"
tf5.paragraphs[0].font.size = Pt(15)
tf5.paragraphs[0].font.bold = True
tf5.paragraphs[0].font.color.rgb = BLUE

add_bullet(tf5, "Persistent Sliding Cart Drawer:", "Dynamic quantity increment/decrement, live subtotal computation, zero packaging fee logic, and full drawer overlay.")
add_bullet(tf5, "Campus Promotional Coupon Engine:", "REST endpoint validates student coupon VITFEST50 (10% student festival discount: -₹3,500 applied) with real-time bill deduction.")
add_bullet(tf5, "4 Campus Payment Gateways:", "Supports Instant UPI (GPay/PhonePe), VIT Student RFID Smart Card tap-and-pay, Debit/Credit Card, and Cash on Delivery.")
add_bullet(tf5, "Client-Side Order Validation:", "Secures itemized billing details before transmitting JSON checkout payload to backend worker endpoint.")

add_image_card(slide5, os.path.join(real_dir, "real_cart_checkout_modal.png"), Inches(5.8), Inches(1.75), Inches(6.8), Inches(5.1), "Authentic Live System Capture: Cart Drawer & Applied VITFEST50 Coupon")

# ==============================================================================
# SLIDE 6: MODULE 1C - 10-MIN MICRO-FULFILLMENT & LIVE TRACKING
# ==============================================================================
slide6 = prs.slides.add_slide(blank_layout)
add_header(slide6, "Module 1C: Sub-10-Minute Micro-Fulfillment & Live Order Tracking", "Delivery Lifecycle")

tx6 = slide6.shapes.add_textbox(Inches(0.8), Inches(1.4), Inches(4.8), Inches(5.5))
tf6 = tx6.text_frame
tf6.word_wrap = True
tf6.paragraphs[0].text = "Micro-Fulfillment & Driver Telemetry:"
tf6.paragraphs[0].font.name = "Arial"
tf6.paragraphs[0].font.size = Pt(15)
tf6.paragraphs[0].font.bold = True
tf6.paragraphs[0].font.color.rgb = BLUE

add_bullet(tf6, "4-Stage Visual Progress Stepper:", "Tracks order lifecycle: Order Placed -> Packed at Dark Store -> Out for Delivery (Active) -> Delivered.")
add_bullet(tf6, "Live Countdown Timer:", "Active countdown clock simulating hyper-local delivery arriving in 05:42 minutes to student residence.")
add_bullet(tf6, "Assigned Courier Profile:", "Features verified delivery partner Ramesh Kumar (⚡ Fast Express Courier, 4.9★ rating) on Electric Scooter TN-23-AB-1024.")
add_bullet(tf6, "Secure Handover OTP:", "Generates 4-digit verification code (OTP: 4921) ensuring zero-tamper physical delivery at Men's Hostel Q-Block.")

add_image_card(slide6, os.path.join(real_dir, "real_live_tracking_modal.png"), Inches(5.8), Inches(1.75), Inches(6.8), Inches(5.1), "Authentic Live System Capture: 10-Min Live Tracking, Courier & OTP")

# ==============================================================================
# SLIDE 7: MODULE 3 - RUNTIME ZERO DIVISION ERROR CRASH
# ==============================================================================
slide7 = prs.slides.add_slide(blank_layout)
add_header(slide7, "Module 3: Dark Store Stockout Edge-Case & Runtime Server Crash", "Incident Reproduction")

tx7 = slide7.shapes.add_textbox(Inches(0.8), Inches(1.4), Inches(4.8), Inches(5.5))
tf7 = tx7.text_frame
tf7.word_wrap = True
tf7.paragraphs[0].text = "Runtime Microservice Failure:"
tf7.paragraphs[0].font.name = "Arial"
tf7.paragraphs[0].font.size = Pt(15)
tf7.paragraphs[0].font.bold = True
tf7.paragraphs[0].font.color.rgb = RED

add_bullet(tf7, "The Stockout Edge-Case Condition:", "During flash sales, local dark store inventory hits stock = 0. The checkout inventory allocation formula executes: allocation = 100 / stock_count.")
add_bullet(tf7, "Unhandled Python Runtime Exception:", "Raises fatal ZeroDivisionError: division by zero in app.py at line 142, crashing the worker thread and emitting HTTP 500.")
add_bullet(tf7, "Structured Telemetry Emission:", "Logger immediately intercepts stack trace and emits structured JSON stdout: [CRITICAL_ALERT] INCIDENT_DETECTED.")
add_bullet(tf7, "Forensic Metadata Captured:", "Includes incident ID INC-1791945923-07CD12B5, ISO 8601 timestamp, target service, error type, and complete traceback.")

add_image_card(slide7, os.path.join(real_dir, "real_terminal_crash.png"), Inches(5.8), Inches(1.75), Inches(6.8), Inches(5.1), "Authentic PowerShell Server Terminal: ZeroDivisionError & Critical Alert")

# ==============================================================================
# SLIDE 8: MODULE 2 - CLIENT EXCEPTION SHIELD & CUSTOMER INSULATION
# ==============================================================================
slide8 = prs.slides.add_slide(blank_layout)
add_header(slide8, "Module 2: Client Exception Interception & Customer Insulation", "Customer Insulation")

tx8 = slide8.shapes.add_textbox(Inches(0.8), Inches(1.4), Inches(4.8), Inches(5.5))
tf8 = tx8.text_frame
tf8.word_wrap = True
tf8.paragraphs[0].text = "Defensive Client Safeguards:"
tf8.paragraphs[0].font.name = "Arial"
tf8.paragraphs[0].font.size = Pt(15)
tf8.paragraphs[0].font.bold = True
tf8.paragraphs[0].font.color.rgb = GREEN

add_bullet(tf8, "Client HTTP 500 Interception:", "SPA frontend catches server 500 Internal Server Error asynchronously, completely preventing browser white-screen crashes.")
add_bullet(tf8, "Polite Waitlist Modal:", "Renders 'Item Not Deliverable to Your Location' drawer explaining stock exhaustion at Men's Hostel Dark Store (VIT Vellore).")
add_bullet(tf8, "Customer Trust & Retention:", "Offers a 'Notify Me When Available' waitlist subscription button and alternative dark store pickup selection, preserving brand reputation.")
add_bullet(tf8, "Seamless User Experience:", "Shields end users from raw infrastructure failures while background SRE automation handles the incident.")

add_image_card(slide8, os.path.join(real_dir, "real_stockout_waitlist_drawer.png"), Inches(5.8), Inches(1.75), Inches(6.8), Inches(5.1), "Authentic Live System Capture: Graceful Stockout Waitlist Customer Shield")

# ==============================================================================
# SLIDE 9: MODULE 4 - CLOUDWATCH METRIC INGESTION & SRE CONSOLE
# ==============================================================================
slide9 = prs.slides.add_slide(blank_layout)
add_header(slide9, "Module 4: AWS CloudWatch Metric Ingestion & SRE Backstage Console", "SRE Observability")

tx9 = slide9.shapes.add_textbox(Inches(0.8), Inches(1.4), Inches(4.8), Inches(5.5))
tf9 = tx9.text_frame
tf9.word_wrap = True
tf9.paragraphs[0].text = "Sub-5-Second Incident Ingestion:"
tf9.paragraphs[0].font.name = "Arial"
tf9.paragraphs[0].font.size = Pt(15)
tf9.paragraphs[0].font.bold = True
tf9.paragraphs[0].font.color.rgb = BLUE

add_bullet(tf9, "Non-Invasive Metric Filter Pattern:", "CloudWatch Metric Filter continuously monitors log group /aws/lambda/watchdog-target-app matching pattern [CRITICAL_ALERT].")
add_bullet(tf9, "Zero Polling Latency:", "Fires CloudWatch alarm state asynchronously and dispatches execution event to Watchdog Lambda within 4.2 seconds.")
add_bullet(tf9, "Dedicated SRE Backstage Console:", "Web-based operator dashboard (/?view=devops) surfaces live incident metrics, CloudWatch alarm status, and Agile backlog sync.")
add_bullet(tf9, "Mean Time to Acknowledge (MTTA):", "Reduces incident discovery latency from 2-8 hours of manual log grepping down to < 24 seconds.")

add_image_card(slide9, os.path.join(real_dir, "real_sre_backstage_dashboard.png"), Inches(5.8), Inches(1.75), Inches(6.8), Inches(5.1), "Authentic Live System Capture: SRE Backstage Dashboard & Telemetry Stream")

# ==============================================================================
# SLIDE 10: MODULE 5 - IMMUTABLE CLOUD FORENSICS IN S3 (DUAL SCREENSHOTS)
# ==============================================================================
slide10 = prs.slides.add_slide(blank_layout)
add_header(slide10, "Module 5: Cryptographic Forensic Archival in Amazon S3 Console", "Forensic Compliance")

tx10 = slide10.shapes.add_textbox(Inches(0.8), Inches(1.4), Inches(4.8), Inches(5.5))
tf10 = tx10.text_frame
tf10.word_wrap = True
tf10.paragraphs[0].text = "Tamper-Proof Audit Compliance:"
tf10.paragraphs[0].font.name = "Arial"
tf10.paragraphs[0].font.size = Pt(15)
tf10.paragraphs[0].font.bold = True
tf10.paragraphs[0].font.color.rgb = BLUE

add_bullet(tf10, "Comprehensive Forensic JSON Schema:", "Captures uncompressed traceback, git commit SHA, HTTP headers, dark store hub node, environment, and UTC timestamp.")
add_bullet(tf10, "11 9's Durability Guarantee:", "Stored in private S3 bucket devops-incident-watchdog-logs-401537512022 with Block Public Access and AES-256 encryption.")
add_bullet(tf10, "Cryptographic INC-ID Naming:", "Mints immutable key: incidents/2026-10-14/INC-1791945923-07CD12B5.json for tamper-proof audit trails.")

# Top Image: S3 Bucket View
add_image_card(slide10, os.path.join(real_dir, "real_aws_s3_bucket_incidents.png"), Inches(5.8), Inches(1.68), Inches(6.8), Inches(2.45), "Real Amazon S3 Console: Target Bucket & Incident Folders View")

# Bottom Image: S3 Dump Object View
add_image_card(slide10, os.path.join(real_dir, "real_aws_s3_incident_dump.png"), Inches(5.8), Inches(4.55), Inches(6.8), Inches(2.45), "Real Amazon S3 Console: Incident Forensic Dump Object Properties")

# ==============================================================================
# SLIDE 11: MODULE 6 - AUTONOMOUS BUG STORY MINTING ON GITHUB
# ==============================================================================
slide11 = prs.slides.add_slide(blank_layout)
add_header(slide11, "Module 6: Autonomous Bug Story Minting on GitHub Issues", "Agile Backlog Integration")

tx11 = slide11.shapes.add_textbox(Inches(0.8), Inches(1.4), Inches(4.8), Inches(5.5))
tf11 = tx11.text_frame
tf11.word_wrap = True
tf11.paragraphs[0].text = "Zero-Touch Sprint Integration:"
tf11.paragraphs[0].font.name = "Arial"
tf11.paragraphs[0].font.size = Pt(15)
tf11.paragraphs[0].font.bold = True
tf11.paragraphs[0].font.color.rgb = BLUE

add_bullet(tf11, "GitHub REST API v3 Integration:", "Watchdog Lambda dispatches authenticated HTTP POST call to mint structured Bug User Story within 24 seconds of crash.")
add_bullet(tf11, "Standardized Agile Bug Story:", "Formatted as: 'As an SRE on-call engineer, I need the checkout allocation microservice to handle stock = 0 without throwing ZeroDivisionError...'.")
add_bullet(tf11, "Automated Diagnostics Table:", "Embeds incident ID, error type, target microservice, VIT campus hub, and direct S3 forensic URI link.")
add_bullet(tf11, "6 Definition of Done (DoD) Criteria:", "Includes explicit acceptance checkboxes for code guard, customer insulation, and pytest CI regression verification.")

add_image_card(slide11, os.path.join(real_dir, "real_github_issue.png"), Inches(5.8), Inches(1.75), Inches(6.8), Inches(5.1), "Authentic GitHub Issues Capture: Issue #1 with Diagnostics & 6 DoD Criteria")

# ==============================================================================
# SLIDE 12: MODULE 7 - CI/CD PIPELINE & SMART COMMIT CLOSURE (DUAL)
# ==============================================================================
slide12 = prs.slides.add_slide(blank_layout)
add_header(slide12, "Module 7: GitHub Actions CI/CD & Smart Commit Automated Closure", "Continuous Remediation")

tx12 = slide12.shapes.add_textbox(Inches(0.8), Inches(1.4), Inches(4.8), Inches(5.5))
tf12 = tx12.text_frame
tf12.word_wrap = True
tf12.paragraphs[0].text = "GitOps Automated Lifecycle:"
tf12.paragraphs[0].font.name = "Arial"
tf12.paragraphs[0].font.size = Pt(15)
tf12.paragraphs[0].font.bold = True
tf12.paragraphs[0].font.color.rgb = GREEN

add_bullet(tf12, "GitOps Smart Commit Syntax:", "Developer commits code fix referencing issue ID: git commit -am 'Fixes #1: Handled division by zero in checkout logic'.")
add_bullet(tf12, "GitHub Actions CI Runner:", "Triggers automated CI regression suite on push, verifying all test suites on Ubuntu runner.")
add_bullet(tf12, "Green Checkmark Build Status:", "GitHub repository confirms passing build with green checkmark next to the commit SHA in main branch.")
add_bullet(tf12, "Zero-Touch Issue Transition:", "Merging to main automatically transitions GitHub Issue #1 to Closed (Done), updating sprint burn-down without human overhead.")

# Top Image: GitHub Repo CI Pass
add_image_card(slide12, os.path.join(real_dir, "real_github_repo_ci_pass.png"), Inches(5.8), Inches(1.68), Inches(6.8), Inches(2.45), "Authentic GitHub Repo: Commit with Green Checkmark CI/CD Build Pass")

# Bottom Image: Terminal GitOps
add_image_card(slide12, os.path.join(real_dir, "real_terminal_gitops.png"), Inches(5.8), Inches(4.55), Inches(6.8), Inches(2.45), "Authentic PowerShell Terminal: GitOps Smart Commit & Branch Tracking")

# ==============================================================================
# SLIDE 13: MODULE 8 - AUTOMATED PYTEST REGRESSION (17/17 PASSED)
# ==============================================================================
slide13 = prs.slides.add_slide(blank_layout)
add_header(slide13, "Module 8: Automated Pytest Regression Verification (17/17 Passed)", "Quality Assurance")

tx13 = slide13.shapes.add_textbox(Inches(0.8), Inches(1.4), Inches(4.8), Inches(5.5))
tf13 = tx13.text_frame
tf13.word_wrap = True
tf13.paragraphs[0].text = "100% Automated Test Pass Rate:"
tf13.paragraphs[0].font.name = "Arial"
tf13.paragraphs[0].font.size = Pt(15)
tf13.paragraphs[0].font.bold = True
tf13.paragraphs[0].font.color.rgb = GREEN

add_bullet(tf13, "Comprehensive Test Harness (tests/test_app.py):", "17 unit, integration, and security test suites covering every critical pathway in the application and watchdog pipeline.")
add_bullet(tf13, "ZeroDivision Guard Verification:", "Verifies that stock = 0 triggers stockout handling without raising unhandled runtime server exceptions.")
add_bullet(tf13, "Campus Feature Verification:", "Tests coupon validation (VITFEST50), 10-min live order tracking endpoint, 6 dark store inventory allocations, and cart calculations.")
add_bullet(tf13, "Execution Performance:", "Executes all 17 tests in 1.14 seconds with 100% test pass rate and zero regression failures.")

add_image_card(slide13, os.path.join(real_dir, "real_terminal_pytest.png"), Inches(5.8), Inches(1.75), Inches(6.8), Inches(5.1), "Authentic PowerShell Terminal: Pytest 17/17 Tests Passing (100% Pass Rate)")

# ==============================================================================
# SLIDE 14: AWS SERVERLESS TOPOLOGY & CONSOLE HOME (DUAL)
# ==============================================================================
slide14 = prs.slides.add_slide(blank_layout)
add_header(slide14, "AWS Serverless Production Deployment & Cost Breakdown", "Cloud Infrastructure")

tx14 = slide14.shapes.add_textbox(Inches(0.8), Inches(1.4), Inches(4.8), Inches(5.5))
tf14 = tx14.text_frame
tf14.word_wrap = True
tf14.paragraphs[0].text = "Production Cloud Parameters:"
tf14.paragraphs[0].font.name = "Arial"
tf14.paragraphs[0].font.size = Pt(15)
tf14.paragraphs[0].font.bold = True
tf14.paragraphs[0].font.color.rgb = BLUE

add_bullet(tf14, "AWS Region & Account:", "Deployed serverless in Sydney (ap-southeast-2) region under verified AWS Account 401537512022.")
add_bullet(tf14, "Microservice Compute Sizing:", "Both target app and incident creator configured with 128 MB RAM (sub-300ms cold start latency).")
add_bullet(tf14, "100% Free Tier Eligible ($0.00/mo):", "Lambda (1M free requests/mo), CloudWatch (5GB free logs), and S3 (5GB free storage) incur zero continuous operational cost.")

# Top Image: AWS Console Home
add_image_card(slide14, os.path.join(real_dir, "real_aws_console_home.png"), Inches(5.8), Inches(1.68), Inches(6.8), Inches(2.45), "Real AWS Management Console Home: Active Account & Sydney Region")

# Bottom Image: AWS Topology
add_image_card(slide14, os.path.join(base_dir, "figure4_aws_topology.png"), Inches(5.8), Inches(4.55), Inches(6.8), Inches(2.45), "AWS Serverless Microservice Topology & Security Boundaries")

# ==============================================================================
# SLIDE 15: 7-STAGE END-TO-END WORKFLOW
# ==============================================================================
slide15 = prs.slides.add_slide(blank_layout)
add_header(slide15, "Summary of the 7-Stage End-to-End Incident Lifecycle", "Workflow Lifecycle")

tx15 = slide15.shapes.add_textbox(Inches(0.8), Inches(1.35), Inches(11.733), Inches(0.55))
tf15 = tx15.text_frame
tf15.word_wrap = True
p15 = tf15.paragraphs[0]
p15.text = "From unhandled runtime microservice crash to zero-touch sprint closure across 7 automated stages in < 24 seconds:"
p15.font.name = "Arial"
p15.font.size = Pt(13.5)
p15.font.color.rgb = SLATE

add_image_card(slide15, os.path.join(base_dir, "figure2_workflow.png"), Inches(0.8), Inches(1.95), Inches(11.733), Inches(4.3), "Figure 2: 7-Stage Autonomous Incident Ingestion & Sprint Remediation Lifecycle")

tx15_b = slide15.shapes.add_textbox(Inches(0.8), Inches(6.4), Inches(11.733), Inches(0.75))
tf15_b = tx15_b.text_frame
tf15_b.word_wrap = True
p15_b = tf15_b.paragraphs[0]
p15_b.text = "Stages 1-2 (Detection & Customer Insulation) -> Stages 3-4 (CloudWatch Ingestion & S3 Forensics) -> Stages 5-7 (Agile Backlog Minting, GitOps Code Fix, Automated Pytest CI/CD Closure)."
p15_b.font.name = "Arial"
p15_b.font.size = Pt(11.5)
p15_b.font.bold = True
p15_b.font.color.rgb = BLUE

# ==============================================================================
# SLIDE 16: CONCLUSION & VERIFIED METRICS
# ==============================================================================
slide16 = prs.slides.add_slide(blank_layout)
bg16 = slide16.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), Inches(13.333), Inches(7.5))
bg16.fill.solid()
bg16.fill.fore_color.rgb = NAVY
bg16.line.fill.background()

tx_c = slide16.shapes.add_textbox(Inches(1.0), Inches(0.7), Inches(11.333), Inches(6.1))
tf_c = tx_c.text_frame
tf_c.word_wrap = True

p_c_head = tf_c.paragraphs[0]
p_c_head.text = "VERIFIED PROJECT OUTCOMES & CONCLUSION"
p_c_head.font.name = "Arial"
p_c_head.font.size = Pt(24)
p_c_head.font.bold = True
p_c_head.font.color.rgb = CYAN

p_c_desc = tf_c.add_paragraph()
p_c_desc.text = "DevOps Incident Watchdog establishes a fully autonomous, closed-loop Site Reliability Engineering feedback bridge for cloud-native microservices:"
p_c_desc.font.name = "Arial"
p_c_desc.font.size = Pt(14)
p_c_desc.font.color.rgb = RGBColor(226, 232, 240)
p_c_desc.space_before = Pt(8)

def add_stat_box(slide, left, top, num_text, label_text, color_rgb):
    box = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, left, top, Inches(2.6), Inches(1.6))
    box.fill.solid()
    box.fill.fore_color.rgb = CARD_BG
    box.line.color.rgb = color_rgb
    box.line.width = Pt(2)
    tf_b = box.text_frame
    tf_b.word_wrap = True
    p1 = tf_b.paragraphs[0]
    p1.text = num_text
    p1.font.name = "Arial"
    p1.font.size = Pt(28)
    p1.font.bold = True
    p1.font.color.rgb = color_rgb
    p1.alignment = PP_ALIGN.CENTER
    p2 = tf_b.add_paragraph()
    p2.text = label_text
    p2.font.name = "Arial"
    p2.font.size = Pt(10.5)
    p2.font.color.rgb = RGBColor(203, 213, 225)
    p2.alignment = PP_ALIGN.CENTER

add_stat_box(slide16, Inches(1.0), Inches(2.35), "< 24s", "Mean Time to Acknowledge\n(Manual MTTA: 2-8 hrs)", CYAN)
add_stat_box(slide16, Inches(3.9), Inches(2.35), "1.14s", "Pytest Suite Execution\n(17/17 Tests Passing 100%)", RGBColor(74, 222, 128))
add_stat_box(slide16, Inches(6.8), Inches(2.35), "11 9's", "S3 Durability SLA\n(Immutable Forensics)", RGBColor(250, 204, 21))
add_stat_box(slide16, Inches(9.7), Inches(2.35), "$0.00", "Monthly Infrastructure\n(100% Free Tier)", RGBColor(168, 85, 247))

tx_end = slide16.shapes.add_textbox(Inches(1.0), Inches(4.35), Inches(11.333), Inches(2.5))
tf_e = tx_end.text_frame
tf_e.word_wrap = True

p_e1 = tf_e.paragraphs[0]
p_e1.text = "Key Takeaway for Faculty Evaluation:"
p_e1.font.name = "Arial"
p_e1.font.size = Pt(15)
p_e1.font.bold = True
p_e1.font.color.rgb = WHITE

p_e2 = tf_e.add_paragraph()
p_e2.text = "By shifting incident triage from manual, error-prone on-call rotations to software-defined, event-driven automation, the project demonstrates that Agile velocity and Site Reliability Engineering operate in complete harmony."
p_e2.font.name = "Arial"
p_e2.font.size = Pt(13)
p_e2.font.color.rgb = RGBColor(203, 213, 225)
p_e2.space_before = Pt(6)

p_thank = tf_e.add_paragraph()
p_thank.text = "Thank You! Open for Faculty Demonstration & Technical Q&A."
p_thank.font.name = "Arial"
p_thank.font.size = Pt(16)
p_thank.font.bold = True
p_thank.font.color.rgb = CYAN
p_thank.space_before = Pt(12)

p_author = tf_e.add_paragraph()
p_author.text = "S Hemal (24MIS0050) | ISWE406 Agile Development Process and DevOps | VIT Vellore Campus (SCOPE)"
p_author.font.name = "Arial"
p_author.font.size = Pt(11)
p_author.font.color.rgb = RGBColor(148, 163, 184)
p_author.space_before = Pt(4)

# Save Presentation
prs.save(pptx_output)
print(f"SUCCESS: Academic Presentation saved to: {pptx_output}")

# Convert PPTX to PDF via PowerPoint COM
import win32com.client
try:
    ppt_app = win32com.client.Dispatch("PowerPoint.Application")
    ppt_pres = ppt_app.Presentations.Open(pptx_output, WithWindow=False)
    ppt_pres.SaveAs(pdf_output, 32) # 32 = ppSaveAsPDF
    ppt_pres.Close()
    ppt_app.Quit()
    print(f"SUCCESS: Presentation PDF saved to: {pdf_output}")
except Exception as e:
    print(f"WARNING: PowerPoint PDF export exception: {e}")
