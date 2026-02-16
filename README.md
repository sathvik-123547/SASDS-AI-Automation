# 🚀 SASDS — Single Agent Software Development System

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python](https://img.shields.io/badge/Python-3.9+-3776AB?logo=python&logoColor=white)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.109+-009688?logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com)
[![React](https://img.shields.io/badge/React-18.3+-61DAFB?logo=react&logoColor=black)](https://reactjs.org)
[![TypeScript](https://img.shields.io/badge/TypeScript-5.6+-3178C6?logo=typescript&logoColor=white)](https://typescriptlang.org)
[![Docker](https://img.shields.io/badge/Docker-Compose-2496ED?logo=docker&logoColor=white)](https://docker.com)

**SASDS** is a revolutionary **AI-powered IDE** that transforms natural language requirements into full-stack applications. Powered by **Google Gemini AI**, it provides real-time streaming code generation, an intelligent Auto-Pilot for proactive code analysis, and a self-correction engine that automatically fixes bugs.

---

## ✨ Key Features

| Feature | Description |
|---|---|
| 🏗️ **Natural Language to Code** | Describe your app in plain English — the AI builds it |
| ⚡ **Real-Time Streaming** | Watch code being written live, token by token |
| 🤖 **Auto-Pilot** | Proactive scanning for bugs, security issues, and improvements |
| 🔧 **Self-Correction** | Automatically runs tests and fixes failures (up to 3 iterations) |
| 💬 **Context-Aware Chat** | AI assistant that understands your current file and project |
| ✨ **Code Refinement** | Select code and give AI instructions to modify it |
| 💻 **Interactive Terminal** | Full shell session via xterm.js WebSocket PTY |
| 📝 **Monaco Editor** | VS Code-grade editor with 50+ language support |
| 📁 **File Explorer** | Full file tree with create, rename, delete operations |
| 🔗 **GitHub Integration** | Sync projects directly to GitHub repositories |

---

## 🏗️ Architecture

![System Architecture](docs/images/system_architecture.png)

**Full architecture documentation →** [System Architecture](docs/architecture/system_overview.md)

---

## 🚀 Quick Start

### Prerequisites

- **Docker** & **Docker Compose** (recommended)
- **Google Gemini API Key** ([Get one here](https://aistudio.google.com/app/apikey))

### Option 1: Docker (Recommended)

```bash
# 1. Clone
git clone https://github.com/your-username/SASDS-AI-Automation.git
cd SASDS-AI-Automation

# 2. Configure
echo "GEMINI_API_KEY=your_api_key_here" > backend/.env

# 3. Launch
docker compose up --build -d

# 4. Open
open http://localhost:5173
```

### Option 2: Local Development

```bash
# Backend
cd backend
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
echo "GEMINI_API_KEY=your_key" > .env
uvicorn app.main:app --reload --port 8000

# Frontend (new terminal)
cd frontend
npm install
npm run dev
```

---

## 📚 Documentation

| Document | Description |
|---|---|
| [📋 Project Proposal](docs/PROJECT_PROPOSAL.md) | Executive summary, features, and roadmap |
| [🏗️ System Architecture](docs/architecture/system_overview.md) | High-level design with Mermaid diagrams |
| [🔧 Technical Design](docs/architecture/technical_design.md) | Deep-dive into implementation details |
| [📡 API Reference](docs/API_REFERENCE.md) | Complete REST & WebSocket API documentation |
| [⚙️ Backend Guide](docs/backend/overview.md) | Service layer, configuration, and setup |
| [🎨 Frontend Guide](docs/frontend/overview.md) | Component architecture and state management |
| [🚀 Deployment](docs/ops/deployment.md) | Docker & production deployment guide |
| [📖 User Guide](docs/guides/user_guide.md) | How to use every feature of the IDE |
| [🤝 Contributing](docs/guides/contributing.md) | Development setup and contribution workflow |
| [🔐 Security](docs/SECURITY.md) | Security policy and vulnerability reporting |
| [📋 Changelog](docs/CHANGELOG.md) | Version history and release notes |

---

## 🛠️ Tech Stack

| Layer | Technologies |
|---|---|
| **Frontend** | React 18, TypeScript, Vite, TailwindCSS, Shadcn/UI, Monaco Editor, xterm.js |
| **Backend** | FastAPI, Python 3.11+, Uvicorn, Pydantic, SQLAlchemy |
| **AI** | Google Gemini 2.5 Flash |
| **Infrastructure** | Docker, Docker Compose, PostgreSQL, Redis, GitHub Actions |

---

## 📄 License

This project is licensed under the **MIT License** — see the [LICENSE](LICENSE) file for details.

---

<p align="center">
  <b>SASDS</b> — Turning ideas into software, one prompt at a time.
</p>
