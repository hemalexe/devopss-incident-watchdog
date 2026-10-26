"""
Generate High-Quality Academic Presentation (.pptx)
Title: FlashMart Quick-Commerce & Autonomous DevOps Incident Watchdog
Student: S Hemal (24MIS0050)
Course: ISWE406 Agile Development Process and DevOps
Institution: SCOPE, VIT Vellore Campus
"""

import os
import pptx
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.enum.shapes import MSO_SHAPE

base_dir = r"C:\Users\Sailaja C\Documents\New folder\DevOps-Incident-Watchdog"
pptx_output = os.path.join(base_dir, "FlashMart_Incident_Watchdog_Application_Guide.pptx")
pdf_output = os.path.join(base_dir, "FlashMart_Incident_Watchdog_Application_Guide_Slides.pdf")

prs = Presentation()
prs.slide_width = Inches(13.333)
prs.slide_height = Inches(7.5)

blank_layout = prs.slide_layouts[6]

# Theme Colors
NAVY = RGBColor(15, 23, 42)        # #0F172A
SLATE = RGBColor(30, 41, 59)       # #1E293B
MUTED = RGBColor(100, 116, 139)    # #64748B
BLUE = RGBColor(2, 132, 199)       # #0284C7
LIGHT_BG = RGBColor(248, 250, 252) # #F8FAFC
WHITE = RGBColor(255, 255, 255)
GREEN = RGBColor(22, 163, 74)
RED = RGBColor(220, 38, 38)

def add_header(slide, title_text, category_text=""):
    # Header background strip
    shape = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), Inches(13.333), Inches(1.15))
    shape.fill.solid()
    shape.fill.fore_color.rgb = SLATE
    shape.line.fill.background()
    
    # Category tag
    if category_text:
        tx_cat = slide.shapes.add_textbox(Inches(0.8), Inches(0.12), Inches(11.5), Inches(0.3))
        tf_c = tx_cat.text_frame
        tf_c.word_wrap = True
        p_c = tf_c.paragraphs[0]
        p_c.text = category_text.upper()
        p_c.font.name = "Arial"
        p_c.font.size = Pt(10)
        p_c.font.bold = True
        p_c.font.color.rgb = RGBColor(56, 189, 248)
        
    # Title text
    tx_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.38), Inches(11.5), Inches(0.65))
    tf = tx_box.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = title_text
    p.font.name = "Arial"
    p.font.size = Pt(22)
    p.font.bold = True
    p.font.color.rgb = WHITE
    
    # Footer strip
    tx_foot = slide.shapes.add_textbox(Inches(0.8), Inches(7.1), Inches(11.7), Inches(0.3))
    tf_f = tx_foot.text_frame
    p_f = tf_f.paragraphs[0]
    p_f.text = "FlashMart & DevOps Incident Watchdog | Student: S Hemal (24MIS0050) | ISWE406 | VIT Vellore"
    p_f.font.name = "Arial"
    p_f.font.size = Pt(9.5)
    p_f.font.color.rgb = MUTED

def add_bullet(tf, bold_prefix, text):
    p = tf.add_paragraph()
    p.space_before = Pt(10)
    p.space_after = Pt(4)
    p.level = 0
    
    r1 = p.add_run()
    r1.text = bold_prefix + " "
    r1.font.name = "Arial"
    r1.font.size = Pt(14)
    r1.font.bold = True
    r1.font.color.rgb = NAVY
    
    r2 = p.add_run()
    r2.text = text
    r2.font.name = "Arial"
    r2.font.size = Pt(13)
    r2.font.color.rgb = SLATE

# ==============================================================================
# SLIDE 1: FORMAL TITLE SLIDE
# ==============================================================================
slide1 = prs.slides.add_slide(blank_layout)
bg1 = slide1.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), Inches(13.333), Inches(7.5))
bg1.fill.solid()
bg1.fill.fore_color.rgb = NAVY
bg1.line.fill.background()

# Title text frame
tx_t = slide1.shapes.add_textbox(Inches(1.0), Inches(1.2), Inches(11.333), Inches(2.2))
tf = tx_t.text_frame
tf.word_wrap = True

