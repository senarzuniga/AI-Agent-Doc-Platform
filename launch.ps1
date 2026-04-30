# launch.ps1 – Start the AI-Agent-Doc-Platform locally
# Run with: .\launch.ps1

param(
    [switch]$Setup
)

$ErrorActionPreference = "Stop"

Write-Host @"
╔══════════════════════════════════════════════════════════════╗
║          AI-Agent-Doc-Platform  –  Launcher                 ║
╚══════════════════════════════════════════════════════════════╝
"@ -ForegroundColor Cyan

# ── Optional first-time setup ──────────────────────────────────────────────
if ($Setup -or -not (Test-Path ".venv")) {
    Write-Host "`n🔧 Setting up virtual environment..." -ForegroundColor Yellow
    python -m venv .venv
    Write-Host "✅ Virtual environment created" -ForegroundColor Green

    Write-Host "`n📦 Installing dependencies..." -ForegroundColor Yellow
    & .venv\Scripts\pip install --upgrade pip | Out-Null
    & .venv\Scripts\pip install -r requirements.txt
    Write-Host "✅ Dependencies installed" -ForegroundColor Green
}

# ── Copy .env template if needed ───────────────────────────────────────────
if (-not (Test-Path ".env")) {
    Copy-Item ".env.example" ".env"
    Write-Host "`n⚠️  Created .env from template." -ForegroundColor Yellow
    Write-Host "   Edit .env and add your OPENAI_API_KEY before continuing." -ForegroundColor Yellow
    Write-Host "   Then run .\launch.ps1 again." -ForegroundColor Yellow
    exit 0
}

# ── Launch Streamlit ────────────────────────────────────────────────────────
Write-Host "`n🚀 Launching Streamlit app..." -ForegroundColor Green
Write-Host "   Open http://localhost:8501 in your browser`n" -ForegroundColor Cyan

& .venv\Scripts\streamlit run app\main.py
