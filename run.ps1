# Unified Startup Script for Event Management System

Write-Host "--- Starting Event Management System Setup ---" -ForegroundColor Cyan

# 1. Check Dependencies
Write-Host "[1/4] Checking dependencies..." -ForegroundColor Yellow
if (!(Get-Command python -ErrorAction SilentlyContinue)) {
    Write-Error "Python is not installed. Please install Python 3.12+."
    exit
}
if (!(Get-Command npm -ErrorAction SilentlyContinue)) {
    Write-Error "Node.js/NPM is not installed. Please install Node.js."
    exit
}

# 2. Setup Backend
Write-Host "[2/4] Setting up Backend..." -ForegroundColor Yellow
cd backend
if (!(Test-Path venv)) {
    Write-Host "Creating Virtual Environment..."
    python -m venv venv
}
& ".\venv\Scripts\Activate.ps1"
Write-Host "Installing Backend dependencies..."
pip install -r requirements.txt
pip install pytest pytest-asyncio pytest-mock httpx # Testing dependencies

# Start Backend in background
Write-Host "Starting Backend on http://localhost:8000..." -ForegroundColor Green
Start-Process powershell -ArgumentList "-NoExit -Command `".\venv\Scripts\Activate.ps1; uvicorn app.main:app --reload`""
cd ..

# 3. Setup Frontend
Write-Host "[3/4] Setting up Frontend..." -ForegroundColor Yellow
cd frontend
Write-Host "Installing Frontend dependencies (this may take a minute)..."
cmd /c npm install
Write-Host "Starting Frontend on http://localhost:4200..." -ForegroundColor Green
Start-Process powershell -ArgumentList "-NoExit -Command `"npm run dev`""
cd ..

Write-Host "[4/4] Success! Both services are starting." -ForegroundColor Cyan
Write-Host "Backend: http://localhost:8000"
Write-Host "Frontend: http://localhost:4200"
Write-Host "Press any key to close this installer (services will keep running)..."
Pause
