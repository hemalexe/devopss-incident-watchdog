
 = New-Object -ComObject Word.Application
.Visible = False
 = .Documents.Add()
 = .Selection
.TypeText('Hello World')
 = .InlineShapes.AddPicture('C:\Users\Sailaja C\Documents\New folder\DevOps-Incident-Watchdog\snapshot1_storefront.png', False, True)
.SaveAs2('C:\Users\Sailaja C\Documents\New folder\DevOps-Incident-Watchdog\test_embed.docx', 16)
.Close()
.Quit()
