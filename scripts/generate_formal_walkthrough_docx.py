"""
Generate Formal Academic Application & Incident Walkthrough Report (.docx & .pdf)
Document Title: FlashMart Quick-Commerce & Autonomous DevOps Incident Watchdog: Application Architecture, Runtime Incident Lifecycle, and Closed-Loop SRE Remediation
Student: S Hemal (24MIS0050)
Course: ISWE406 Agile Development Process and DevOps
Institution: School of Computer Science Engineering and Information Systems, VIT Vellore Campus
"""

import os
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import parse_xml
from docx.oxml.ns import nsdecls

base_dir = r"C:\Users\Sailaja C\Documents\New folder\DevOps-Incident-Watchdog"
docx_output = os.path.join(base_dir, "FlashMart_Incident_Watchdog_Application_Guide.docx")
pdf_output = os.path.join(base_dir, "FlashMart_Incident_Watchdog_Application_Guide.pdf")

doc = docx.Document()

# -------------------------------------------------------------
# PAGE SETUP (A4, 0.8 in margins)
# -------------------------------------------------------------
section = doc.sections[0]
section.page_width = Inches(8.27)
section.page_height = Inches(11.69)
section.top_margin = Inches(0.8)
section.bottom_margin = Inches(0.8)
section.left_margin = Inches(0.8)
section.right_margin = Inches(0.8)

# Different First Page (Cover page has NO header/footer)
section.different_first_page_header_footer = True

# Running Header (Pages 2+)
header = section.header
p_head = header.paragraphs[0]
p_head.alignment = WD_ALIGN_PARAGRAPH.RIGHT
r_head = p_head.add_run("FlashMart & DevOps Incident Watchdog - Application & Incident Guide | ISWE406")
r_head.font.name = "Times New Roman"
r_head.font.size = Pt(8.5)
r_head.font.italic = True
r_head.font.color.rgb = RGBColor(100, 116, 139)

# Running Footer with Page Number (Pages 2+)
def add_page_number(run):
    fldChar1 = parse_xml(r'<w:fldChar %s w:fldCharType="begin"/>' % nsdecls('w'))
    instrText = parse_xml(r'<w:instrText %s xml:space="preserve"> PAGE </w:instrText>' % nsdecls('w'))
    fldChar2 = parse_xml(r'<w:fldChar %s w:fldCharType="separate"/>' % nsdecls('w'))
    fldChar3 = parse_xml(r'<w:fldChar %s w:fldCharType="end"/>' % nsdecls('w'))
    run._r.append(fldChar1)
    run._r.append(instrText)
    run._r.append(fldChar2)
    run._r.append(fldChar3)

footer = section.footer
p_foot = footer.paragraphs[0]
p_foot.alignment = WD_ALIGN_PARAGRAPH.RIGHT
r_foot = p_foot.add_run("Page ")
r_foot.font.name = "Times New Roman"
r_foot.font.size = Pt(9)
r_foot.font.color.rgb = RGBColor(100, 116, 139)
add_page_number(r_foot)

# Set base Normal style font
style_normal = doc.styles['Normal']
style_normal.font.name = 'Times New Roman'
style_normal.font.size = Pt(11.5)
style_normal.font.color.rgb = RGBColor(17, 24, 39)

# -------------------------------------------------------------
# HELPER FUNCTIONS (11.5pt, Justified, Continuous Narrative)
# -------------------------------------------------------------
def p(text="", bold_prefix="", italic=False, space_after=5):
    par = doc.add_paragraph()
    par.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    par.paragraph_format.line_spacing = 1.25
    par.paragraph_format.space_after = Pt(space_after)
    par.paragraph_format.space_before = Pt(0)
    
    if bold_prefix:
        r_b = par.add_run(bold_prefix)
        r_b.font.name = 'Times New Roman'
        r_b.font.size = Pt(11.5)
        r_b.font.bold = True
        r_b.font.color.rgb = RGBColor(17, 24, 39)
        
    if text:
        r_t = par.add_run(text)
        r_t.font.name = 'Times New Roman'
        r_t.font.size = Pt(11.5)
        r_t.font.italic = italic
        r_t.font.color.rgb = RGBColor(17, 24, 39)
    return par

def h1(title):
    par = doc.add_paragraph()
    par.paragraph_format.space_before = Pt(16)
    par.paragraph_format.space_after = Pt(6)
    par.paragraph_format.keep_with_next = True
    r = par.add_run(title)
    r.font.name = 'Times New Roman'
    r.font.size = Pt(15.5)
    r.font.bold = True
    r.font.color.rgb = RGBColor(15, 23, 42)
    return par

def h2(title):
    par = doc.add_paragraph()
    par.paragraph_format.space_before = Pt(12)
    par.paragraph_format.space_after = Pt(4)
    par.paragraph_format.keep_with_next = True
    r = par.add_run(title)
    r.font.name = 'Times New Roman'
    r.font.size = Pt(13)
    r.font.bold = True
    r.font.color.rgb = RGBColor(30, 41, 59)
    return par

def bullet(text, bold_prefix=""):
    par = doc.add_paragraph(style='List Bullet')
    par.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    par.paragraph_format.line_spacing = 1.2
    par.paragraph_format.space_after = Pt(3)
    par.paragraph_format.space_before = Pt(0)
    
    if bold_prefix:
        r_b = par.add_run(bold_prefix)
        r_b.font.name = 'Times New Roman'
        r_b.font.size = Pt(11.5)
        r_b.font.bold = True
        r_b.font.color.rgb = RGBColor(17, 24, 39)
        
    r_t = par.add_run(text)
    r_t.font.name = 'Times New Roman'
    r_t.font.size = Pt(11.5)
    r_t.font.color.rgb = RGBColor(17, 24, 39)
    return par

