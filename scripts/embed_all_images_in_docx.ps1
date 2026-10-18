$htmlPath = "C:\Users\Sailaja C\Documents\New folder\DevOps-Incident-Watchdog\PROJECT_REPORT_FOR_WORD.html"
$docxPath = "C:\Users\Sailaja C\Documents\New folder\DevOps-Incident-Watchdog\DevOps_Incident_Watchdog_Project_Report.docx"
$pdfPath  = "C:\Users\Sailaja C\Documents\New folder\DevOps-Incident-Watchdog\DevOps_Incident_Watchdog_Project_Report.pdf"
$baseDir  = "C:\Users\Sailaja C\Documents\New folder\DevOps-Incident-Watchdog"

$imageFiles = @(
    "architecture_diagram.png",
    "figure2_workflow.png",
    "figure3_safety_gates.png",
    "figure4_aws_topology.png",
    "snapshot1_storefront.png",
    "snapshot2_stockout_drawer.png",
    "snapshot3_server_crash.png",
    "snapshot4_sre_dashboard.png",
    "snapshot5_s3_vault.png",
    "snapshot6_github_issue.png",
    "snapshot7_cicd_pipeline.png"
)

# Max heights in points (1 inch = 72 pt)
# Fig 1 (Arch): 200 pt
# Fig 2, 3, 4: 95 pt
# Fig 5-11 (Snapshots): 120 pt
$maxHeights = @(
    200,
    95,
    95,
    95,
    120,
    120,
    120,
    120,
    120,
    120,
    120
)

Write-Host "Starting Word Application..."
$word = New-Object -ComObject Word.Application
$word.Visible = $false

try {
    Write-Host "Opening HTML file: $htmlPath"
    $doc = $word.Documents.Open($htmlPath)
    
    $shapeCount = $doc.InlineShapes.Count
    Write-Host "Detected $shapeCount shapes in HTML import."
    
    # Iterate backwards so deleting/inserting doesn't shift earlier indices
    for ($i = $shapeCount; $i -ge 1; $i--) {
        $idx = $i - 1 # 0-based index
        $imgName = $imageFiles[$idx]
        $fullPath = Join-Path $baseDir $imgName
        $maxH = $maxHeights[$idx]
        
        Write-Host "Embedding Image $i ($imgName) from: $fullPath"
        
        $oldShape = $doc.InlineShapes.Item($i)
        $range = $oldShape.Range
        $oldShape.Delete()
        
        # AddPicture(FileName, LinkToFile, SaveWithDocument, Range)
        $newShape = $doc.InlineShapes.AddPicture($fullPath, $false, $true, $range)
        
        # Scale to fit page height constraints
        $origH = $newShape.Height
        $origW = $newShape.Width
        if ($origH -gt $maxH) {
            $ratio = $maxH / $origH
            $newShape.Height = $maxH
            $newShape.Width = [math]::Round($origW * $ratio)
        }
        # Center the shape paragraph
        $newShape.Range.ParagraphFormat.Alignment = 1 # wdAlignParagraphCenter
        
        Write-Host "Image $i successfully embedded into docx package! (Size: $($newShape.Width)x$($newShape.Height))"
    }
    
    Write-Host "Saving standalone DOCX with all images embedded: $docxPath"
    $doc.SaveAs2($docxPath, 16)
    
    Write-Host "Exporting to PDF: $pdfPath"
    $doc.SaveAs2($pdfPath, 17)
    
    $doc.Close()
    Write-Host "SUCCESS: Standalone Word document and PDF generated with all images physically embedded!"
} catch {
    Write-Host "ERROR: $_"
} finally {
    $word.Quit()
    [System.Runtime.Interopservices.Marshal]::ReleaseComObject($word) | Out-Null
}
