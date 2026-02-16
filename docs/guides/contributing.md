# Contributing Guide

We welcome contributions to SASDS! Please follow these guidelines.

## Development Setup

1. **Fork and Clone**:
   ```bash
   git clone https://github.com/your-username/SASDS-AI-Automation.git
   cd SASDS-AI-Automation
   ```

2. **Backend Setup**:
   ```bash
   cd backend
   python -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
   ```
   Create a `.env` file with `GEMINI_API_KEY`.

3. **Frontend Setup**:
   ```bash
   cd frontend
   npm install
   ```

## Running Locally

- **Backend**: `uvicorn app.main:app --reload`
- **Frontend**: `npm run dev`

## Code Style

- **Python**: Follow PEP 8. Use `black` and `isort`.
- **TypeScript**: Use Prettier and ESLint.

## Pull Requests

1. Create a feature branch: `git checkout -b feature/my-feature`
2. Commit changes: `git commit -m "Add my feature"`
3. Push to branch: `git push origin feature/my-feature`
4. Open a Pull Request.

## Reporting Issues

Please use the GitHub Issues tracker to report bugs or request features. Include reproduction steps and logs if possible.