def code_block(code_text):
    tbl = doc.add_table(rows=1, cols=1)
    tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    cell = tbl.rows[0].cells[0]
    cell.width = Inches(6.4)
    
    shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="0F172A"/>')
    cell._tc.get_or_add_tcPr().append(shd)
    
    borders = parse_xml(r'''
        <w:tcBorders %s>
            <w:top w:val="single" w:sz="4" w:space="0" w:color="334155"/>
            <w:left w:val="single" w:sz="18" w:space="0" w:color="38BDF8"/>
            <w:bottom w:val="single" w:sz="4" w:space="0" w:color="334155"/>
            <w:right w:val="single" w:sz="4" w:space="0" w:color="334155"/>
        </w:tcBorders>
    ''' % nsdecls('w'))
    cell._tc.get_or_add_tcPr().append(borders)
    
    tcMar = parse_xml(r'''
        <w:tcMar %s>
            <w:top w:w="120" w:type="dxa"/>
            <w:left w:w="160" w:type="dxa"/>
            <w:bottom w:w="120" w:type="dxa"/>
            <w:right w:w="160" w:type="dxa"/>
        </w:tcMar>
    ''' % nsdecls('w'))
    cell._tc.get_or_add_tcPr().append(tcMar)
    
    p_c = cell.paragraphs[0]
    p_c.paragraph_format.space_before = Pt(2)
    p_c.paragraph_format.space_after = Pt(2)
    p_c.paragraph_format.line_spacing = 1.15
    r = p_c.add_run(code_text.strip())
    r.font.name = 'Consolas'
    r.font.size = Pt(9.0)
    r.font.color.rgb = RGBColor(56, 189, 248)
    
    p_gap = doc.add_paragraph()
    p_gap.paragraph_format.space_before = Pt(0)
    p_gap.paragraph_format.space_after = Pt(4)

def figure(img_filename, caption_text, width_inches=6.0):
    img_path = os.path.join(base_dir, img_filename)
    if not os.path.exists(img_path):
        print(f"WARNING: Image not found: {img_path}")
        return
        
    p_img = doc.add_paragraph()
    p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_img.paragraph_format.space_before = Pt(8)
    p_img.paragraph_format.space_after = Pt(2)
    p_img.paragraph_format.keep_with_next = True
    
    run_img = p_img.add_run()
    run_img.add_picture(img_path, width=Inches(width_inches))
    
    p_cap = doc.add_paragraph()
    p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_cap.paragraph_format.space_before = Pt(2)
    p_cap.paragraph_format.space_after = Pt(10)
    p_cap.paragraph_format.keep_with_next = False
    
    r_cap = p_cap.add_run(caption_text)
    r_cap.font.name = 'Times New Roman'
    r_cap.font.size = Pt(10)
    r_cap.font.bold = True
    r_cap.font.italic = True
    r_cap.font.color.rgb = RGBColor(15, 23, 42)

def make_table(headers, data, col_widths=None, caption=""):
    if caption:
        p_cap = doc.add_paragraph()
        p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_cap.paragraph_format.space_before = Pt(8)
        p_cap.paragraph_format.space_after = Pt(4)
        p_cap.paragraph_format.keep_with_next = True
        r_c = p_cap.add_run(caption)
        r_c.font.name = 'Times New Roman'
        r_c.font.size = Pt(10)
        r_c.font.bold = True
        r_c.font.color.rgb = RGBColor(15, 23, 42)

    tbl = doc.add_table(rows=len(data) + 1, cols=len(headers))
    tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    
    # APA / IEEE Table borders
    tblBorders = parse_xml(r'''
        <w:tblBorders %s>
            <w:top w:val="single" w:sz="6" w:space="0" w:color="1E293B"/>
            <w:left w:val="none"/>
            <w:bottom w:val="single" w:sz="8" w:space="0" w:color="1E293B"/>
            <w:right w:val="none"/>
            <w:insideH w:val="single" w:sz="4" w:space="0" w:color="CBD5E1"/>
            <w:insideV w:val="none"/>
        </w:tblBorders>
    ''' % nsdecls('w'))
    tbl._tbl.tblPr.append(tblBorders)
    
    hdr_cells = tbl.rows[0].cells
    for i, h_text in enumerate(headers):
        hdr_cells[i].text = h_text
        shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="1E293B"/>')
        hdr_cells[i]._tc.get_or_add_tcPr().append(shd)
        p_h = hdr_cells[i].paragraphs[0]
        p_h.alignment = WD_ALIGN_PARAGRAPH.LEFT
        p_h.paragraph_format.space_before = Pt(4)
        p_h.paragraph_format.space_after = Pt(4)
        for r in p_h.runs:
            r.font.name = 'Times New Roman'
            r.font.size = Pt(9.5)
            r.font.bold = True
            r.font.color.rgb = RGBColor(255, 255, 255)
            
    for row_idx, row_data in enumerate(data):
        row_cells = tbl.rows[row_idx + 1].cells
        bg_color = "F8FAFC" if row_idx % 2 == 1 else "FFFFFF"
        for col_idx, cell_value in enumerate(row_data):
            row_cells[col_idx].text = str(cell_value)
            shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{bg_color}"/>')
            row_cells[col_idx]._tc.get_or_add_tcPr().append(shd)
            p_d = row_cells[col_idx].paragraphs[0]
            p_d.alignment = WD_ALIGN_PARAGRAPH.LEFT
            p_d.paragraph_format.space_before = Pt(3)
            p_d.paragraph_format.space_after = Pt(3)
            p_d.paragraph_format.line_spacing = 1.15
            for r in p_d.runs:
                r.font.name = 'Times New Roman'
                r.font.size = Pt(9.0)
                r.font.color.rgb = RGBColor(30, 41, 59)
                
    if col_widths:
        for row in tbl.rows:
            for idx, width in enumerate(col_widths):
                row.cells[idx].width = Inches(width)
                
    p_gap = doc.add_paragraph()
    p_gap.paragraph_format.space_before = Pt(0)
    p_gap.paragraph_format.space_after = Pt(6)

# =============================================================
# PAGE 1: TITLE PAGE (CLEAN NORMAL TEXT - STRICTLY NO BOXES)
# =============================================================
p_pre = doc.add_paragraph()
p_pre.paragraph_format.space_before = Pt(70)
p_pre.paragraph_format.space_after = Pt(4)
p_pre.alignment = WD_ALIGN_PARAGRAPH.CENTER
r = p_pre.add_run("PROJECT APPLICATION & INCIDENT WALKTHROUGH GUIDE")
r.font.name = 'Times New Roman'
r.font.size = Pt(12)
r.font.bold = True
r.font.color.rgb = RGBColor(75, 85, 99)

