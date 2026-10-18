$htmlPath = "C:\Users\Sailaja C\Documents\New folder\DevOps-Incident-Watchdog\PROJECT_REPORT_FOR_WORD.html"
$docxPath = "C:\Users\Sailaja C\Documents\New folder\DevOps-Incident-Watchdog\DevOps_Incident_Watchdog_Project_Report.docx"

Write-Host "Starting Word Application..."
$word = New-Object -ComObject Word.Application
$word.Visible = $false
try {
    Write-Host "Opening HTML file: $htmlPath"
    $doc = $word.Documents.Open($htmlPath)
    Write-Host "Saving as DOCX: $docxPath"
    $doc.SaveAs2($docxPath, 16)
    $doc.Close()
    Write-Host "SUCCESS: Document converted and saved to DOCX!"
} catch {
    Write-Host "ERROR during conversion: $_"
} finally {
    $word.Quit()
    [System.Runtime.Interopservices.Marshal]::ReleaseComObject($word) | Out-Null
}
