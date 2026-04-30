# AI-Agent-Doc-Platform

> Multi-agent document generation platform powered by the **AI-FACTORY-v2** architecture.

[![CI](https://github.com/senarzuniga/AI-Agent-Doc-Platform/actions/workflows/ci.yml/badge.svg)](https://github.com/senarzuniga/AI-Agent-Doc-Platform/actions/workflows/ci.yml)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/UI-Streamlit-ff4b4b.svg)](https://streamlit.io)

---

## Overview

AI-Agent-Doc-Platform chains four specialised AI agents into a single pipeline that turns a brief topic description into a polished, formatted document.

```
Topic → [Research] → [Writer] → [Reviewer] → [Formatter] → Document
```

| Agent | Role |
|-------|------|
| **ResearchAgent** | Gathers key facts and background context |
| **WriterAgent** | Composes the initial structured draft |
| **ReviewerAgent** | Edits and improves the draft for quality |
| **FormatterAgent** | Converts the result into Markdown / HTML / plain text |

---

## Project Structure

```
ai-agent-doc-platform/
├── app/
│   └── main.py              # Streamlit web application
├── agents/
│   ├── base_agent.py        # Shared OpenAI client base class
│   ├── research_agent.py
│   ├── writer_agent.py
│   ├── reviewer_agent.py
│   └── formatter_agent.py
├── core/
│   └── orchestrator.py      # Pipeline coordinator
├── tests/
│   ├── test_orchestrator.py
│   └── test_agents.py
├── .github/workflows/
│   ├── ci.yml               # Lint & test on every push/PR
│   └── deploy.yml           # Deployment verification
├── config.yaml              # Model & pipeline defaults
├── .env.example             # Environment variable template
├── requirements.txt
├── requirements-dev.txt
├── launch.ps1               # Windows launcher
└── launch.sh                # Linux / macOS launcher
```

---

## Quick Start

### Prerequisites
- Python 3.11+
- An [OpenAI API key](https://platform.openai.com/api-keys)

### 1 – Clone & configure

```bash
git clone https://github.com/senarzuniga/AI-Agent-Doc-Platform.git
cd AI-Agent-Doc-Platform
cp .env.example .env
# Edit .env and set OPENAI_API_KEY=sk-...
```

### 2 – Launch (Windows)

```powershell
.\launch.ps1
# Add -Setup on first run to create the virtual environment automatically
.\launch.ps1 -Setup
```

### 2 – Launch (Linux / macOS)

```bash
chmod +x launch.sh
./launch.sh
```

### 3 – Open the app

Navigate to **http://localhost:8501** in your browser.

---

## Use the pipeline from Python

```python
from core.orchestrator import run

document = run(
    topic="The business case for adopting renewable energy in manufacturing",
    doc_type="report",       # report | proposal | summary
    output_format="markdown" # markdown | html | plain
)
print(document)
```

---

## Configuration

Edit **`config.yaml`** to change the default model, temperature, or token limit:

```yaml
openai:
  model: "gpt-4o-mini"
  temperature: 0.7
  max_tokens: 2048
```

---

## Running Tests

```bash
pip install -r requirements-dev.txt
pytest tests/ -v
```

Tests mock the OpenAI API — no real key is needed.

---

## GitHub Actions Secrets

Add the following secret in **Settings → Secrets and variables → Actions**:

| Secret | Description |
|--------|-------------|
| `OPENAI_API_KEY` | Your OpenAI API key (used by CI tests) |

---

## Deploying to Streamlit Cloud

1. Push this repository to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io) → **New app**
3. Select the repo, branch `main`, and entry point `app/main.py`
4. Add `OPENAI_API_KEY` as a secret in the Streamlit Cloud dashboard
5. Click **Deploy**

---

## License

MIT
