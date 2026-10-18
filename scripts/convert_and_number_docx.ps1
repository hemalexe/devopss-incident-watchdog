$htmlPath = "C:\Users\Sailaja C\Documents\New folder\DevOps-Incident-Watchdog\PROJECT_REPORT_FOR_WORD.html"
$docxPath = "C:\Users\Sailaja C\Documents\New folder\DevOps-Incident-Watchdog\DevOps_Incident_Watchdog_Project_Report.docx"
$pdfPath  = "C:\Users\Sailaja C\Documents\New folder\DevOps-Incident-Watchdog\DevOps_Incident_Watchdog_Project_Report.pdf"

Write-Host "Starting Word COM Application..."
$word = New-Object -ComObject Word.Application
$word.Visible = $false

try {
    Write-Host "Opening HTML source file: $htmlPath"
    $doc = $word.Documents.Open($htmlPath)
    
    # 1. Embed all linked shapes
    $count = $doc.InlineShapes.Count
    Write-Host "Embedding $count images into document..."
    for ($i = 1; $i -le $count; $i++) {
        $shape = $doc.InlineShapes.Item($i)
        try {
            if ($shape.LinkFormat) {
                $shape.LinkFormat.SavePictureWithDocument = $true
                $shape.LinkFormat.BreakLink()
            }
        } catch {
            Write-Host "Note on image ${i}: $_"
        }
    }
    
    # 2. Configure Professional Running Headers and Footers with Page Numbers
    Write-Host "Configuring Academic Running Headers & Footers..."
    $section = $doc.Sections.Item(1)
    $section.PageSetup.DifferentFirstPageHeaderFooter = $true
    
    # Running Header (Top)
    $header = $section.Headers.Item(1)
    $header.Range.Text = "Auto-Incident to Agile Ticket Pipeline (DevOps Incident Watchdog) • S Hemal (24MIS0050)"
    $header.Range.Font.Name = "Times New Roman"
    $header.Range.Font.Size = 8.5
    $header.Range.Font.Italic = $true
    $header.Range.ParagraphFormat.Alignment = 2 # Right align
    
    # Running Footer with Page Numbers (Bottom)
    $footer = $section.Footers.Item(1)
    $footer.Range.Text = "VIT Vellore Campus • Agile Development Process & DevOps     |     Page "
    $footer.Range.Font.Name = "Times New Roman"
    $footer.Range.Font.Size = 9.0
    $footer.Range.ParagraphFormat.Alignment = 2 # Right align
    
    # Add Page Number field (wdFieldPage = 33)
    $range = $footer.Range
    $range.Collapse(0) # Collapse to end
    $doc.Fields.Add($range, 33) | Out-Null
    
    $range = $footer.Range
    $range.Collapse(0)
    $range.InsertAfter(" of ")
    $range.Collapse(0)
    $doc.Fields.Add($range, 26) | Out-Null # wdFieldNumPages = 26
    
    # Update all fields in document
    $doc.Fields.Update() | Out-Null
    
    # 3. Save as standalone DOCX
    Write-Host "Saving Word Document: $docxPath"
    $doc.SaveAs2($docxPath, 16)
    
    # 4. Export to PDF
    Write-Host "Exporting to PDF: $pdfPath"
    $doc.SaveAs2($pdfPath, 17)
    
    $doc.Close()
    Write-Host "SUCCESS: Generated 26-page DOCX and PDF with embedded page numbering!"
} catch {
    Write-Host "ERROR: $_"
} finally {
    $word.Quit()
    [System.Runtime.Interopservices.Marshal]::ReleaseComObject($word) | Out-Null
}