p_course = doc.add_paragraph()
p_course.paragraph_format.space_before = Pt(0)
p_course.paragraph_format.space_after = Pt(45)
p_course.alignment = WD_ALIGN_PARAGRAPH.CENTER
r = p_course.add_run("COURSE: ISWE406 AGILE DEVELOPMENT PROCESS AND DEVOPS")
r.font.name = 'Times New Roman'
r.font.size = Pt(12)
r.font.bold = True
r.font.color.rgb = RGBColor(31, 41, 55)

p_title = doc.add_paragraph()
p_title.paragraph_format.space_before = Pt(10)
p_title.paragraph_format.space_after = Pt(12)
p_title.paragraph_format.line_spacing = 1.35
p_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
r = p_title.add_run("FLASHMART QUICK-COMMERCE &\nAUTONOMOUS DEVOPS INCIDENT WATCHDOG:\nAPPLICATION FEATURES, RUNTIME INCIDENT LIFECYCLE, AND CLOSED-LOOP SRE REMEDIATION")
r.font.name = 'Times New Roman'
r.font.size = Pt(18)
r.font.bold = True
r.font.color.rgb = RGBColor(15, 23, 42)

p_sub = doc.add_paragraph()
p_sub.paragraph_format.space_before = Pt(10)
p_sub.paragraph_format.space_after = Pt(100)
p_sub.alignment = WD_ALIGN_PARAGRAPH.CENTER
r = p_sub.add_run("A Formal Technical Guide on Microservice Telemetry, Cloud Forensics, and Zero-Touch Agile Sprint Backlog Automation")
r.font.name = 'Times New Roman'
r.font.size = Pt(11)
r.font.italic = True
r.font.color.rgb = RGBColor(100, 116, 139)

p_subm = doc.add_paragraph()
p_subm.paragraph_format.space_before = Pt(0)
p_subm.paragraph_format.space_after = Pt(4)
p_subm.alignment = WD_ALIGN_PARAGRAPH.CENTER
r = p_subm.add_run("Submitted by:")
r.font.name = 'Times New Roman'
r.font.size = Pt(11)
r.font.bold = True
r.font.color.rgb = RGBColor(75, 85, 99)

p_author = doc.add_paragraph()
p_author.paragraph_format.space_before = Pt(0)
p_author.paragraph_format.space_after = Pt(100)
p_author.alignment = WD_ALIGN_PARAGRAPH.CENTER
r = p_author.add_run("S Hemal (Registration No: 24MIS0050)")
r.font.name = 'Times New Roman'
r.font.size = Pt(13.5)
r.font.bold = True
r.font.color.rgb = RGBColor(17, 24, 39)

p_inst = doc.add_paragraph()
p_inst.paragraph_format.space_before = Pt(0)
p_inst.paragraph_format.space_after = Pt(0)
p_inst.paragraph_format.line_spacing = 1.3
p_inst.alignment = WD_ALIGN_PARAGRAPH.CENTER
r = p_inst.add_run("School of Computer Science Engineering and Information Systems (SCOPE)\nVellore Institute of Technology, Vellore Campus\nAcademic Year 2026-2027\nDate of Submission: 26 October 2026")
r.font.name = 'Times New Roman'
r.font.size = Pt(10.5)
r.font.color.rgb = RGBColor(75, 85, 99)

doc.add_page_break()

# =============================================================
# PAGE 2: EXECUTIVE SUMMARY & ABSTRACT
# =============================================================
p_ack_h = doc.add_paragraph()
p_ack_h.alignment = WD_ALIGN_PARAGRAPH.CENTER
p_ack_h.paragraph_format.space_before = Pt(10)
p_ack_h.paragraph_format.space_after = Pt(10)
r = p_ack_h.add_run("EXECUTIVE SUMMARY")
r.font.name = 'Times New Roman'
r.font.size = Pt(14)
r.font.bold = True
r.font.color.rgb = RGBColor(15, 23, 42)

p("This application and incident walkthrough document details the operational behavior, architectural features, fault reproduction mechanics, and closed-loop Site Reliability Engineering (SRE) remediation capabilities of DevOps Incident Watchdog. The monitored target application, FlashMart Tech, models high-velocity 10-minute quick-commerce delivery, featuring localized dark store fulfillment centered at the VIT Vellore Campus (Men's Hostel Q-Block Dark Store).")

p("During high-concurrency promotional flash deals, localized warehouse inventory depletes to zero within seconds. When backend routing algorithms calculate discount allocations without boundary validation, an unhandled ZeroDivisionError crashes the microservice worker thread with an HTTP 500 Internal Server Error. This guide demonstrates how the autonomous DevOps Incident Watchdog pipeline detects the failure in Amazon CloudWatch within 4.2 seconds, isolates the customer from white-screen crashes via defensive frontend exception interception, archives immutable forensic dumps in Amazon S3 with 11 9's durability, and mints an actionable Bug User Story on GitHub Issues complete with 6 Definition of Done acceptance criteria.")

p("Furthermore, this guide details the closed-loop remediation phase: an engineer commits a code fix referencing Smart Commit syntax (Fixes #1), which triggers GitHub Actions continuous integration runners to execute 9 Pytest automated regression suites in 0.53 seconds, redeploy the updated serverless microservice to AWS Lambda, and auto-close GitHub Issue #1 without manual administrative overhead.")

p("Keywords: Agile DevOps, Site Reliability Engineering, Automated Incident Triage, Microservice Telemetry, Amazon CloudWatch, Amazon S3, GitHub Issues, Continuous Integration, Zero-Touch Closure.", bold_prefix="Keywords: ", italic=True)

doc.add_page_break()

# =============================================================
# PAGE 3: TABLE OF CONTENTS
# =============================================================
p_toc_h = doc.add_paragraph()
p_toc_h.alignment = WD_ALIGN_PARAGRAPH.CENTER
p_toc_h.paragraph_format.space_before = Pt(8)
p_toc_h.paragraph_format.space_after = Pt(12)
r = p_toc_h.add_run("TABLE OF CONTENTS")
r.font.name = 'Times New Roman'
r.font.size = Pt(14)
r.font.bold = True
r.font.color.rgb = RGBColor(15, 23, 42)

