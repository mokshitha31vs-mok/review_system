# ==============================================================================
# Helper Script to Launch Port-Forwarding for Review System V1, V2, and V3
# ==============================================================================

Write-Host "==========================================================" -ForegroundColor Cyan
Write-Host " Starting Kubernetes Port-Forwarding for Review System     " -ForegroundColor Cyan
Write-Host "==========================================================" -ForegroundColor Cyan

# Terminate existing kubectl port-forward processes to avoid port conflicts
Get-Process kubectl -ErrorAction SilentlyContinue | Where-Object { $_.CommandLine -like "*port-forward*" } | Stop-Process -Force -ErrorAction SilentlyContinue

Write-Host "Launching port-forward for Version 1 on port 18081..." -ForegroundColor Yellow
Start-Process kubectl -ArgumentList "port-forward", "service/review-system-v1-service", "18081:5000" -WindowStyle Minimized

Write-Host "Launching port-forward for Version 2 on port 18082..." -ForegroundColor Yellow
Start-Process kubectl -ArgumentList "port-forward", "service/review-system-v2-service", "18082:5000" -WindowStyle Minimized

Write-Host "Launching port-forward for Version 3 on port 18083..." -ForegroundColor Yellow
Start-Process kubectl -ArgumentList "port-forward", "service/review-system-v3-service", "18083:5000" -WindowStyle Minimized

Start-Sleep -Seconds 3

Write-Host ""
Write-Host "All port-forwards are now RUNNING in the background!" -ForegroundColor Green
Write-Host "Open the following URLs in your web browser:" -ForegroundColor White
Write-Host "  - Version 1 (Classic Blue):    http://localhost:18081" -ForegroundColor Cyan
Write-Host "  - Version 2 (Modern Emerald):  http://localhost:18082" -ForegroundColor Green
Write-Host "  - Version 3 (Royal Purple):    http://localhost:18083" -ForegroundColor Magenta
Write-Host ""
Write-Host "Health endpoints:" -ForegroundColor White
Write-Host "  - V1 Health: http://localhost:18081/health"
Write-Host "  - V2 Health: http://localhost:18082/health"
Write-Host "  - V3 Health: http://localhost:18083/health"
Write-Host "==========================================================" -ForegroundColor Cyan