p_pre = tf.paragraphs[0]
p_pre.text = "TECHNICAL PROJECT PRESENTATION & APPLICATION WALKTHROUGH"
p_pre.font.name = "Arial"
p_pre.font.size = Pt(12)
p_pre.font.bold = True
p_pre.font.color.rgb = RGBColor(56, 189, 248)

p_title = tf.add_paragraph()
p_title.text = "DevOps Incident Watchdog:\nAutonomous SRE Telemetry & Closed-Loop Sprint Backlog Automation"
p_title.font.name = "Arial"
p_title.font.size = Pt(30)
p_title.font.bold = True
p_title.font.color.rgb = WHITE
p_title.space_before = Pt(12)

p_sub = tf.add_paragraph()
p_sub.text = "Monitored Microservice: FlashMart Tech (10-Minute E-Commerce at VIT Vellore Hub)"
p_sub.font.name = "Arial"
p_sub.font.size = Pt(16)
p_sub.font.color.rgb = RGBColor(148, 163, 184)
p_sub.space_before = Pt(10)

# Author card
tx_a = slide1.shapes.add_textbox(Inches(1.0), Inches(4.5), Inches(11.333), Inches(2.2))
tf_a = tx_a.text_frame
tf_a.word_wrap = True

p_by = tf_a.paragraphs[0]
p_by.text = "Submitted by:"
p_by.font.name = "Arial"
p_by.font.size = Pt(13)
p_by.font.color.rgb = RGBColor(148, 163, 184)

p_auth = tf_a.add_paragraph()
p_auth.text = "S Hemal (Registration No: 24MIS0050)"
p_auth.font.name = "Arial"
p_auth.font.size = Pt(20)
p_auth.font.bold = True
p_auth.font.color.rgb = WHITE

p_course = tf_a.add_paragraph()
p_course.text = "Course: ISWE406 Agile Development Process and DevOps"
p_course.font.name = "Arial"
p_course.font.size = Pt(14)
p_course.font.color.rgb = RGBColor(56, 189, 248)

p_inst = tf_a.add_paragraph()
p_inst.text = "School of Computer Science Engineering and Information Systems (SCOPE)\nVellore Institute of Technology, Vellore Campus | Academic Year 2026-2027"
p_inst.font.name = "Arial"
p_inst.font.size = Pt(13)
p_inst.font.color.rgb = RGBColor(148, 163, 184)
p_inst.space_before = Pt(6)

# ==============================================================================
# SLIDE 2: THE EXECUTIVE OVERVIEW
# ==============================================================================
slide2 = prs.slides.add_slide(blank_layout)
add_header(slide2, "Executive Problem Statement & Project Scope", "Project Overview")

tx = slide2.shapes.add_textbox(Inches(0.8), Inches(1.5), Inches(11.7), Inches(5.3))
tf = tx.text_frame
tf.word_wrap = True
tf.paragraphs[0].text = "Why Traditional DevOps Fails During Promotional Flash Spikes:"
tf.paragraphs[0].font.name = "Arial"
tf.paragraphs[0].font.size = Pt(16)
tf.paragraphs[0].font.bold = True
tf.paragraphs[0].font.color.rgb = BLUE

add_bullet(tf, "1. Extreme Concurrency & Dark Store Exhaustion:", "In quick-commerce platforms (FlashMart, Zepto, Blinkit), promotional flash sales generate sudden 50x demand spikes that deplete localized warehouse stock to zero within seconds.")
add_bullet(tf, "2. Unhandled Microservice Boundary Crashes:", "Algorithms computing discount allocations or delivery slots encounter fatal ZeroDivisionError when stock drops to 0, crashing WSGI worker threads with HTTP 500.")
add_bullet(tf, "3. Crippling Administrative Delay (Elevated MTTA):", "Traditional monitoring leaves crashes in raw CloudWatch streams. Engineers spend 2 to 8 hours manually locating logs, reproducing errors, and typing Jira/GitHub tickets.")
add_bullet(tf, "4. The DevOps Incident Watchdog Solution:", "An event-driven, closed-loop SRE platform that autonomously captures crashes in CloudWatch, archives forensic JSON dumps in Amazon S3, mints structured Agile Bug Stories on GitHub, and enables automated CI/CD closure upon verified fix.")