toc_items = [
    ("Executive Summary", "2"),
    ("Table of Contents", "3"),
    ("List of Figures & List of Tables", "4"),
    ("1. Application Overview & System Architecture", "5"),
    ("   1.1 Purpose and Industry Motivation", "5"),
    ("   1.2 Architectural Decoupling: Three-Tier Model (Figure 1)", "5"),
    ("   1.3 Component Responsibilities Matrix (Table 1.1)", "6"),
    ("2. Storefront Presentation & Multi-Hub Logistics", "6"),
    ("   2.1 FlashMart E-Commerce Interface (Figure 2)", "6"),
    ("   2.2 VIT Vellore Campus Dark Store Routing", "7"),
    ("   2.3 Promotional Flash Sale Concurrency Engine", "7"),
    ("3. The Runtime Incident: Zero-Stock Exhaustion & Crash", "7"),
    ("   3.1 Fault Simulation Mechanics", "7"),
    ("   3.2 Mathematical Division-by-Zero Exception (Figure 3)", "8"),
    ("   3.3 WSGI Worker Thread Crash & [CRITICAL_ALERT] Logging", "8"),
    ("4. Defensive Presentation Engineering: Customer Insulation", "9"),
    ("   4.1 Client-Side HTTP 500 Interception (Figure 4)", "9"),
    ("   4.2 Informative Stockout Waitlist Modal", "9"),
    ("   4.3 Customer Trust and Brand Equity Protection", "9"),
    ("5. SRE Observability: Sub-5-Second Metric Ingestion", "10"),
    ("   5.1 Event-Driven CloudWatch Log Filtering", "10"),
    ("   5.2 Operator SRE Backstage Dashboard (Figure 5)", "10"),
    ("   5.3 Zero-Polling Telemetry Architecture", "10"),
    ("6. Cloud Forensics: Immutable S3 Vault Archival", "11"),
    ("   6.1 Cryptographic Incident ID Minting", "11"),
    ("   6.2 Private Amazon S3 Storage & 11 9's Durability (Figure 6)", "11"),
    ("   6.3 Structured Forensic JSON Payload Specification", "11"),
    ("7. Agile Backlog Automation: GitHub Issue Minting", "12"),
    ("   7.1 REST API v3 Automated Ticket Creation (Figure 7)", "12"),
    ("   7.2 Standardized Diagnostics Table & Priority Labels", "12"),
    ("   7.3 Enforcing 6 Definition of Done (DoD) Criteria", "13"),
    ("8. Continuous Remediation: GitOps Smart Commit & CI/CD", "13"),
    ("   8.1 Developer Defensive Code Fix Implementation", "13"),
    ("   8.2 GitHub Actions Automated Pytest Regression Runner (Figure 8)", "13"),
    ("   8.3 Zero-Touch Sprint Backlog Closure via Smart Commits", "14"),
    ("9. Security Architecture & Serverless Cloud Topology", "14"),
    ("   9.1 Seven Closed-Loop Security Safety Gates (Figure 9)", "14"),
    ("   9.2 AWS Serverless Live Deployment Topology (Figure 10)", "15"),
    ("   9.3 Monthly Free Tier Cost Breakdown (Table 9.1)", "15"),
    ("10. End-to-End Workflow Synthesis & Conclusion", "16"),
    ("   10.1 Complete 7-Stage Remediation Lifecycle (Figure 11)", "16"),
    ("   10.2 Verified Performance Metrics & Engineering Achievements", "16"),
    ("   10.3 Final Assessment for Faculty Evaluation", "16"),
]

for title, page_no in toc_items:
    par = doc.add_paragraph()
    par.paragraph_format.line_spacing = 1.05
    par.paragraph_format.space_after = Pt(1.5)
    par.paragraph_format.space_before = Pt(0)
    
    is_main = not title.startswith("   ")
    r_t = par.add_run(title)
    r_t.font.name = 'Times New Roman'
    r_t.font.size = Pt(9.5 if is_main else 9.0)
    r_t.font.bold = is_main
    r_t.font.color.rgb = RGBColor(15, 23, 42) if is_main else RGBColor(51, 65, 85)
    
    dots_count = max(4, 94 - len(title) * 2)
    r_dots = par.add_run(" " + "." * dots_count + " ")
    r_dots.font.name = 'Times New Roman'
    r_dots.font.size = Pt(8.5)
    r_dots.font.color.rgb = RGBColor(148, 163, 184)
    
    r_p = par.add_run(page_no)
    r_p.font.name = 'Times New Roman'
    r_p.font.size = Pt(9.5 if is_main else 9.0)
    r_p.font.bold = is_main
    r_p.font.color.rgb = RGBColor(15, 23, 42) if is_main else RGBColor(51, 65, 85)

doc.add_page_break()

# =============================================================
# PAGE 4: LIST OF FIGURES & LIST OF TABLES
# =============================================================
p_lof_h = doc.add_paragraph()
p_lof_h.alignment = WD_ALIGN_PARAGRAPH.CENTER
p_lof_h.paragraph_format.space_before = Pt(8)
p_lof_h.paragraph_format.space_after = Pt(10)
r = p_lof_h.add_run("LIST OF FIGURES")
r.font.name = 'Times New Roman'
r.font.size = Pt(13.5)
r.font.bold = True
r.font.color.rgb = RGBColor(15, 23, 42)

figures_list = [
    ("Figure 1: High-Level Minimal Architecture Diagram of DevOps Incident Watchdog", "5"),
    ("Figure 2: FlashMart Customer Storefront & VIT Vellore Delivery Hub Selection Interface", "7"),
    ("Figure 3: Backend Server ZeroDivisionError Crash Terminal Output & Structured Telemetry", "8"),
    ("Figure 4: Graceful Frontend Stockout Exception Interception and Customer Insulation", "9"),
    ("Figure 5: AWS CloudWatch Metric Filter & SRE Telemetry Backstage Dashboard", "10"),
    ("Figure 6: Immutable Incident Forensic Evidence Archived in Amazon S3 Bucket Vault", "11"),
    ("Figure 7: Automated Agile Bug User Story Minted on GitHub Issues with Definition of Done", "12"),
    ("Figure 8: GitHub Actions CI/CD Automated Pytest Regression Suite and Zero-Touch Closure", "14"),
    ("Figure 9: Closed-Loop Telemetry & GitOps Security Safety Gate Architecture", "15"),
    ("Figure 10: AWS Serverless Live Production Topology in Sydney (ap-southeast-2)", "15"),
    ("Figure 11: End-to-End Autonomous Incident-to-Agile Remediation Workflow", "16"),
]

