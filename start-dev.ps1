# Script chay ca Backend (FastAPI) va Frontend (React) cung luc
# Chay tu thu muc root cua project

Write-Host "Bat dau chay Backend va Frontend..." -ForegroundColor Green

# Activate venv
Write-Host ""
Write-Host "Activating virtual environment..." -ForegroundColor Yellow
& .\venv\Scripts\Activate.ps1

# Kiem tra xem frontend da cai dependencies chua
if (-not (Test-Path "frontend\node_modules")) {
    Write-Host ""
    Write-Host "Frontend chua co node_modules. Dang cai dat..." -ForegroundColor Yellow
    Set-Location frontend
    npm install
    Set-Location ..
}

# Chay Backend trong background
Write-Host ""
Write-Host "Khoi dong Backend FastAPI (port 8001)..." -ForegroundColor Cyan
$backendCommand = "cd '$PWD'; .\venv\Scripts\Activate.ps1; uvicorn fastapi_app.main:app --reload --port 8001"
Start-Process powershell -ArgumentList "-NoExit", "-Command", $backendCommand -WindowStyle Normal

# Doi backend khoi dong
Start-Sleep -Seconds 3

# Chay Frontend trong background
Write-Host ""
Write-Host "Khoi dong Frontend React (port 3000)..." -ForegroundColor Cyan
$frontendCommand = "cd '$PWD\frontend'; npm run dev"
Start-Process powershell -ArgumentList "-NoExit", "-Command", $frontendCommand -WindowStyle Normal

Write-Host ""
Write-Host "Da khoi dong ca 2 server!" -ForegroundColor Green
Write-Host ""
Write-Host "Truy cap:" -ForegroundColor Yellow
Write-Host "   - Frontend: http://localhost:3000" -ForegroundColor White
Write-Host "   - Backend API: http://127.0.0.1:8001" -ForegroundColor White
Write-Host "   - API Docs: http://127.0.0.1:8001/docs" -ForegroundColor White
Write-Host ""
Write-Host "De dung server, dong cac cua so PowerShell da mo" -ForegroundColor Gray
Write-Host ""