# ==============================================================================
# SLIDE 3: HIGH-LEVEL MINIMAL ARCHITECTURE (FIGURE 1)
# ==============================================================================
slide3 = prs.slides.add_slide(blank_layout)
add_header(slide3, "System Architecture: Decoupled Three-Tier Topology", "System Architecture")

tx = slide3.shapes.add_textbox(Inches(0.8), Inches(1.4), Inches(4.8), Inches(5.3))
tf = tx.text_frame
tf.word_wrap = True
tf.paragraphs[0].text = "Core Subsystems & Responsibilities:"
tf.paragraphs[0].font.name = "Arial"
tf.paragraphs[0].font.size = Pt(15)
tf.paragraphs[0].font.bold = True
tf.paragraphs[0].font.color.rgb = BLUE

add_bullet(tf, "Presentation Tier:", "FlashMart Single-Page Application (SPA) with dynamic delivery hub routing defaulting to VIT Vellore Campus.")
add_bullet(tf, "Serverless Compute Tier:", "AWS Lambda microservices (Python 3.12, Flask adapter) coupled with asynchronous Watchdog triage worker.")
add_bullet(tf, "Cloud & Agile Tier:", "Amazon CloudWatch real-time metric ingestion, Amazon S3 immutable forensic vault, and GitHub Issues Kanban board.")

img_path = os.path.join(base_dir, "architecture_diagram.png")
if os.path.exists(img_path):
    slide3.shapes.add_picture(img_path, Inches(5.8), Inches(1.6), Inches(6.8))

# ==============================================================================
# SLIDE 4: FLASHMART STOREFRONT & VIT HUB (FIGURE 5)
# ==============================================================================
slide4 = prs.slides.add_slide(blank_layout)
add_header(slide4, "Module 1: FlashMart Storefront & Campus Delivery Hub", "Microservice Features")

tx = slide4.shapes.add_textbox(Inches(0.8), Inches(1.4), Inches(4.8), Inches(5.3))
tf = tx.text_frame
tf.word_wrap = True
tf.paragraphs[0].text = "Customer Presentation Capabilities:"
tf.paragraphs[0].font.name = "Arial"
tf.paragraphs[0].font.size = Pt(15)
tf.paragraphs[0].font.bold = True
tf.paragraphs[0].font.color.rgb = BLUE

add_bullet(tf, "10-Minute Express Electronics:", "Realistic quick-commerce catalog offering electronics, smartphones, and accessories with zero external Node.js dependencies.")
add_bullet(tf, "VIT Vellore Hub Selector:", "Dynamic location routing defaulting to VIT Vellore Campus (Men's Hostel Q-Block Dark Store).")
add_bullet(tf, "Promotional Flash Sale Deal:", "Features OnePlus 11R 5G flash sale pricing with real-time countdown timer to test localized demand exhaustion.")

img_path = os.path.join(base_dir, "snapshot1_storefront.png")
if os.path.exists(img_path):
    slide4.shapes.add_picture(img_path, Inches(5.8), Inches(1.5), Inches(6.8))

# ==============================================================================
# SLIDE 5: THE UNHANDLED RUNTIME CRASH (FIGURE 7)
# ==============================================================================
slide5 = prs.slides.add_slide(blank_layout)
add_header(slide5, "Module 3: Server ZeroDivisionError Crash & Telemetry", "Incident Reproduction")

tx = slide5.shapes.add_textbox(Inches(0.8), Inches(1.4), Inches(4.8), Inches(5.3))
tf = tx.text_frame
tf.word_wrap = True
tf.paragraphs[0].text = "Runtime Microservice Failure:"
tf.paragraphs[0].font.name = "Arial"
tf.paragraphs[0].font.size = Pt(15)
tf.paragraphs[0].font.bold = True
tf.paragraphs[0].font.color.rgb = RED

add_bullet(tf, "The Stockout Edge-Case:", "When inventory reaches stock = 0 at the VIT Vellore dark store, the checkout worker executes: allocation = 100 / stock.")
add_bullet(tf, "Fatal Python Exception:", "Raises an unhandled ZeroDivisionError, crashing the worker thread and returning HTTP 500 Internal Server Error.")
add_bullet(tf, "Structured Telemetry Emission:", "Logger immediately emits [CRITICAL_ALERT] INCIDENT_DETECTED with exception context and timestamp to stdout.")

