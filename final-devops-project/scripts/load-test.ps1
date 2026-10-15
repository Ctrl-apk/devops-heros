# PowerShell load-test script to generate CPU load and demonstrate HPA scaling
param(
    [string]$Url = "http://taskboard.local/api/health",
    [int]$Requests = 500
)

Write-Host "Sending $Requests requests to $Url..." -ForegroundColor Cyan

$success = 0
$failed = 0

for ($i = 1; $i -le $Requests; $i++) {
    try {
        $res = Invoke-WebRequest -Uri $Url -UseBasicParsing -TimeoutSec 2
        if ($res.StatusCode -eq 200) { $success++ } else { $failed++ }
    } catch {
        $failed++
    }

    if ($i % 50 -eq 0) {
        Write-Host "Progress: $i / $Requests (Success: $success, Failed: $failed)" -ForegroundColor Yellow
    }
}

Write-Host "Load test completed! Total: $Requests, Success: $success, Failed: $failed" -ForegroundColor Green
Write-Host "Check HPA status with: kubectl get hpa -n taskboard -w" -ForegroundColor Cyan
