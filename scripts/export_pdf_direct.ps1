
$word = New-Object -ComObject Word.Application
$word.Visible = $false
try {
    $doc = $word.Documents.Open('C:\Users\Sailaja C\Documents\New folder\DevOps-Incident-Watchdog\DevOps_Incident_Watchdog_Project_Report.docx')
    $doc.SaveAs2('C:\Users\Sailaja C\Documents\New folder\DevOps-Incident-Watchdog\DevOps_Incident_Watchdog_Project_Report.pdf', 17)
    $doc.Close()
    Write-Host "PDF export succeeded!"
} finally {
    $word.Quit()
    [System.Runtime.Interopservices.Marshal]::ReleaseComObject($word) | Out-Null
}
