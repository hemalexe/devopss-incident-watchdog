$htmlPath = "C:\Users\Sailaja C\Documents\New folder\DevOps-Incident-Watchdog\PROJECT_REPORT_FOR_WORD.html"
$docxPath = "C:\Users\Sailaja C\Documents\New folder\DevOps-Incident-Watchdog\DevOps_Incident_Watchdog_Project_Report.docx"

Write-Host "Starting Word Application..."
$word = New-Object -ComObject Word.Application
$word.Visible = $false
try {
    Write-Host "Opening HTML file: $htmlPath"
    $doc = $word.Documents.Open($htmlPath)
    
    $count = $doc.InlineShapes.Count
    Write-Host "Detected $count images in document."
    
    for ($i = 1; $i -le $count; $i++) {
        $shape = $doc.InlineShapes.Item($i)
        try {
            if ($shape.LinkFormat) {
                $shape.LinkFormat.SavePictureWithDocument = $true
                $shape.LinkFormat.BreakLink()
                Write-Host "Embedded Image $i into document."
            }
        } catch {
            Write-Host "Note on image ${i}: $_"
        }
    }
    
    Write-Host "Saving as standalone DOCX with all images embedded: $docxPath"
    $doc.SaveAs2($docxPath, 16)
    $doc.Close()
    Write-Host "SUCCESS: Standalone Word document created!"
} catch {
    Write-Host "ERROR during conversion: $_"
} finally {
    $word.Quit()
    [System.Runtime.Interopservices.Marshal]::ReleaseComObject($word) | Out-Null
}
