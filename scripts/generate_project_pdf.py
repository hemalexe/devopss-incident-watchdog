"""
Generates the comprehensive Project Architecture & Process Report PDF
Project: Auto-Incident to Agile Ticket Pipeline (DevOps Incident Watchdog)
Student: S Hemal (24MIS0050)
Course: Agile Development Process and DevOps
"""

import os
import sys
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, KeepTogether, HRFlowable, PageBreak
)
from reportlab.graphics.shapes import Drawing, Rect, String, Line, Polygon, Group
from reportlab.pdfgen import canvas

class NumberedCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        super(NumberedCanvas, self).__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_decorations(num_pages)
            super(NumberedCanvas, self).showPage()
        super(NumberedCanvas, self).save()

    def draw_page_decorations(self, page_count):
        self.saveState()
        self.setFont("Helvetica", 8)
        self.setFillColor(colors.HexColor("#718096"))
        
        # Header (pages 2+)
        if self._pageNumber > 1:
            self.drawString(54, 755, "DevOps Incident Watchdog | Auto-Incident to Agile Ticket Pipeline")
            self.drawRightString(letter[0] - 54, 755, "S Hemal (24MIS0050)")
            self.setStrokeColor(colors.HexColor("#E2E8F0"))
            self.setLineWidth(0.75)
            self.line(54, 747, letter[0] - 54, 747)

        # Footer (all pages)
        self.setStrokeColor(colors.HexColor("#E2E8F0"))
        self.setLineWidth(0.75)
        self.line(54, 45, letter[0] - 54, 45)
        
        self.drawString(54, 32, "Course: Agile Development Process and DevOps | VIT")
        page_text = f"Page {self._pageNumber} of {page_count}"
        self.drawRightString(letter[0] - 54, 32, page_text)
        self.restoreState()