img_path = os.path.join(base_dir, "snapshot3_server_crash.png")
if os.path.exists(img_path):
    slide5.shapes.add_picture(img_path, Inches(5.8), Inches(1.5), Inches(6.8))

# ==============================================================================
# SLIDE 6: GRACEFUL CUSTOMER INSULATION (FIGURE 6)
# ==============================================================================
slide6 = prs.slides.add_slide(blank_layout)
add_header(slide6, "Module 2: Client Stockout Exception Interception", "Customer Insulation")

tx = slide6.shapes.add_textbox(Inches(0.8), Inches(1.4), Inches(4.8), Inches(5.3))
tf = tx.text_frame
tf.word_wrap = True
tf.paragraphs[0].text = "Defensive Client Safeguards:"
tf.paragraphs[0].font.name = "Arial"
tf.paragraphs[0].font.size = Pt(15)
tf.paragraphs[0].font.bold = True
tf.paragraphs[0].font.color.rgb = GREEN

add_bullet(tf, "HTTP 500 Interception:", "Client SPA intercepts server 500 errors before browser rendering, completely preventing white-screen crashes.")
add_bullet(tf, "Informative Waitlist Modal:", "Renders 'Item Not Deliverable to Your Location' modal explaining out-of-stock condition at VIT Vellore Hub.")
add_bullet(tf, "Customer Trust Preservation:", "Offers a polite 'Notify Me When Available' button and alternate dark store selection, preserving brand equity.")

img_path = os.path.join(base_dir, "snapshot2_stockout_drawer.png")
if os.path.exists(img_path):
    slide6.shapes.add_picture(img_path, Inches(5.8), Inches(1.5), Inches(6.8))

# ==============================================================================
# SLIDE 7: CLOUDWATCH METRIC FILTER INGESTION (FIGURE 8)
# ==============================================================================
slide7 = prs.slides.add_slide(blank_layout)
add_header(slide7, "Module 4: AWS CloudWatch Metric Ingestion & SRE Console", "SRE Observability")

tx = slide7.shapes.add_textbox(Inches(0.8), Inches(1.4), Inches(4.8), Inches(5.3))
tf = tx.text_frame
tf.word_wrap = True
tf.paragraphs[0].text = "Sub-5-Second Incident Ingestion:"
tf.paragraphs[0].font.name = "Arial"
tf.paragraphs[0].font.size = Pt(15)
tf.paragraphs[0].font.bold = True
tf.paragraphs[0].font.color.rgb = BLUE

add_bullet(tf, "Non-Invasive Log Filtering:", "CloudWatch Metric Filter continuously monitors /aws/lambda/watchdog-target-app log stream matching [CRITICAL_ALERT].")
add_bullet(tf, "Zero Polling Latency:", "Fires CloudWatch alarm and triggers Watchdog Lambda asynchronously within 4.2 seconds.")
add_bullet(tf, "SRE Backstage Dashboard:", "Dedicated operator console displaying active CloudWatch metrics, S3 dump links, and Agile backlog sync status.")

img_path = os.path.join(base_dir, "snapshot4_sre_dashboard.png")
if os.path.exists(img_path):
    slide7.shapes.add_picture(img_path, Inches(5.8), Inches(1.5), Inches(6.8))

# ==============================================================================
# SLIDE 8: IMMUTABLE FORENSIC ARCHIVAL IN S3 (FIGURE 9)
# ==============================================================================
slide8 = prs.slides.add_slide(blank_layout)
add_header(slide8, "Module 5: Forensic JSON Vault in Amazon S3", "Forensic Compliance")

tx = slide8.shapes.add_textbox(Inches(0.8), Inches(1.4), Inches(4.8), Inches(5.3))
tf = tx.text_frame
tf.word_wrap = True
tf.paragraphs[0].text = "Tamper-Proof Audit Evidence:"
tf.paragraphs[0].font.name = "Arial"
tf.paragraphs[0].font.size = Pt(15)
tf.paragraphs[0].font.bold = True
tf.paragraphs[0].font.color.rgb = BLUE

