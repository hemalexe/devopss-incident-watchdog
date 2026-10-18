$htmlPath = "C:\Users\Sailaja C\Documents\New folder\DevOps-Incident-Watchdog\PROJECT_REPORT_FOR_WORD.html"
$docxPath = "C:\Users\Sailaja C\Documents\New folder\DevOps-Incident-Watchdog\DevOps_Incident_Watchdog_Project_Report.docx"

$word = New-Object -ComObject Word.Application
$word.Visible = $false
try {
    $doc = $word.Documents.Open($htmlPath)
    Write-Host "Initial Fields Count: " $doc.Fields.Count
    
    # Unlink all fields (converts INCLUDEPICTURE to embedded picture bytes)
    for ($i = $doc.Fields.Count; $i -ge 1; $i--) {
        try {
            $doc.Fields.Item($i).Unlink()
        } catch {
            Write-Host "Field unlink error: $_"
        }
    }
    
    Write-Host "Remaining Fields Count: " $doc.Fields.Count
    $doc.SaveAs2($docxPath, 16)
    $doc.Close()
    Write-Host "Document saved successfully!"
} finally {
    $word.Quit()
    [System.Runtime.Interopservices.Marshal]::ReleaseComObject($word) | Out-Null
}