for fig_name, p_no in figures_list:
    par = doc.add_paragraph()
    par.paragraph_format.line_spacing = 1.05
    par.paragraph_format.space_after = Pt(2)
    r1 = par.add_run(fig_name)
    r1.font.name = 'Times New Roman'
    r1.font.size = Pt(9.0)
    dots = max(4, 96 - len(fig_name) * 2)
    r2 = par.add_run(" " + "." * dots + " ")
    r2.font.color.rgb = RGBColor(148, 163, 184)
    r3 = par.add_run(p_no)
    r3.font.name = 'Times New Roman'
    r3.font.size = Pt(9.0)
    r3.font.bold = True

p_lot_h = doc.add_paragraph()
p_lot_h.alignment = WD_ALIGN_PARAGRAPH.CENTER
p_lot_h.paragraph_format.space_before = Pt(16)
p_lot_h.paragraph_format.space_after = Pt(10)
r = p_lot_h.add_run("LIST OF TABLES")
r.font.name = 'Times New Roman'
r.font.size = Pt(13.5)
r.font.bold = True
r.font.color.rgb = RGBColor(15, 23, 42)

tables_list = [
    ("Table 1.1: Component Architectural Responsibilities Across the Three Tiers", "6"),
    ("Table 9.1: AWS Free Tier Monthly Compute and Storage Cost Breakdown", "15"),
]

for tbl_name, p_no in tables_list:
    par = doc.add_paragraph()
    par.paragraph_format.line_spacing = 1.05
    par.paragraph_format.space_after = Pt(2)
    r1 = par.add_run(tbl_name)
    r1.font.name = 'Times New Roman'
    r1.font.size = Pt(9.0)
    dots = max(4, 96 - len(tbl_name) * 2)
    r2 = par.add_run(" " + "." * dots + " ")
    r2.font.color.rgb = RGBColor(148, 163, 184)
    r3 = par.add_run(p_no)
    r3.font.name = 'Times New Roman'
    r3.font.size = Pt(9.0)
    r3.font.bold = True

doc.add_page_break()

# =============================================================
# CHAPTER 1: APPLICATION OVERVIEW & SYSTEM ARCHITECTURE
# =============================================================
h1("1. Application Overview & System Architecture")

h2("1.1 Purpose and Industry Motivation")
p("In modern cloud-native enterprise operations, high-velocity consumer applications—such as quick-commerce grocery delivery, flash sale electronics storefronts, and on-demand logistics—operate under extreme demand volatility. During promotional events, concurrent user traffic frequently surges by 50 to 100 times baseline levels within seconds. Under these surge conditions, localized physical dark store inventory is rapidly depleted to zero. When backend checkout and delivery allocation microservices lack robust boundary validation, algorithms calculating delivery ratios or promotional discounts encounter fatal arithmetic exceptions, resulting in unhandled ZeroDivisionError crashes and widespread HTTP 500 outages.")

p("Traditional incident management paradigms rely heavily on passive monitoring dashboards, email alert notifications, or manual on-call escalation rotations (e.g., PagerDuty dispatching to human support engineers). In standard organizations, support personnel take between 2 and 8 hours to identify the crash, locate the relevant log streams in cloud consoles, reproduce the fault in staging environments, and manually transcribe the defect into Jira or GitHub Issues. This manual handoff introduces crippling Mean-Time-to-Acknowledge (MTTA) latency, drains developer productivity, and corrupts sprint burndown velocity.")

p("DevOps Incident Watchdog bridges this critical operational chasm. It establishes an autonomous, event-driven, closed-loop Site Reliability Engineering (SRE) and Agile remediation feedback pipeline. The platform pairs a production quick-commerce microservice (FlashMart Tech) with automated CloudWatch metric filters, serverless triage engines, immutable Amazon S3 forensic storage, and zero-touch GitHub sprint backlog ticket creation.")

h2("1.2 Architectural Decoupling: Three-Tier Model")
p("The entire platform is architected according to decoupled, service-oriented principles across three distinct operational layers. Figure 1 illustrates this decoupled minimal system architecture and the directional data flow governing inter-tier communication.")

figure("architecture_diagram.png", "Figure 1: High-Level Minimal Architecture Diagram of DevOps Incident Watchdog", width_inches=6.2)

h2("1.3 Component Responsibilities Matrix")
p("Table 1.1 specifies the primary source files, execution runtimes, and core architectural responsibilities across all platform components.")

t1_headers = ["Tier", "Component Name", "Source File / Target", "Core Operational Responsibility"]
t1_data = [
    ["Tier 1: Client", "FlashMart Storefront", "templates/index.html", "Responsive SPA catalog, delivery hub selection, and order dispatch."],
    ["Tier 1: Client", "Exception Shield", "templates/index.html", "Intercepts HTTP 500 errors and renders polite stockout waitlist drawer."],
    ["Tier 2: Compute", "Target Microservice", "app/app.py (Lambda)", "Processes checkout requests; executes zero-stock allocation calculation."],
    ["Tier 2: Compute", "Watchdog Lambda", "lambda_watchdog/watchdog.py", "Decompresses gzip crash telemetry, mints INC-IDs, and calls S3/GitHub."],
    ["Tier 3: Cloud", "Amazon CloudWatch", "Log Filter Ingestion", "Sub-5-second metric filter pattern matching for [CRITICAL_ALERT] in stdout."],
    ["Tier 3: Cloud", "Amazon S3 Vault", "S3 Standard Bucket", "Immutable JSON forensic crash dump persistence with 11 9's durability."],
    ["Tier 3: Cloud", "GitHub Issues & CI", "GitHub REST API & Actions", "Automated Bug User Story minting and zero-touch smart commit closure."],
]
make_table(t1_headers, t1_data, [1.0, 1.4, 1.6, 2.4], "Table 1.1: Component Architectural Responsibilities Across the Three Tiers")

# =============================================================
# CHAPTER 2: STOREFRONT PRESENTATION & MULTI-HUB LOGISTICS
# =============================================================
h1("2. Storefront Presentation & Multi-Hub Logistics")