add_bullet(tf, "Comprehensive JSON Dump:", "Captures uncompressed stack trace, git commit SHA, HTTP headers, timestamp, and dark store hub identifier.")
add_bullet(tf, "11 9's Durability Guarantee:", "Stored in private S3 bucket (devops-incident-watchdog-logs-401537512022) with Block Public Access and AES-256 encryption.")
add_bullet(tf, "Cryptographic INC-ID:", "Mints immutable key: incidents/YYYY-MM-DD/INC-1791945923-07CD12B5.json for audit permanence.")

img_path = os.path.join(base_dir, "snapshot5_s3_vault.png")
if os.path.exists(img_path):
    slide8.shapes.add_picture(img_path, Inches(5.8), Inches(1.5), Inches(6.8))

# ==============================================================================
# SLIDE 9: AUTOMATED AGILE USER STORY MINTING (FIGURE 10)
# ==============================================================================
slide9 = prs.slides.add_slide(blank_layout)
add_header(slide9, "Module 6: Autonomous Bug Story Minting on GitHub Issues", "Agile Backlog Integration")

tx = slide9.shapes.add_textbox(Inches(0.8), Inches(1.4), Inches(4.8), Inches(5.3))
tf = tx.text_frame
tf.word_wrap = True
tf.paragraphs[0].text = "Zero-Touch Sprint Ticket Creation:"
tf.paragraphs[0].font.name = "Arial"
tf.paragraphs[0].font.size = Pt(15)
tf.paragraphs[0].font.bold = True
tf.paragraphs[0].font.color.rgb = BLUE

add_bullet(tf, "GitHub REST API v3 Integration:", "Watchdog Lambda dispatches authenticated HTTP POST call to create structured Bug User Story within 24 seconds.")
add_bullet(tf, "Standardized Diagnostics Table:", "Embeds incident ID, error type, target microservice, VIT campus hub, and direct S3 forensic URI link.")
add_bullet(tf, "6 Definition of Done (DoD) Criteria:", "Includes explicit acceptance criteria checkboxes ensuring code guard, customer insulation, and pytest CI verification.")

img_path = os.path.join(base_dir, "snapshot6_github_issue.png")
if os.path.exists(img_path):
    slide9.shapes.add_picture(img_path, Inches(5.8), Inches(1.5), Inches(6.8))

# ==============================================================================
# SLIDE 10: CI/CD REGRESSION & SMART COMMIT CLOSE (FIGURE 11)
# ==============================================================================
slide10 = prs.slides.add_slide(blank_layout)
add_header(slide10, "Module 7: Automated Pytest CI/CD & Smart Commit Closure", "Continuous Remediation")

tx = slide10.shapes.add_textbox(Inches(0.8), Inches(1.4), Inches(4.8), Inches(5.3))
tf = tx.text_frame
tf.word_wrap = True
tf.paragraphs[0].text = "GitOps Automated Lifecycle:"
tf.paragraphs[0].font.name = "Arial"
tf.paragraphs[0].font.size = Pt(15)
tf.paragraphs[0].font.bold = True
tf.paragraphs[0].font.color.rgb = GREEN

add_bullet(tf, "Smart Commit Syntax:", "Developer commits code fix with: git commit -am 'Fixes #1: Handled division by zero in checkout logic'.")
add_bullet(tf, "GitHub Actions CI Runner:", "Automatically executes 9 Pytest regression test suites on Ubuntu runner in 0.53 seconds (100% test pass rate).")
add_bullet(tf, "Zero-Touch Issue Closure:", "Redeploys patched package to AWS Lambda and automatically transitions GitHub Issue #1 to Closed (Done).")

img_path = os.path.join(base_dir, "snapshot7_cicd_pipeline.png")
if os.path.exists(img_path):
    slide10.shapes.add_picture(img_path, Inches(5.8), Inches(1.5), Inches(6.8))

# ==============================================================================
# SLIDE 11: SECURITY SAFETY GATES (FIGURE 3)
# ==============================================================================
slide11 = prs.slides.add_slide(blank_layout)
add_header(slide11, "Closed-Loop Telemetry & GitOps Security Safety Gates", "Security Architecture")