def create_architecture_diagram():
    """Draws a vector system architecture diagram using ReportLab shapes."""
    dwg = Drawing(504, 155)
    
    # Background card
    dwg.add(Rect(0, 0, 504, 155, fillColor=colors.HexColor("#F8FAFC"), strokeColor=colors.HexColor("#CBD5E1"), rx=8, ry=8, strokeWidth=1))
    
    # Title
    dwg.add(String(15, 138, "END-TO-END SYSTEM & INCIDENT ARCHITECTURE", fontName="Helvetica-Bold", fontSize=9, fillColor=colors.HexColor("#1E293B")))
    
    # 1. Target Web Store
    dwg.add(Rect(15, 68, 85, 52, fillColor=colors.HexColor("#EFF6FF"), strokeColor=colors.HexColor("#3B82F6"), rx=5, ry=5, strokeWidth=1.5))
    dwg.add(String(23, 103, "Target Web App", fontName="Helvetica-Bold", fontSize=7.5, fillColor=colors.HexColor("#1D4ED8")))
    dwg.add(String(22, 90, "Flask / AWS Lambda", fontName="Helvetica", fontSize=6.5, fillColor=colors.HexColor("#475569")))
    dwg.add(String(22, 78, "Port 5000 / Function URL", fontName="Helvetica-Oblique", fontSize=6, fillColor=colors.HexColor("#64748B")))
    
    # Arrow 1 -> CloudWatch
    dwg.add(Line(100, 94, 115, 94, strokeColor=colors.HexColor("#EF4444"), strokeWidth=1.5))
    dwg.add(Polygon([115, 97, 120, 94, 115, 91], fillColor=colors.HexColor("#EF4444"), strokeColor=colors.HexColor("#EF4444")))
    dwg.add(String(100, 100, "500 Error", fontName="Helvetica-Bold", fontSize=5.5, fillColor=colors.HexColor("#DC2626")))

    # 2. CloudWatch Monitoring
    dwg.add(Rect(120, 68, 80, 52, fillColor=colors.HexColor("#FEF2F2"), strokeColor=colors.HexColor("#EF4444"), rx=5, ry=5, strokeWidth=1.5))
    dwg.add(String(125, 103, "AWS CloudWatch", fontName="Helvetica-Bold", fontSize=7.5, fillColor=colors.HexColor("#B91C1C")))
    dwg.add(String(125, 90, "Log Subscription Filter", fontName="Helvetica", fontSize=6.5, fillColor=colors.HexColor("#475569")))
    dwg.add(String(125, 78, "Crash Anomaly Filter", fontName="Helvetica-Oblique", fontSize=6, fillColor=colors.HexColor("#64748B")))

    # Arrow 2 -> Lambda Watchdog
    dwg.add(Line(200, 94, 215, 94, strokeColor=colors.HexColor("#F59E0B"), strokeWidth=1.5))
    dwg.add(Polygon([215, 97, 220, 94, 215, 91], fillColor=colors.HexColor("#F59E0B"), strokeColor=colors.HexColor("#F59E0B")))
    dwg.add(String(202, 100, "Trigger", fontName="Helvetica-Bold", fontSize=5.5, fillColor=colors.HexColor("#D97706")))

    # 3. AWS Lambda Watchdog
    dwg.add(Rect(220, 68, 90, 52, fillColor=colors.HexColor("#FFFBEB"), strokeColor=colors.HexColor("#F59E0B"), rx=5, ry=5, strokeWidth=1.5))
    dwg.add(String(226, 103, "AWS Lambda Watchdog", fontName="Helvetica-Bold", fontSize=7.5, fillColor=colors.HexColor("#B45309")))
    dwg.add(String(226, 90, "Parses Crash Stacktrace", fontName="Helvetica", fontSize=6.5, fillColor=colors.HexColor("#475569")))
    dwg.add(String(226, 78, "Autonomous Triager", fontName="Helvetica-Oblique", fontSize=6, fillColor=colors.HexColor("#64748B")))

    # Split Arrows: Lambda -> S3 & Lambda -> GitHub
    # Branch A: Up to S3
    dwg.add(Line(265, 68, 265, 48, strokeColor=colors.HexColor("#10B981"), strokeWidth=1.5))
    dwg.add(Line(265, 48, 325, 48, strokeColor=colors.HexColor("#10B981"), strokeWidth=1.5))
    dwg.add(Polygon([325, 51, 330, 48, 325, 45], fillColor=colors.HexColor("#10B981"), strokeColor=colors.HexColor("#10B981")))
    dwg.add(String(270, 53, "JSON Dump", fontName="Helvetica-Bold", fontSize=5.5, fillColor=colors.HexColor("#047857")))

    # Branch B: Right to GitHub Issues
    dwg.add(Line(310, 94, 325, 94, strokeColor=colors.HexColor("#6366F1"), strokeWidth=1.5))
    dwg.add(Polygon([325, 97, 330, 94, 325, 91], fillColor=colors.HexColor("#6366F1"), strokeColor=colors.HexColor("#6366F1")))
    dwg.add(String(312, 100, "REST API", fontName="Helvetica-Bold", fontSize=5.5, fillColor=colors.HexColor("#4338CA")))

    # 4. Amazon S3 Bucket
    dwg.add(Rect(330, 22, 90, 44, fillColor=colors.HexColor("#ECFDF5"), strokeColor=colors.HexColor("#10B981"), rx=5, ry=5, strokeWidth=1.5))
    dwg.add(String(336, 52, "Amazon S3 Bucket", fontName="Helvetica-Bold", fontSize=7.5, fillColor=colors.HexColor("#047857")))
    dwg.add(String(336, 40, "Private Audit Log Archive", fontName="Helvetica", fontSize=6.5, fillColor=colors.HexColor("#475569")))
    dwg.add(String(336, 30, "INC-*.json (Forensics)", fontName="Helvetica-Oblique", fontSize=6, fillColor=colors.HexColor("#64748B")))

    # 5. GitHub Issues
    dwg.add(Rect(330, 72, 90, 48, fillColor=colors.HexColor("#EEF2FF"), strokeColor=colors.HexColor("#6366F1"), rx=5, ry=5, strokeWidth=1.5))
    dwg.add(String(336, 105, "GitHub Issues Board", fontName="Helvetica-Bold", fontSize=7.5, fillColor=colors.HexColor("#4338CA")))
    dwg.add(String(336, 93, "Agile Bug User Story", fontName="Helvetica", fontSize=6.5, fillColor=colors.HexColor("#475569")))
    dwg.add(String(336, 81, "Acceptance Criteria List", fontName="Helvetica-Oblique", fontSize=6, fillColor=colors.HexColor("#64748B")))

    # Arrow GitHub Issues -> GitHub Actions
    dwg.add(Line(420, 96, 432, 96, strokeColor=colors.HexColor("#8B5CF6"), strokeWidth=1.5))
    dwg.add(Polygon([432, 99, 437, 96, 432, 93], fillColor=colors.HexColor("#8B5CF6"), strokeColor=colors.HexColor("#8B5CF6")))

    # 6. GitHub Actions CI/CD
    dwg.add(Rect(437, 45, 58, 75, fillColor=colors.HexColor("#FAF5FF"), strokeColor=colors.HexColor("#8B5CF6"), rx=5, ry=5, strokeWidth=1.5))
    dwg.add(String(441, 107, "CI/CD Pipeline", fontName="Helvetica-Bold", fontSize=7, fillColor=colors.HexColor("#6D28D9")))
    dwg.add(String(441, 95, "GitHub Actions", fontName="Helvetica-Bold", fontSize=6.5, fillColor=colors.HexColor("#7C3AED")))
    dwg.add(String(441, 82, "1. Pytest Unit", fontName="Helvetica", fontSize=6, fillColor=colors.HexColor("#475569")))
    dwg.add(String(441, 71, "2. Deploy AWS", fontName="Helvetica", fontSize=6, fillColor=colors.HexColor("#475569")))
    dwg.add(String(441, 60, "3. Auto-Close", fontName="Helvetica", fontSize=6, fillColor=colors.HexColor("#475569")))
    dwg.add(String(441, 50, "'Fixes #1'", fontName="Helvetica-Bold", fontSize=6, fillColor=colors.HexColor("#059669")))

    # Feedback loop line from CI/CD back to Target Web App
    dwg.add(Line(466, 45, 466, 10, strokeColor=colors.HexColor("#059669"), strokeWidth=1.2, strokeDashArray=[3, 2]))
    dwg.add(Line(466, 10, 57, 10, strokeColor=colors.HexColor("#059669"), strokeWidth=1.2, strokeDashArray=[3, 2]))
    dwg.add(Line(57, 10, 57, 68, strokeColor=colors.HexColor("#059669"), strokeWidth=1.2, strokeDashArray=[3, 2]))
    dwg.add(Polygon([54, 63, 57, 68, 60, 63], fillColor=colors.HexColor("#059669"), strokeColor=colors.HexColor("#059669")))
    dwg.add(String(160, 14, "Automated Continuous Deployment (Zero-Downtime Patch Deployed)", fontName="Helvetica-Bold", fontSize=6.5, fillColor=colors.HexColor("#047857")))

    return dwg


