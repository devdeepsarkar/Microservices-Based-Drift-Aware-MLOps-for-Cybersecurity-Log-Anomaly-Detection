# run.ps1 — Start all services (PowerShell)
# Run with: .\run.ps1

# Enable script execution if needed:
# Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

$ProjectDir = Split-Path -Parent $MyInvocation.MyCommand.Path

Write-Host "Activating virtual environment..." -ForegroundColor Cyan
& "$ProjectDir\venv\Scripts\Activate.ps1"

Write-Host "Starting Prediction Service (port 8000)..." -ForegroundColor Cyan
$prediction = Start-Process -PassThru powershell -ArgumentList `
    "-NoExit", "-Command", `
    "cd '$ProjectDir\prediction_service'; python app.py"

Write-Host "Waiting for prediction service to start..."
Start-Sleep -Seconds 3

Write-Host "Starting Drift Detection Service (port 8001)..." -ForegroundColor Cyan
$drift = Start-Process -PassThru powershell -ArgumentList `
    "-NoExit", "-Command", `
    "cd '$ProjectDir\drift_service'; python app.py"

Write-Host "Starting Streamlit Frontend (port 8501)..." -ForegroundColor Cyan
$frontend = Start-Process -PassThru powershell -ArgumentList `
    "-NoExit", "-Command", `
    "cd '$ProjectDir'; streamlit run frontend/app.py"

Write-Host ""
Write-Host "All services are running!" -ForegroundColor Green
Write-Host "  Prediction Service : http://localhost:8000  (PID: $($prediction.Id))"
Write-Host "  Drift Service      : http://localhost:8001  (PID: $($drift.Id))"
Write-Host "  Dashboard          : http://localhost:8501  (PID: $($frontend.Id))"
Write-Host ""
Write-Host "Close the PowerShell windows to stop each service." -ForegroundColor Yellow
Write-Host "Or run: Stop-Process -Id $($prediction.Id),$($drift.Id),$($frontend.Id)" -ForegroundColor Yellow
