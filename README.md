# SASDS-AI-Automation
# SASDS – Single Agent Software Development System

An AI-driven system that automates requirement analysis, code generation,
testing, self-correction, and deployment — using a single intelligent agent.

## Tech Stack
- Backend: FastAPI, Python, LangChain, OpenAI API
- Frontend: React / Next.js
- Testing: Pytest
- CI/CD: GitHub Actions
- Versioning: GitHub API

## Project Structure
SASDS-AI-Automation/
│
├── backend/
│   ├── app/
│   │   ├── main.py
│   │   ├── routers/
│   │   ├── services/
│   │   └── utils/
│   ├── tests/
│   ├── requirements.txt
│   └── README.md
│
├── frontend/
│   ├── src/
│   ├── public/
│   ├── package.json
│   └── README.md
│
├── models/
│   ├── prompts/
│   ├── templates/
│   └── json_schemas/
│
├── docs/
│   ├── architecture/
│   ├── api_docs/
│   └── workflow_diagrams/
│
├── scripts/
│   └── utilities/
│
├── .github/
│   └── workflows/
│       └── ci.yml
│
├── .gitignore
├── README.md
└── LICENSE


## Branch Strategy
- main: production
- dev: active development
- feature/*: individual tasks

## How to Contribute
1. Create feature branch
2. Commit using Conventional Commits
3. Create PR to dev
4. Wait for review + CI
5. Merge
