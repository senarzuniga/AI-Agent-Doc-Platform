#!/usr/bin/env bash
# launch.sh — Start the AI-Agent-Doc-Platform on Linux/macOS

set -euo pipefail

PORT="${1:-8501}"

echo "╔══════════════════════════════════════════════════════════════╗"
echo "║         AI-Agent-Doc-Platform — AI-FACTORY-v2               ║"
echo "╚══════════════════════════════════════════════════════════════╝"

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$ROOT_DIR"

# Create virtual environment if needed
if [ ! -d ".venv" ]; then
    echo "🔧 Creating virtual environment..."
    python3 -m venv .venv
fi

# Activate virtual environment
echo "✅ Activating virtual environment..."
# shellcheck disable=SC1091
source .venv/bin/activate

# Install / update dependencies
echo "📦 Installing dependencies..."
pip install -r requirements.txt --quiet

# Copy .env.example to .env if not present
if [ ! -f ".env" ] && [ -f ".env.example" ]; then
    cp .env.example .env
    echo "⚠️  Created .env from .env.example. Please edit it and add your OPENAI_API_KEY."
fi

# Create outputs directory
mkdir -p outputs

# Launch Streamlit
echo "🚀 Starting AI-Agent-Doc-Platform on http://localhost:${PORT} ..."
streamlit run app/main.py --server.port "${PORT}"