def generate_pdf(output_path):
    doc = SimpleDocTemplate(
        output_path,
        pagesize=letter,
        leftMargin=54,
        rightMargin=54,
        topMargin=54,
        bottomMargin=54
    )
    
    styles = getSampleStyleSheet()
    
    # Custom styles
    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Heading1'],
        fontName='Helvetica-Bold',
        fontSize=20,
        leading=24,
        textColor=colors.HexColor("#0F172A"),
        spaceAfter=4
    )
    
    subtitle_style = ParagraphStyle(
        'DocSubtitle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=11,
        leading=14,
        textColor=colors.HexColor("#2563EB"),
        spaceAfter=12
    )

    h2_style = ParagraphStyle(
        'Heading2Custom',
        parent=styles['Heading2'],
        fontName='Helvetica-Bold',
        fontSize=12,
        leading=15,
        textColor=colors.HexColor("#1E293B"),
        spaceBefore=10,
        spaceAfter=4
    )

    body_style = ParagraphStyle(
        'BodyCustom',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8.5,
        leading=12,
        textColor=colors.HexColor("#334155"),
        spaceAfter=6
    )

    code_style = ParagraphStyle(
        'CodeStyle',
        parent=styles['Normal'],
        fontName='Courier',
        fontSize=7.5,
        leading=10,
        textColor=colors.HexColor("#0F172A")
    )
    
    callout_style = ParagraphStyle(
        'CalloutText',
        parent=styles['Normal'],
        fontName='Helvetica-Oblique',
        fontSize=8.5,
        leading=12,
        textColor=colors.HexColor("#1E3A8A")
    )

    table_header_style = ParagraphStyle(
        'TableHeader',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=8,
        leading=10,
        textColor=colors.white
    )

    table_cell_style = ParagraphStyle(
        'TableCell',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=7.5,
        leading=10,
        textColor=colors.HexColor("#1E293B")
    )

    story = []

    # Title & Metadata Banner
    story.append(Paragraph("DevOps Incident Watchdog", title_style))
    story.append(Paragraph("Auto-Incident to Agile Ticket Pipeline & Continuous Delivery Architecture", subtitle_style))
    
    meta_data = [
        [
            Paragraph("<b>Student:</b> S Hemal", table_cell_style),
            Paragraph("<b>Reg. No:</b> 24MIS0050", table_cell_style),
            Paragraph("<b>Course:</b> Agile Dev Process & DevOps", table_cell_style),
            Paragraph("<b>AWS Region:</b> ap-southeast-2", table_cell_style)
        ]
    ]
    meta_table = Table(meta_data, colWidths=[110, 110, 170, 114])
    meta_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#F1F5F9")),
        ('BOX', (0,0), (-1,-1), 0.5, colors.HexColor("#CBD5E1")),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor("#E2E8F0")),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('LEFTPADDING', (0,0), (-1,-1), 6),
        ('RIGHTPADDING', (0,0), (-1,-1), 6),
    ]))
    story.append(meta_table)
    story.append(Spacer(1, 10))

    # Executive Summary Box
    summary_html = """<b>Project Essence:</b> An autonomous, closed-loop SRE and Agile pipeline deployed on AWS. When unexpected runtime crashes occur in production (e.g. flash sale inventory depletion causing HTTP 500 errors), AWS CloudWatch and AWS Lambda automatically capture the stack trace, archive the forensic crash dump in Amazon S3, and generate a structured Agile Bug User Story with Acceptance Criteria on the GitHub sprint backlog. Developers commit fixes with smart syntax (<code>Fixes #1</code>), triggering automated unit testing and zero-touch production deployment via GitHub Actions."""
    summary_table = Table([[Paragraph(summary_html, callout_style)]], colWidths=[504])
    summary_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#EFF6FF")),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#93C5FD")),
        ('TOPPADDING', (0,0), (-1,-1), 6),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
        ('LEFTPADDING', (0,0), (-1,-1), 8),
        ('RIGHTPADDING', (0,0), (-1,-1), 8),
    ]))
    story.append(summary_table)
    story.append(Spacer(1, 8))

    # Section 1: Target Application & Simulated Failure
    story.append(Paragraph("1. Target Application & Incident Scenario", h2_style))
    story.append(Paragraph(
        "<b>What application are we using?</b> A production e-commerce retail store (<b>Flask Microservice</b> with zero-dependency WSGI serverless adapter). The catalog features high-demand electronics: Pro Laptop, Noise-Cancelling Headphones, and a <b>Flagship Smartphone</b> set up for a high-traffic flash sale.",
        body_style
    ))
    story.append(Paragraph(
        "<b>The Failure Mechanism:</b> Customers rapidly purchase the promotional smartphone until inventory drops to <code>0</code>. The legacy checkout calculation routine attempts an unhandled order ratio calculation: <code>discount = total / remaining_stock</code>. When <code>remaining_stock == 0</code>, Python raises an unhandled <b><code>ZeroDivisionError: division by zero</code></b>, immediately triggering an <b>HTTP 500 Internal Server Error</b>. In the fixed version, inventory boundary validation returns an <code>HTTP 409 Conflict</code> (Sold Out) without crashing.",
        body_style
    ))
    story.append(Spacer(1, 6))

    # Section 2: Visual Architecture
    story.append(Paragraph("2. Process Architecture & Component Flow", h2_style))
    story.append(create_architecture_diagram())
    story.append(Spacer(1, 8))
    story.append(PageBreak())

    # Section 3: The 7-Step Lifecycle Table ("What All Happens")
    story.append(Paragraph("3. Detailed End-to-End Incident Lifecycle (What All Happens)", h2_style))
    
    lifecycle_data = [
        [
            Paragraph("Phase / Step", table_header_style),
            Paragraph("Component", table_header_style),
            Paragraph("Action & Technical Process", table_header_style),
            Paragraph("Output / Proof", table_header_style)
        ],
        [
            Paragraph("<b>Step 1: Checkout Crash</b>", table_cell_style),
            Paragraph("Flask App / Lambda URL", table_cell_style),
            Paragraph("User orders last smartphone. Stock reaches 0. App raises <code>ZeroDivisionError</code>.", table_cell_style),
            Paragraph("HTTP 500 Server Error<br/>Console log emitted", table_cell_style)
        ],
        [
            Paragraph("<b>Step 2: Log Intercept</b>", table_cell_style),
            Paragraph("AWS CloudWatch", table_cell_style),
            Paragraph("CloudWatch log filter detects pattern <code>[INCIDENT_DETECTED] Type=ZeroDivisionError</code>.", table_cell_style),
            Paragraph("Gzip base64 event payload dispatched", table_cell_style)
        ],
        [
            Paragraph("<b>Step 3: Watchdog Triage</b>", table_cell_style),
            Paragraph("AWS Lambda (Python 3.12)", table_cell_style),
            Paragraph("Extracts error name, timestamp, log group, and 1500-character stack trace.", table_cell_style),
            Paragraph("Generates unique Incident ID (e.g. <code>INC-1791945923</code>)", table_cell_style)
        ],
        [
            Paragraph("<b>Step 4: Forensic Storage</b>", table_cell_style),
            Paragraph("Amazon S3 Bucket", table_cell_style),
            Paragraph("Stores immutable JSON crash dump at <code>s3://devops-...-logs/incidents/YYYY-MM-DD/</code>.", table_cell_style),
            Paragraph("Persistent crash audit file (369 B JSON)", table_cell_style)
        ],
        [
            Paragraph("<b>Step 5: Ticket Creation</b>", table_cell_style),
            Paragraph("GitHub REST API v3", table_cell_style),
            Paragraph("Lambda sends HTTP POST to <code>/repos/.../issues</code> with formatted User Story and Acceptance Criteria.", table_cell_style),
            Paragraph("Agile Ticket created in GitHub Issues (e.g. Issue #1)", table_cell_style)
        ],
        [
            Paragraph("<b>Step 6: CI/CD Pipeline</b>", table_cell_style),
            Paragraph("GitHub Actions", table_cell_style),
            Paragraph("Developer pushes patch with <code>Fixes #1</code>. Runner executes 8 <code>pytest</code> unit tests and builds artifacts.", table_cell_style),
            Paragraph("Green Checkmark (✅ All tests passed)", table_cell_style)
        ],
        [
            Paragraph("<b>Step 7: Zero-Touch Close</b>", table_cell_style),
            Paragraph("Git Smart Commit / AWS", table_cell_style),
            Paragraph("Pipeline updates AWS Lambda runtime with patched code and automatically transitions Agile ticket to <b>Closed / Done</b>.", table_cell_style),
            Paragraph("Live app healthy (200 OK)<br/>Sprint board updated", table_cell_style)
        ]
    ]

    lifecycle_table = Table(lifecycle_data, colWidths=[90, 85, 215, 114])
    lifecycle_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#1E293B")),
        ('ALIGN', (0,0), (-1,-1), 'LEFT'),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor("#F8FAFC")]),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#CBD5E1")),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('LEFTPADDING', (0,0), (-1,-1), 5),
        ('RIGHTPADDING', (0,0), (-1,-1), 5),
    ]))
    story.append(lifecycle_table)
    story.append(Spacer(1, 10))

    # Section 4: Agile User Story Structure
    story.append(Paragraph("4. Agile Backlog Structure & Acceptance Criteria", h2_style))
    story.append(Paragraph(
        "Each ticket generated by the Watchdog strictly follows standard Agile User Story conventions:",
        body_style
    ))
    
    agile_box_content = """<b>Title:</b> [INCIDENT] ZeroDivisionError: division by zero in calculation worker<br/>
<b>Labels:</b> <code>bug</code>, <code>incident</code>, <code>sprint-backlog</code><br/>
<b>User Story:</b> <i>As an Agile Development Team member, I need to resolve runtime failure in <code>/aws/watchdog-target-app</code> so that high system availability is restored and users experience zero disruption.</i><br/>
<b>Acceptance Criteria (Definition of Done):</b><br/>
&bull; Root Cause Analysis (RCA) completed from crash logs archived in Amazon S3.<br/>
&bull; Reproduce bug with automated unit test in <code>tests/test_app.py</code>.<br/>
&bull; Push code fix using smart commit syntax (<code>git commit -m "Fixes #1"</code>).<br/>
&bull; Automated CI/CD pipeline passes all tests and deploys updated application.<br/>
&bull; Health check endpoint (<code>/health</code>) returns HTTP 200 OK."""
    
    agile_table = Table([[Paragraph(agile_box_content, body_style)]], colWidths=[504])
    agile_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#F8FAFC")),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#CBD5E1")),
        ('TOPPADDING', (0,0), (-1,-1), 5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
        ('LEFTPADDING', (0,0), (-1,-1), 8),
        ('RIGHTPADDING', (0,0), (-1,-1), 8),
    ]))
    story.append(agile_table)
    story.append(Spacer(1, 10))

    # Section 5: Faculty Viva Cheat Sheet & Defense Answers
    story.append(Paragraph("5. Faculty Viva Cheat Sheet (Quick Answers for S Hemal)", h2_style))
    
    viva_qa = [
        [
            Paragraph("<b>Question from Professor</b>", table_header_style),
            Paragraph("<b>Recommended High-Scoring Response (What to say)</b>", table_header_style)
        ],
        [
            Paragraph("<b>1. What is the role of Amazon S3?</b>", table_cell_style),
            Paragraph("<i>'Amazon S3 provides private, tamper-proof forensic storage for raw crash dumps and stack traces outside our application server, ensuring compliance and audit traceability.'</i>", table_cell_style)
        ],
        [
            Paragraph("<b>2. How does GitHub get the ticket?</b>", table_cell_style),
            Paragraph("<i>'The AWS Lambda Watchdog executes upon incident detection and calls the GitHub REST API (POST /issues) using a secure token to instantly create the Agile User Story with acceptance criteria.'</i>", table_cell_style)
        ],
        [
            Paragraph("<b>3. What is the Agile connection?</b>", table_cell_style),
            Paragraph("<i>'Instead of manual triage, runtime production defects are automatically mapped directly into sprint backlog user stories with explicit acceptance criteria (Definition of Done).'</i>", table_cell_style)
        ],
        [
            Paragraph("<b>4. How does the ticket close automatically?</b>", table_cell_style),
            Paragraph("<i>'Through GitHub Smart Commits: our developer references <code>Fixes #1</code>. When GitHub Actions passes all tests and deploys, GitHub auto-closes the issue with bidirectional traceability.'</i>", table_cell_style)
        ]
    ]

    viva_table = Table(viva_qa, colWidths=[160, 344])
    viva_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#0F172A")),
        ('ALIGN', (0,0), (-1,-1), 'LEFT'),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor("#F1F5F9")]),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#CBD5E1")),
        ('TOPPADDING', (0,0), (-1,-1), 5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
        ('LEFTPADDING', (0,0), (-1,-1), 6),
        ('RIGHTPADDING', (0,0), (-1,-1), 6),
    ]))
    story.append(viva_table)

    # Build PDF
    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"[SUCCESS] Generated professional project PDF at: {output_path}")

if __name__ == "__main__":
    out_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(out_dir)
    target_file = os.path.join(project_root, "DevOps_Incident_Watchdog_Architecture_Report.pdf")
    generate_pdf(target_file)
