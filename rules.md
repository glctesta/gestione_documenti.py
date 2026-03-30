After finishing PyInstaller compilation, always sign the EXE files:

```powershell
signtool.exe sign /sha1 "a21358bd1e887cef30c0ae40c7e8b9c885b833b3" /fd SHA256 /tr http://time.certum.pl /td sha256 /v "C:\Users\gtesta\PythonProjetcs\Python\PrductionDocumentation\dist\DocumentManagement\DocumentManagement.exe" "C:\Users\gtesta\PythonProjetcs\Python\PrductionDocumentation\dist\DocumentManagement\_internal\updater.exe"
```
