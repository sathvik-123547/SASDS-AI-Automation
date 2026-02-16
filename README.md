# SASDS - Single Agent Software Development System

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

**SASDS** is a revolutionary AI-powered IDE designed to democratize software creation. It transforms natural language requirements into full-stack applications, provides real-time streaming feedback, and offers an intelligent "Auto-Pilot" to maintain code health.

## 🚀 Key Features

- **Agentic Workflow**: A single agent that understands context, refines code, and fixes bugs autonomously.
- **Real-time Streaming**: Watch your code being written live, token-by-token.
- **Auto-Pilot**: Proactive background analysis for bugs, security issues, and improvements.
- **Interactive Terminal**: Full xterm.js integration with backend PTY support.
- **Modern UI**: VS Code-like experience with Monaco Editor, Files Explorer, and Split Panes.

## 📚 Documentation

We have comprehensive documentation available in the `docs/` directory:

- **[System Architecture](docs/architecture/system_overview.md)**: High-level design and diagrams.
- **[Backend API](docs/backend/overview.md)**: Service details and API endpoints.
- **[Frontend Guide](docs/frontend/overview.md)**: Component structure and state management.
- **[Deployment](docs/ops/deployment.md)**: Docker and deployment instructions.
- **[User Guide](docs/guides/user_guide.md)**: How to use the IDE.
- **[Contributing](docs/guides/contributing.md)**: How to contribute to SASDS.

## Quick Start

### Prerequisites

- Docker & Docker Compose
- Google Gemini API Key

### Running with Docker

1. **Clone the repository**:
   ```bash
   git clone https://github.com/your-username/SASDS-AI-Automation.git
   cd SASDS-AI-Automation
   ```

2. **Set API Key**:
   Add your `GEMINI_API_KEY` to `backend/.env`.

3. **Launch**:
   ```bash
   docker compose up --build
   ```

4. **Access**:
   Open `http://localhost:5173` in your browser.

## License

This project is licensed under the MIT License - see the `LICENSE` file for details.
