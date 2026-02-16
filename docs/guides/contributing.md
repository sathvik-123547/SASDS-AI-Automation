# 🤝 Contributing Guide

> SASDS — How to Contribute

We welcome contributions to SASDS! Whether it's a bug fix, new feature, or documentation improvement, here's how to get involved.

---

## Development Setup

### Prerequisites

| Tool | Version |
|---|---|
| Python | 3.9+ |
| Node.js | 18+ |
| npm | 9+ |
| Git | 2.0+ |
| Docker (optional) | 20.10+ |

### 1. Fork and Clone

```bash
git clone https://github.com/your-username/SASDS-AI-Automation.git
cd SASDS-AI-Automation
```

### 2. Backend Setup

```bash
cd backend
python -m venv .venv
source .venv/bin/activate          # macOS/Linux
# .venv\Scripts\activate           # Windows
pip install -r requirements.txt
```

Create a `.env` file:
```bash
echo "GEMINI_API_KEY=your_key_here" > .env
```

### 3. Frontend Setup

```bash
cd frontend
npm install
```

---

## Running Locally

| Service | Command | URL |
|---|---|---|
| **Backend** | `uvicorn app.main:app --reload` | `http://localhost:8000` |
| **Frontend** | `npm run dev` | `http://localhost:5173` |

Or use Docker:
```bash
docker compose up --build
```

---

## Project Structure

| Directory | Language | Description |
|---|---|---|
| `backend/app/routers/` | Python | API route handlers |
| `backend/app/services/` | Python | Business logic & AI integration |
| `backend/app/schemas/` | Python | Pydantic data models |
| `backend/app/utils/` | Python | Shared utilities |
| `frontend/src/components/` | TypeScript | React UI components |
| `frontend/src/api/` | TypeScript | API client |
| `frontend/src/lib/` | TypeScript | Utility libraries |
| `docs/` | Markdown | Documentation |

---

## Code Style

### Python

- Follow **PEP 8** conventions
- Use **Ruff** for linting and formatting
- Use **Mypy** for type checking
- Write docstrings for all public functions

```bash
# Lint
ruff check .

# Format
ruff format .

# Type check
mypy .
```

### TypeScript

- Use **Prettier** for formatting
- Use **ESLint** for linting
- Prefer functional components with hooks
- Use proper TypeScript types (avoid `any`)

```bash
# Type check
npx tsc --noEmit
```

---

## Making Changes

### 1. Create a Feature Branch

```bash
git checkout -b feature/your-feature-name
```

### 2. Implement Your Changes

- Write clean, well-documented code
- Follow existing patterns and conventions
- Add or update tests as needed

### 3. Test Your Changes

```bash
# Backend tests
cd backend && pytest

# Frontend type check
cd frontend && npx tsc --noEmit
```

### 4. Commit

Write clear, descriptive commit messages:

```bash
git commit -m "feat: add user authentication endpoint"
git commit -m "fix: resolve file explorer crash on empty directories"
git commit -m "docs: update API reference with new endpoints"
```

**Commit Message Prefixes:**

| Prefix | Use |
|---|---|
| `feat:` | New feature |
| `fix:` | Bug fix |
| `docs:` | Documentation changes |
| `refactor:` | Code refactoring |
| `test:` | Test additions/changes |
| `chore:` | Build/config changes |

### 5. Push and Open a PR

```bash
git push origin feature/your-feature-name
```

Open a Pull Request against the `main` branch with:
- Clear description of what changed
- Link to any related issues
- Screenshots for UI changes

---

## CI/CD Pipeline

All PRs are automatically validated by GitHub Actions:

| Check | Tool | What It Does |
|---|---|---|
| **Lint** | Ruff | Code style enforcement |
| **Type Check** | Mypy | Static type analysis |
| **Unit Tests** | Pytest | Automated test execution |
| **Docker Build** | Docker Buildx | Validates container builds |

---

## Reporting Issues

Please use the [GitHub Issues](https://github.com/your-username/SASDS-AI-Automation/issues) tracker:

1. **Bug Report**: Include reproduction steps, expected vs. actual behavior, and logs
2. **Feature Request**: Describe the use case and proposed solution
3. **Question**: For general questions, use the Discussions tab

---

## Code of Conduct

Be respectful, inclusive, and constructive. We follow the [Contributor Covenant](https://www.contributor-covenant.org/) Code of Conduct.