tx = slide11.shapes.add_textbox(Inches(0.8), Inches(1.4), Inches(4.8), Inches(5.3))
tf = tx.text_frame
tf.word_wrap = True
tf.paragraphs[0].text = "Enforced Architectural Invariants:"
tf.paragraphs[0].font.name = "Arial"
tf.paragraphs[0].font.size = Pt(15)
tf.paragraphs[0].font.bold = True
tf.paragraphs[0].font.color.rgb = BLUE

add_bullet(tf, "Gate 1 & 2 (Ingestion & Isolation):", "Read-only CloudWatch subscription; serverless sandbox with zero persistent host state.")
add_bullet(tf, "Gate 3 & 4 (Durability & IAM):", "S3 Private Bucket with AES-256 SSE; strictly scoped IAM execution roles (S3 PutObject only).")
add_bullet(tf, "Gate 5 & 6 (Backlog & Testing):", "Sanitized ticket payload (zero PII); mandatory 9 Pytest regression tests passing before deployment.")
add_bullet(tf, "Gate 7 (Traceability):", "Immutable GitOps SHA commit linking directly to Issue #1.")

img_path = os.path.join(base_dir, "figure3_safety_gates.png")
if os.path.exists(img_path):
    slide11.shapes.add_picture(img_path, Inches(5.8), Inches(1.5), Inches(6.8))

# ==============================================================================
# SLIDE 12: AWS PRODUCTION TOPOLOGY & COST (FIGURE 4)
# ==============================================================================
slide12 = prs.slides.add_slide(blank_layout)
add_header(slide12, "AWS Serverless Production Deployment & Cost Breakdown", "Cloud Deployment")

tx = slide12.shapes.add_textbox(Inches(0.8), Inches(1.4), Inches(4.8), Inches(5.3))
tf = tx.text_frame
tf.word_wrap = True
tf.paragraphs[0].text = "Production Cloud Parameters:"
tf.paragraphs[0].font.name = "Arial"
tf.paragraphs[0].font.size = Pt(15)
tf.paragraphs[0].font.bold = True
tf.paragraphs[0].font.color.rgb = BLUE

add_bullet(tf, "AWS Region:", "Deployed serverless in Sydney (ap-southeast-2) under AWS Account 401537512022.")
add_bullet(tf, "Compute Sizing:", "Both watchdog-target-app and watchdog-incident-creator configured with 128 MB RAM (sub-300ms cold starts).")
add_bullet(tf, "100% Free Tier Eligible ($0.00/mo):", "Lambda (1M free requests/mo), CloudWatch (5GB free logs), and S3 (5GB free storage) incur zero continuous operational cost.")

img_path = os.path.join(base_dir, "figure4_aws_topology.png")
if os.path.exists(img_path):
    slide12.shapes.add_picture(img_path, Inches(5.8), Inches(1.5), Inches(6.8))

# ==============================================================================
# SLIDE 13: END-TO-END WORKFLOW SUMMARY (FIGURE 2)
# ==============================================================================
slide13 = prs.slides.add_slide(blank_layout)
add_header(slide13, "Summary of the 7-Stage End-to-End Incident Lifecycle", "Workflow Lifecycle")

tx = slide13.shapes.add_textbox(Inches(0.8), Inches(1.4), Inches(11.7), Inches(2.2))
tf = tx.text_frame
tf.word_wrap = True
p = tf.paragraphs[0]
p.text = "From unhandled runtime microservice crash to zero-touch sprint closure across 7 automated stages:"
p.font.name = "Arial"
p.font.size = Pt(15)
p.font.color.rgb = SLATE

img_path = os.path.join(base_dir, "figure2_workflow.png")
if os.path.exists(img_path):
    slide13.shapes.add_picture(img_path, Inches(1.2), Inches(2.3), Inches(10.9))

tx_sub = slide13.shapes.add_textbox(Inches(0.8), Inches(5.2), Inches(11.7), Inches(1.8))
tf_s = tx_sub.text_frame
tf_s.word_wrap = True
add_bullet(tf_s, "Continuous SRE Feedback Loop:", "Eliminates manual triage handoffs, guarantees 11 9's forensic compliance, and maintains real-time Agile velocity tracking.")

