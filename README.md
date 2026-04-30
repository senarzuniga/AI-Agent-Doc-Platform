# AI-Agent-Doc-Platform

Multi-agent document generation platform with **AI-FACTORY-v2** architecture.

[![CI](https://github.com/senarzuniga/AI-Agent-Doc-Platform/actions/workflows/ci.yml/badge.svg)](https://github.com/senarzuniga/AI-Agent-Doc-Platform/actions/workflows/ci.yml)

## Overview

AI-Agent-Doc-Platform orchestrates three specialised AI agents to produce
professional, research-backed documents from a single prompt:

| Agent | Role |
|-------|------|
| 🔍 **Research Agent** | Gathers facts, statistics, and context |
| ✍️ **Writing Agent** | Drafts structured, professional content |
| ✅ **Review Agent** | Refines and finalises document quality |

## Quick Start

### Prerequisites

- Python 3.10+
- An [OpenAI API key](https://platform.openai.com/api-keys)

### Linux / macOS

```bash
git clone https://github.com/senarzuniga/AI-Agent-Doc-Platform.git
cd AI-Agent-Doc-Platform
./launch.sh
```

### Windows (PowerShell)

```powershell
git clone https://github.com/senarzuniga/AI-Agent-Doc-Platform.git
cd AI-Agent-Doc-Platform
.\launch.ps1
```

Both scripts will:
1. Create a `.venv` virtual environment
2. Install dependencies from `requirements.txt`
3. Copy `.env.example` → `.env` if it doesn't exist
4. Start the Streamlit web app at <http://localhost:8501>

### Manual setup

```bash
python -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\Activate.ps1
pip install -r requirements.txt
cp .env.example .env               # add your OPENAI_API_KEY
streamlit run app/main.py
```

## Python API

```python
from core.orchestrator import run

result = run("Generate a business report on the impact of AI in healthcare")
print(result)
```

## Project Structure

```
AI-Agent-Doc-Platform/
├── app/
│   └── main.py              # Streamlit web application
├── agents/
│   ├── base_agent.py        # Abstract base class for all agents
│   ├── research_agent.py    # Gathers research data and context
│   ├── writing_agent.py     # Drafts professional documents
│   └── review_agent.py      # Reviews and refines document quality
├── core/
│   └── orchestrator.py      # Multi-agent pipeline coordinator
├── tests/
│   └── test_platform.py     # Unit tests
├── .github/
│   └── workflows/
│       └── ci.yml           # CI pipeline (lint + test)
├── config.yaml              # Application and agent configuration
├── .env.example             # Environment variable template
├── requirements.txt         # Python dependencies
├── launch.ps1               # Windows launch script
└── launch.sh                # Linux/macOS launch script
```

## Configuration

Edit `config.yaml` to customise model settings and agent behaviour:

```yaml
model:
  name: gpt-4o-mini
  max_tokens: 4096
  temperature: 0.7
```

Environment variables (`.env`):

| Variable | Description | Default |
|----------|-------------|---------|
| `OPENAI_API_KEY` | OpenAI API key (**required**) | — |
| `OPENAI_MODEL` | Model name | `gpt-4o-mini` |
| `APP_OUTPUT_DIR` | Output directory | `outputs/` |

## GitHub Actions Secrets

Add the following secret in **Settings → Secrets and variables → Actions**:

- `OPENAI_API_KEY` — your OpenAI API key

## Running Tests

```bash
pip install pytest
pytest tests/ -v
```

## License

MIT