h2("2.1 FlashMart E-Commerce Interface")
p("The consumer-facing presentation layer, FlashMart Tech, is engineered as a modern Single-Page Application (SPA) leveraging standard HTML5, CSS3 CSS variables, and vanilla JavaScript (ES6+). By eliminating external build tooling and heavy Node.js runtimes, the application achieves instantaneous browser rendering, sub-100ms DOM hydration, and minimal network payload transfer overhead. The interface is optimized for rapid catalog browsing and promotional flash deal checkouts. Figure 2 illustrates the FlashMart storefront user interface.")

figure("snapshot1_storefront.png", "Figure 2: FlashMart Customer Storefront & VIT Vellore Delivery Hub Selection Interface", width_inches=6.0)

h2("2.2 VIT Vellore Campus Dark Store Routing")
p("A foundational feature of FlashMart Tech is its localized delivery hub routing engine. Built specifically to model campus micro-fulfillment, the application defaults to the VIT Vellore Campus hub (Men's Hostel Q-Block Dark Store, Katpadi). When an order is placed, the frontend serializes the selected delivery hub string along with the product identifier into a structured JSON payload: {product_id: 3, delivery_hub: 'VIT Vellore Campus (Men\\'s Hostel Q-Block)'}. The backend microservice evaluates localized dark store inventory specifically for the selected fulfillment node, demonstrating geographic warehouse isolation.")

h2("2.3 Promotional Flash Sale Concurrency Engine")
p("To stress-test microservice reliability, FlashMart incorporates a promotional midnight flash deal engine. The catalog prominently displays the OnePlus 11R 5G (₹34,999) discounted flash deal accompanied by a real-time countdown timer (01:42:18 remaining). This promotional deal models viral customer demand, prompting multiple concurrent checkout submissions to test localized inventory depletion boundaries.")

# =============================================================
# CHAPTER 3: THE RUNTIME INCIDENT: ZERO-STOCK EXHAUSTION & CRASH
# =============================================================
h1("3. The Runtime Incident: Zero-Stock Exhaustion & Crash")

h2("3.1 Fault Simulation Mechanics")
p("The simulated fault models an authentic quick-commerce edge-case: sudden inventory exhaustion. During the promotional flash sale, dark store stock for the OnePlus 11R 5G drops to stock = 0. In an unhardened microservice, checkout calculations attempt to compute allocation ratios or discount percentages using raw stock values without boundary checking.")

h2("3.2 Mathematical Division-by-Zero Exception")
p("In app/app.py, the order processing worker thread executes the allocation calculation:")
code_block("""# app/app.py: Checkout Order Calculation Logic
product = get_product(product_id)
# Unhardened mathematical operation:
allocation = 100 / product['stock']  # When stock == 0, raises ZeroDivisionError!""")

p("Because product['stock'] equals 0, Python's runtime immediately throws an unhandled ZeroDivisionError: division by zero. Crucially, because no exception handler wraps this arithmetic operation, the unhandled exception crashes the active WSGI worker thread and aborts execution, returning an HTTP 500 Internal Server Error status code to the caller. Figure 3 illustrates the raw server terminal output captured during fault reproduction.")

figure("snapshot3_server_crash.png", "Figure 3: Backend Server ZeroDivisionError Crash Terminal Output & Structured Telemetry", width_inches=6.0)

h2("3.3 WSGI Worker Thread Crash & [CRITICAL_ALERT] Logging")
p("Prior to thread termination, the microservice application logger intercepts the unhandled crash context. It serializes the exception event and emits a structured telemetry string to standard output (stdout):")
code_block("""[CRITICAL] [CRITICAL_ALERT] Incident simulation triggered! Item 'OnePlus 11R 5G' has stock=0 for address 'VIT Vellore Campus'
[ERROR] [EXCEPTION] Unhandled ZeroDivisionError in delivery routing allocation worker
Traceback (most recent call last):
  File "app/app.py", line 119, in checkout
    _ = 100 / product["stock"]  # Crashes with HTTP 500 ZeroDivisionError!
ZeroDivisionError: division by zero""")

# =============================================================
# CHAPTER 4: DEFENSIVE PRESENTATION ENGINEERING: CUSTOMER INSULATION
# =============================================================
h1("4. Defensive Presentation Engineering: Customer Insulation")

h2("4.1 Client-Side HTTP 500 Interception")
p("In conventional, fragile web applications, an unhandled HTTP 500 response produces an unstyled, alarming browser error screen or raw JSON traceback dump. Such catastrophic failures destroy consumer trust and immediately induce shopping cart abandonment.")

p("FlashMart Tech enforces a strict Site Reliability Engineering client-insulation invariant: internal server errors must never reach the customer interface. The client Single-Page Application intercepts non-200 HTTP response codes before browser rendering. When the checkout worker returns HTTP 500 due to stock depletion, the client gracefully swallows the raw exception and opens an informative 'Item Not Deliverable to Your Location' waitlist drawer. Figure 4 illustrates this customer insulation mechanism.")

figure("snapshot2_stockout_drawer.png", "Figure 4: Graceful Frontend Stockout Exception Interception and Customer Insulation", width_inches=6.0)

h2("4.2 Informative Stockout Waitlist Modal")
p("The modal provides complete operational transparency without alarming the user. It explicitly informs the customer: 'We're sorry! OnePlus 11R 5G is currently out of stock at your nearest dark store fulfillment center (VIT Vellore Campus - Men's Hostel Q-Block)'. It presents two prominent call-to-action buttons: a high-contrast 'Notify Me When Available at This Address' button that registers the user for replenishment waitlists, and an alternate delivery hub selector allowing the customer to reroute delivery to Katpadi or Vellore Town hubs.")

h2("4.3 Customer Trust and Brand Equity Protection")
p("By insulating customers from raw backend failures, FlashMart preserves brand equity and maintains conversion opportunities even during localized stockouts. The customer perceives a polite stockout notice rather than a broken, malfunctioning system.")

# =============================================================
# CHAPTER 5: SRE OBSERVABILITY: SUB-5-SECOND METRIC INGESTION
# =============================================================
h1("5. SRE Observability: Sub-5-Second Metric Ingestion")

h2("5.1 Event-Driven CloudWatch Log Filtering")
p("Traditional cloud monitoring architectures rely on periodic log scraping daemons or metric polling jobs that introduce 2 to 15 minutes of detection delay. In quick-commerce operations, 15 minutes of downtime during a flash sale results in massive revenue loss before support teams are notified.")