# ==============================================================================
# SLIDE 14: CONCLUSION & VERIFIED METRICS
# ==============================================================================
slide14 = prs.slides.add_slide(blank_layout)
bg14 = slide14.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), Inches(13.333), Inches(7.5))
bg14.fill.solid()
bg14.fill.fore_color.rgb = NAVY
bg14.line.fill.background()

tx_c = slide14.shapes.add_textbox(Inches(1.0), Inches(0.8), Inches(11.333), Inches(6.0))
tf_c = tx_c.text_frame
tf_c.word_wrap = True

p_c_head = tf_c.paragraphs[0]
p_c_head.text = "VERIFIED PROJECT OUTCOMES & CONCLUSION"
p_c_head.font.name = "Arial"
p_c_head.font.size = Pt(24)
p_c_head.font.bold = True
p_c_head.font.color.rgb = RGBColor(56, 189, 248)

p_c_desc = tf_c.add_paragraph()
p_c_desc.text = "DevOps Incident Watchdog establishes a fully autonomous, closed-loop Site Reliability Engineering feedback bridge for cloud-native microservices:"
p_c_desc.font.name = "Arial"
p_c_desc.font.size = Pt(15)
p_c_desc.font.color.rgb = RGBColor(226, 232, 240)
p_c_desc.space_before = Pt(10)

def add_stat_box(slide, left, top, num_text, label_text, color_rgb):
    box = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, left, top, Inches(2.6), Inches(1.6))
    box.fill.solid()
    box.fill.fore_color.rgb = SLATE
    box.line.color.rgb = color_rgb
    box.line.width = Pt(2)
    
    tf = box.text_frame
    tf.word_wrap = True
    p1 = tf.paragraphs[0]
    p1.text = num_text
    p1.alignment = PP_ALIGN.CENTER
    p1.font.name = "Arial"
    p1.font.size = Pt(28)
    p1.font.bold = True
    p1.font.color.rgb = color_rgb
    
    p2 = tf.add_paragraph()
    p2.text = label_text
    p2.alignment = PP_ALIGN.CENTER
    p2.font.name = "Arial"
    p2.font.size = Pt(12)
    p2.font.color.rgb = WHITE
    p2.space_before = Pt(4)

add_stat_box(slide14, Inches(1.0), Inches(2.6), "< 24s", "Incident-to-Ticket Filing\n(vs. 2–8 Hours Manual)", RGBColor(56, 189, 248))
add_stat_box(slide14, Inches(3.9), Inches(2.6), "0.53s", "Pytest Suite Execution\n(9/9 Tests Passing 100%)", RGBColor(74, 222, 128))
add_stat_box(slide14, Inches(6.8), Inches(2.6), "11 9's", "S3 Durability SLA\n(Immutable Forensics)", RGBColor(250, 204, 21))
add_stat_box(slide14, Inches(9.7), Inches(2.6), "$0.00", "Monthly Infrastructure\n(100% Free Tier)", RGBColor(168, 85, 247))

tx_end = slide14.shapes.add_textbox(Inches(1.0), Inches(4.7), Inches(11.333), Inches(2.0))
tf_e = tx_end.text_frame
tf_e.word_wrap = True

p_e1 = tf_e.paragraphs[0]
p_e1.text = "Key Takeaway for Faculty Evaluation:"
p_e1.font.name = "Arial"
p_e1.font.size = Pt(16)
p_e1.font.bold = True
p_e1.font.color.rgb = WHITE

p_e2 = tf_e.add_paragraph()
p_e2.text = "By shifting incident triage from manual, error-prone on-call rotations to software-defined, event-driven automation, the project demonstrates that Agile velocity and Site Reliability Engineering operate in complete harmony."
p_e2.font.name = "Arial"
p_e2.font.size = Pt(13.5)
p_e2.font.color.rgb = RGBColor(203, 213, 225)
p_e2.space_before = Pt(6)

p_thank = tf_e.add_paragraph()
p_thank.text = "Thank You! Open for Faculty Demonstration & Technical Q&A."
p_thank.font.name = "Arial"
p_thank.font.size = Pt(16)
p_thank.font.bold = True
p_thank.font.color.rgb = RGBColor(56, 189, 248)
p_thank.space_before = Pt(12)

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
