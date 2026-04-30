# launch.ps1 — Start the AI-Agent-Doc-Platform on Windows
param(
    [switch]$SkipVenv,
    [string]$Port = "8501"
)

Write-Host @"
╔══════════════════════════════════════════════════════════════╗
║         AI-Agent-Doc-Platform — AI-FACTORY-v2               ║
╚══════════════════════════════════════════════════════════════╝
"@ -ForegroundColor Cyan

$rootDir = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $rootDir

# Create virtual environment if needed
if (-not $SkipVenv -and -not (Test-Path ".venv")) {
    Write-Host "🔧 Creating virtual environment..." -ForegroundColor Yellow
    python -m venv .venv
}

# Activate virtual environment
if (-not $SkipVenv -and (Test-Path ".venv\Scripts\Activate.ps1")) {
    Write-Host "✅ Activating virtual environment..." -ForegroundColor Green
    & .\.venv\Scripts\Activate.ps1
}

# Install / update dependencies
Write-Host "📦 Installing dependencies..." -ForegroundColor Yellow
pip install -r requirements.txt --quiet

# Copy .env.example to .env if not present
if (-not (Test-Path ".env") -and (Test-Path ".env.example")) {
    Copy-Item ".env.example" ".env"
    Write-Host "⚠️  Created .env from .env.example. Please edit it and add your OPENAI_API_KEY." -ForegroundColor Yellow
}

# Create outputs directory
New-Item -Path "outputs" -ItemType Directory -Force | Out-Null

# Launch Streamlit
Write-Host "🚀 Starting AI-Agent-Doc-Platform on http://localhost:$Port ..." -ForegroundColor Green
streamlit run app\main.py --server.port $Port