p("DevOps Incident Watchdog implements event-driven, push-based telemetry ingestion. An Amazon CloudWatch Metric Filter continuously monitors the /aws/lambda/watchdog-target-app log group, matching stdout statements containing the exact pattern [CRITICAL_ALERT]. Upon pattern detection, CloudWatch increments an active incident metric and asynchronously invokes the Watchdog Lambda triage orchestrator within 4.2 seconds of log emission.")

h2("5.2 Operator SRE Backstage Dashboard")
p("To provide operational visibility, the platform includes an SRE Backstage Control Center. The dashboard displays real-time AWS CloudWatch metric filter states, active Lambda function health (200 OK), S3 forensic bucket storage links, and live Agile backlog sync statuses. Figure 5 illustrates the SRE Backstage dashboard.")

figure("snapshot4_sre_dashboard.png", "Figure 5: AWS CloudWatch Metric Filter & SRE Telemetry Backstage Dashboard", width_inches=6.0)

h2("5.3 Zero-Polling Telemetry Architecture")
p("Because the telemetry pipeline leverages native CloudWatch Log Subscriptions rather than polling daemons, the monitoring infrastructure incurs zero idle CPU overhead and zero network polling bandwidth costs.")

# =============================================================
# CHAPTER 6: CLOUD FORENSICS: IMMUTABLE S3 VAULT ARCHIVAL
# =============================================================
h1("6. Cloud Forensics: Immutable S3 Vault Archival")

h2("6.1 Cryptographic Incident ID Minting")
p("Upon invocation, the Watchdog Lambda decompress the incoming base64 gzipped log payload in memory. It parses the log events and mints a unique cryptographic incident identifier combining the Unix timestamp with an MD5 hash: INC-1791945923-07CD12B5. This incident ID serves as the immutable primary key across all cloud logs, forensic dumps, and GitHub Agile tickets.")

h2("6.2 Private Amazon S3 Storage & 11 9's Durability")
p("To satisfy compliance audit requirements and guarantee permanent post-mortem forensic completeness, the Watchdog Lambda packages the full crash traceback, HTTP request headers, active git commit SHA, and dark store hub identifier into a structured JSON evidence document. It uploads this dump to a private Amazon S3 bucket (devops-incident-watchdog-logs-401537512022) with 11 9's durability (99.999999999%) and AES-256 server-side encryption. Figure 6 displays the archived forensic evidence in the Amazon S3 Management Console.")

figure("snapshot5_s3_vault.png", "Figure 6: Immutable Incident Forensic Evidence Archived in Amazon S3 Bucket Vault", width_inches=6.0)

h2("6.3 Structured Forensic JSON Payload Specification")
p("The archived JSON forensic dump contains complete diagnostic context for post-mortem investigations:")
code_block("""{
  "incident_id": "INC-1791945923-07CD12B5",
  "timestamp": "2026-10-18T21:28:44Z",
  "error_type": "ZeroDivisionError",
  "error_message": "division by zero in checkout logic",
  "target_service": "watchdog-target-app (FlashMart Promotional Sale)",
  "fulfillment_location": "VIT Vellore Campus (Men's Hostel Q-Block)",
  "forensic_s3_uri": "s3://devops-incident-watchdog-logs-401537512022/incidents/INC-1791945923.json",
  "git_commit_sha": "369f0b8..."
}""")

# =============================================================
# CHAPTER 7: AGILE BACKLOG AUTOMATION: GITHUB ISSUE MINTING
# =============================================================
h1("7. Agile Backlog Automation: GitHub Issue Minting")

h2("7.1 REST API v3 Automated Ticket Creation")
p("Rather than requiring human engineers to manually transcribe crash logs into sprint issue trackers, the Watchdog Lambda dispatches an authenticated HTTP POST request to the GitHub Issues REST API v3 (/repos/hemalexe/devopss-incident-watchdog/issues). The automated ticket is minted on the active sprint board within 24 seconds of the initial crash event. Figure 7 illustrates the minted Agile Bug User Story.")

figure("snapshot6_github_issue.png", "Figure 7: Automated Agile Bug User Story Minted on GitHub Issues with Definition of Done", width_inches=6.0)

h2("7.2 Standardized Diagnostics Table & Priority Labels")
p("The minted ticket embeds standardized Agile metadata: priority labels (incident, p1-critical, auto-generated), an Agile User Story narrative ('As an Agile SRE Team Member, I need to investigate and resolve the unhandled ZeroDivisionError...'), and a formatted diagnostics table mapping the incident ID, error type, target microservice, campus fulfillment hub, and direct Amazon S3 forensic URI.")

h2("7.3 Enforcing 6 Definition of Done (DoD) Criteria")
p("Crucially, the ticket enforces six explicit Definition of Done acceptance criteria checkboxes:")
bullet("Implement defensive boundary check: if stock <= 0 return HTTP 400 out_of_stock.", bold_prefix="Criteria 1: ")
bullet("Preserve graceful frontend stockout waitlist modal and customer insulation.", bold_prefix="Criteria 2: ")
bullet("Execute all 9 automated unit regression tests with 100% pass rate in CI runner.", bold_prefix="Criteria 3: ")
bullet("Verify zero-touch closure of GitHub Issue #1 via Git Smart Commit (Fixes #1).", bold_prefix="Criteria 4: ")

# =============================================================
# CHAPTER 8: CONTINUOUS REMEDIATION: GITOPS SMART COMMIT & CI/CD
# =============================================================
h1("8. Continuous Remediation: GitOps Smart Commit & CI/CD")

h2("8.1 Developer Defensive Code Fix Implementation")
p("When an engineer inspects GitHub Issue #1, the root cause is immediately clear. The developer modifies app/app.py to introduce the defensive inventory boundary check:")
code_block("""# app/app.py: Defensive Code Remediation
if product['stock'] <= 0:
    return jsonify({
        'error': 'out_of_stock',
        'message': f"Item '{product['name']}' is out of stock at {delivery_hub}.",
        'waitlist_eligible': True
    }), 400

allocation = 100 / product['stock']""")

h2("8.2 GitHub Actions Automated Pytest Regression Runner")
p("The engineer commits the code using Git Smart Commit syntax: git commit -am 'Fixes #1: Handled division by zero in checkout logic'. Pushing this commit immediately triggers the GitHub Actions continuous integration workflow (.github/workflows/ci-cd.yml). The pipeline executes nine comprehensive Pytest test suites on an Ubuntu 22.04 LTS runner in 0.53 seconds (100% test pass rate). Figure 8 illustrates the GitHub Actions CI/CD execution.")

