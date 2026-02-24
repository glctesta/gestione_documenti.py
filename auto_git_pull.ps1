# auto_git_pull.ps1
# Esegue automaticamente git pull per sincronizzare il repository locale con GitHub

$gitExe = "C:\Program Files\Git\bin\git.exe"
$repoPath = "C:\Users\User\PythonProjetcs\Python\PrductionDocumentation"
$logFile = "$repoPath\git_pull.log"

$timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"

try {
    Set-Location $repoPath
    $output = & $gitExe pull 2>&1
    Add-Content -Path $logFile -Value "[$timestamp] $output"
} catch {
    Add-Content -Path $logFile -Value "[$timestamp] ERRORE: $_"
}
