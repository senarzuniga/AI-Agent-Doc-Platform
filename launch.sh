#!/usr/bin/env bash
# launch.sh – Start the AI-Agent-Doc-Platform locally (Linux / macOS)
set -e

echo "╔══════════════════════════════════════════════════════════════╗"
echo "║          AI-Agent-Doc-Platform  –  Launcher                 ║"
echo "╚══════════════════════════════════════════════════════════════╝"

# ── Virtual environment ──────────────────────────────────────────────────────
if [ ! -d ".venv" ]; then
    echo -e "\n🔧 Creating virtual environment..."
    python3 -m venv .venv
    echo "✅ Virtual environment created"
fi

source .venv/bin/activate

echo -e "\n📦 Installing dependencies..."
pip install --upgrade pip -q
pip install -r requirements.txt -q
echo "✅ Dependencies installed"

# ── .env setup ───────────────────────────────────────────────────────────────
if [ ! -f ".env" ]; then
    cp .env.example .env
    echo -e "\n⚠️  Created .env from template."
    echo "   Edit .env and add your OPENAI_API_KEY, then run ./launch.sh again."
    exit 0
fi

# ── Launch Streamlit ─────────────────────────────────────────────────────────
echo -e "\n🚀 Launching Streamlit app..."
echo "   Open http://localhost:8501 in your browser"
echo ""
streamlit run app/main.py