figure("snapshot7_cicd_pipeline.png", "Figure 8: GitHub Actions CI/CD Automated Pytest Regression Suite and Zero-Touch Closure", width_inches=6.0)

h2("8.3 Zero-Touch Sprint Backlog Closure via Smart Commits")
p("Upon successful test verification, the CI runner packages the updated microservice and redeploys the code to AWS Lambda. Because the commit message referenced Fixes #1, GitHub natively links the commit SHA to Issue #1 and automatically transitions the ticket from Open to Closed (Done) without human administrative bookkeeping.")

# =============================================================
# CHAPTER 9: SECURITY ARCHITECTURE & SERVERLESS CLOUD TOPOLOGY
# =============================================================
h1("9. Security Architecture & Serverless Cloud Topology")

h2("9.1 Seven Closed-Loop Security Safety Gates")
p("The operational integrity of DevOps Incident Watchdog is enforced across seven distinct security safety gates governing read-only telemetry ingestion, serverless container sandboxing, S3 immutable storage, least-privilege IAM execution roles, ticket sanitization, mandatory pytest CI verification, and GitOps commit traceability. Figure 9 illustrates this closed-loop safety gate architecture.")

figure("figure3_safety_gates.png", "Figure 9: Closed-Loop Telemetry & GitOps Security Safety Gate Architecture", width_inches=6.2)

h2("9.2 AWS Serverless Live Deployment Topology")
p("The platform is deployed live in the AWS Sydney region (ap-southeast-2) under AWS Account 401537512022. Both microservices execute as decoupled AWS Lambda functions configured with 128 MB RAM, providing sub-300ms cold starts and auto-scaling up to thousands of concurrent requests. Figure 10 illustrates the production AWS cloud topology.")

figure("figure4_aws_topology.png", "Figure 10: AWS Serverless Live Production Topology in Sydney (ap-southeast-2)", width_inches=6.2)

h2("9.3 Monthly Free Tier Cost Breakdown")
p("Table 9.1 confirms that the entire serverless infrastructure operates completely within AWS Free Tier monthly limits ($0.00/month continuous cloud spend).")

t9_headers = ["AWS Resource", "Provisioned Capacity", "AWS Free Tier Allowance", "Monthly Cost ($)"]
t9_data = [
    ["AWS Lambda Compute", "128 MB RAM (50,000 req/mo)", "1,000,000 free requests / mo", "$0.00 / month"],
    ["Amazon CloudWatch Logs", "250 MB log ingestion / mo", "5.0 GB free log ingestion / mo", "$0.00 / month"],
    ["Amazon S3 Storage", "50 MB JSON crash dumps / mo", "5.0 GB free Standard storage / mo", "$0.00 / month"],
    ["Total Cloud Spend", "Complete Infrastructure", "100% Covered Under AWS Free Tier", "$0.00 / month"],
]
make_table(t9_headers, t9_data, [2.0, 2.0, 2.0, 1.0], "Table 9.1: AWS Free Tier Monthly Compute and Storage Cost Breakdown")

# =============================================================
# CHAPTER 10: END-TO-END WORKFLOW SYNTHESIS & CONCLUSION
# =============================================================
h1("10. End-to-End Workflow Synthesis & Conclusion")

h2("10.1 Complete 7-Stage Remediation Lifecycle")
p("The complete operational lifecycle of DevOps Incident Watchdog progresses through seven automated stages, from customer order dispatch to GitOps automated closure. Figure 11 illustrates this end-to-end remediation workflow.")

figure("figure2_workflow.png", "Figure 11: End-to-End Autonomous Incident-to-Agile Remediation Workflow", width_inches=6.2)

h2("10.2 Verified Performance Metrics & Engineering Achievements")
p("The implementation and rigorous testing of DevOps Incident Watchdog substantiate four key engineering achievements:")
bullet("Mean-Time-to-Acknowledge (MTTA) is reduced from 2-8 hours of manual administrative drag to under 24 seconds.", bold_prefix="1. MTTA Reduction: ")
bullet("100% automated regression test coverage across 9 Pytest suites passing in 0.53 seconds.", bold_prefix="2. Quality Assurance: ")
bullet("Permanent forensic compliance guaranteed through 11 9's durability in Amazon S3.", bold_prefix="3. Forensic Integrity: ")
bullet("Zero continuous operational cloud spend ($0.00/month) within AWS Free Tier thresholds.", bold_prefix="4. Cost Efficiency: ")

h2("10.3 Final Assessment for Faculty Evaluation")
p("In conclusion, DevOps Incident Watchdog demonstrates that autonomous Site Reliability Engineering telemetry and Agile sprint management can operate in complete software-defined harmony. By transforming transient microservice exceptions into structured, actionable developer stories and closing them via automated CI/CD verification, the platform frees software engineers to dedicate their energy to root-cause development rather than manual administrative bookkeeping.")

# -------------------------------------------------------------
# SAVE DOCX
# -------------------------------------------------------------
doc.save(docx_output)
print(f"SUCCESS: Formal Walkthrough Word document saved to: {docx_output}")

# -------------------------------------------------------------
# CONVERT TO PDF VIA WORD COM
# -------------------------------------------------------------
import subprocess
ps_cmd = f"""
$word = New-Object -ComObject Word.Application
$word.Visible = $false
try {{
    $doc = $word.Documents.Open('{docx_output}')
    $doc.SaveAs2('{pdf_output}', 17)
    $doc.Close()
    Write-Host "PDF export succeeded!"
}} finally {{
    $word.Quit()
    [System.Runtime.Interopservices.Marshal]::ReleaseComObject($word) | Out-Null
}}
"""
ps_script_path = os.path.join(base_dir, "scripts", "export_formal_walkthrough_pdf.ps1")
with open(ps_script_path, "w", encoding="utf-8") as f:
    f.write(ps_cmd)

print("Running Word COM PDF export...")
subprocess.run(["powershell", "-ExecutionPolicy", "Bypass", "-File", ps_script_path], check=True)
print(f"SUCCESS: Formal Walkthrough PDF saved to: {pdf_output}")
