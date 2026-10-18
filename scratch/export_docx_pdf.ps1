$htmlPath = "C:\Users\Sailaja C\Documents\New folder\DevOps-Incident-Watchdog\PROJECT_REPORT_FOR_WORD.html"
$docxPath = "C:\Users\Sailaja C\Documents\New folder\DevOps-Incident-Watchdog\DevOps_Incident_Watchdog_Project_Report.docx"
$pdfPath  = "C:\Users\Sailaja C\Documents\New folder\DevOps-Incident-Watchdog\DevOps_Incident_Watchdog_Project_Report.pdf"

$word = New-Object -ComObject Word.Application
$word.Visible = $false
try {
    Write-Host "Opening HTML in Word..."
    $doc = $word.Documents.Open($htmlPath)
    
    Write-Host "Saving DOCX..."
    $doc.SaveAs2($docxPath, 16)
    
    Write-Host "Exporting to PDF with all images embedded..."
    $doc.SaveAs2($pdfPath, 17)
    
    $doc.Close()
    Write-Host "SUCCESS: Both DOCX and PDF created!"
} catch {
    Write-Host "Error: $_"
} finally {
    $word.Quit()
    [System.Runtime.Interopservices.Marshal]::ReleaseComObject($word) | Out-Null
}
