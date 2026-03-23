# SASDS — Comprehensive Architecture & Technical Documentation

> **Single Agent Software Development System** — High-Level Documentation

**Version:** 1.0  
**Last Updated:** March 2026

---

## Table of Contents

1. [Software Architecture](#1-software-architecture)
2. [Technical Architecture](#2-technical-architecture)
3. [Sequence Diagrams](#3-sequence-diagrams)
4. [Use Case Diagrams](#4-use-case-diagrams)
5. [Class Diagrams](#5-class-diagrams)
6. [Algorithms](#6-algorithms)
7. [Implementation Steps](#7-implementation-steps)
8. [Test Cases Table](#8-test-cases-table)
9. [Major Source Code](#9-major-source-code)

---

## 1. Software Architecture

### 1.1 Overview

SASDS is a **full-stack, AI-powered IDE** that transforms natural language requirements into working software. The system follows a **layered architecture** with clear separation of concerns.

```
┌─────────────────────────────────────────────────────────────────────────┐
│                     PRESENTATION LAYER (Frontend)                        │
│  React 18 + TypeScript + Vite | Monaco Editor | xterm.js | Radix UI     │
└─────────────────────────────────────────────────────────────────────────┘
                                      │
                                      ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                     API GATEWAY (FastAPI)                                │
│  REST APIs | WebSocket | CORS | Middleware | Error Handling             │
└─────────────────────────────────────────────────────────────────────────┘
                                      │
                                      ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                     AI SERVICE LAYER                                     │
│  Requirements Analyzer | Code Generator | Test Gen | Review | Self-Fix    │
│  Auto-Pilot | Chat Agent | Fix Generator | GitHub Sync                   │
└─────────────────────────────────────────────────────────────────────────┘
                                      │
                                      ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                     STORAGE & INFRASTRUCTURE LAYER                       │
│  SQLite (metadata) | File System (generated_projects) | GitHub API       │
└─────────────────────────────────────────────────────────────────────────┘
```

### 1.2 Component Responsibilities

| Layer | Components | Responsibility |
|-------|------------|----------------|
| **Frontend** | App Shell, File Explorer, Code Viewer, Terminal, Chat | User interaction, state orchestration, real-time updates |
| **API Gateway** | Routers, Middleware | Request routing, validation, CORS, logging |
| **AI Services** | Gemini client, Code/Test/Review generators | Natural language processing, code generation, analysis |
| **Persistence** | SQLite, File Writer | Run logs, generated project storage |

---

## 2. Technical Architecture

### 2.1 Technology Stack

| Layer | Technologies |
|-------|---------------|
| **Frontend** | React 18, TypeScript 5.6+, Vite 6, TailwindCSS, Radix UI, Monaco Editor, xterm.js |
| **Backend** | FastAPI 0.109+, Uvicorn, Python 3.9+ |
| **AI** | Google Gemini 2.5 Flash (`google-generativeai`) |
| **Database** | SQLite (default) via SQLAlchemy 2 |
| **Infrastructure** | Docker Compose, PostgreSQL (optional), Redis (optional) |

### 2.2 Directory Structure

```
SASDS-AI-Automation/
├── backend/
│   ├── app/
│   │   ├── core/           # Config (settings, env vars)
│   │   ├── db/             # SQLAlchemy models, session
│   │   ├── routers/        # 14 API route handlers
│   │   ├── schemas/        # Pydantic request/response models
│   │   ├── services/      # AI integration, business logic
│   │   └── utils/         # file_writer, test_runner
│   ├── generated_projects/  # Output directory for generated code
│   ├── tests/             # Pytest (conftest)
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── components/    # CodeViewer, FileExplorer, Terminal, ChatInterface
│   │   ├── api/           # HTTP client, streaming
│   │   └── lib/           # stream-parser, file-utils
│   └── cypress/           # E2E tests
├── docs/                  # Documentation
└── docker-compose.yml
```

### 2.3 Data Flow Summary

- **Requirements** → `POST /requirements/analyze` → Gemini → Structured JSON
- **Code Gen** → `POST /code/generate/stream` → Gemini (streaming) → Delimiter protocol
- **Write** → `POST /code/write` → `file_writer` → `generated_projects/{id}/`
- **Self-Fix** → `POST /self/fix` → pytest → detect failing file → Gemini fix → rewrite
- **Auto-Pilot** → `POST /autopilot/analyze` → scan project → Gemini analysis
- **Chat** → `POST /chat/send` → context + history → Gemini response
- **Terminal** → `WS /terminal/ws` → PTY → shell

---

## 3. Sequence Diagrams

### 3.1 End-to-End Code Generation (Streaming)

```
User          Frontend         Backend API      Gemini AI       File System
  │               │                  │                │               │
  │ Enter reqs    │                  │                │               │
  ├──────────────►│ POST /analyze    │                │               │
  │               ├─────────────────►│ analyze        │               │
  │               │                  ├──────────────►│               │
  │               │                  │◄──────────────┤ (JSON)        │
  │               │◄─────────────────┤                │               │
  │               │                  │                │               │
  │ Click Generate│                  │                │               │
  ├──────────────►│ POST /stream     │                │               │
  │               ├─────────────────►│ generate_stream│               │
  │               │                  ├──────────────►│               │
  │               │    ┌──────────────Streaming Loop─────────────────┐│
  │               │    │  Gemini ──► Backend ──► Frontend (parse)     ││
  │               │    └─────────────────────────────────────────────┘│
  │               │                  │                │               │
  │               │ POST /code/write │                │               │
  │               ├─────────────────►│ write_files   │               │
  │               │                  ├──────────────────────────────►│
  │               │◄─────────────────┤                │   Success     │
  │◄──────────────┤                  │                │               │
```

### 3.2 Self-Correction Loop

```
Client           Backend           Test Runner      Gemini          File System
   │                │                    │               │                 │
   │ POST /self/fix │                    │               │                 │
   ├───────────────►│ run_pytest         │               │                 │
   │                ├──────────────────►│               │                 │
   │                │◄──────────────────┤ (fail)        │                 │
   │                │ detect_failing_file│               │                 │
   │                │ read_file ─────────────────────────────────────────►│
   │                │ generate_fix       ├─────────────►│                 │
   │                │                    │               │                 │
   │                │◄──────────────────────────────────┤ (fixed code)    │
   │                │ write_file ────────────────────────────────────────►│
   │                │ run_pytest (retry) │               │                 │
   │                ├──────────────────►│               │                 │
   │                │◄──────────────────┤ (pass/fail)  │                 │
   │◄───────────────┤ return result      │               │                 │
```

### 3.3 Terminal WebSocket Session

```
User         xterm.js       WebSocket       Python PTY       Shell
  │              │               │                │             │
  │ Connect      │ WS /terminal/ws               │             │
  ├─────────────►│───────────────►│ Spawn PTY    │             │
  │              │                ├─────────────►│ Start shell │
  │              │                │              ├────────────►│
  │              │                │              │             │
  │ keypress     │ input          │ stdin        │ exec        │
  ├─────────────►│───────────────►│─────────────►│────────────►│
  │              │                │ stdout       │ output      │
  │◄─────────────┤◄───────────────┤◄─────────────┤◄────────────┤
```

---

## 4. Use Case Diagrams

### 4.1 Actor–System Interactions (Text Diagram)

```
                              ┌──────────────────────────────────────────┐
                              │             SASDS System                 │
                              │                                          │
    ┌─────────┐               │  ┌─────────────────────────────────────┐  │
    │ Developer│──────────────┼─►│ Analyze Requirements (NL → JSON)    │  │
    └─────────┘               │  └─────────────────────────────────────┘  │
          │                   │  ┌─────────────────────────────────────┐  │
          │                   │  │ Generate Code (streaming)           │  │
          └───────────────────┼─►─────────────────────────────────────│  │
                              │  └─────────────────────────────────────┘  │
                              │  ┌─────────────────────────────────────┐  │
                              │  │ Write Project to Disk                 │  │
                              │  └─────────────────────────────────────┘  │
                              │  ┌─────────────────────────────────────┐  │
                              │  │ Run Auto-Pilot Analysis              │  │
                              │  └─────────────────────────────────────┘  │
                              │  ┌─────────────────────────────────────┐  │
                              │  │ Self-Correct (run tests, fix bugs)   │  │
                              │  └─────────────────────────────────────┘  │
                              │  ┌─────────────────────────────────────┐  │
                              │  │ Chat with AI (context-aware)         │  │
                              │  └─────────────────────────────────────┘  │
                              │  ┌─────────────────────────────────────┐  │
                              │  │ Refine File (NL instructions)       │  │
                              │  └─────────────────────────────────────┘  │
                              │  ┌─────────────────────────────────────┐  │
                              │  │ Use Terminal (PTY shell)             │  │
                              │  └─────────────────────────────────────┘  │
                              │  ┌─────────────────────────────────────┐  │
                              │  │ File CRUD (create/rename/delete)     │  │
                              │  └─────────────────────────────────────┘  │
                              │  ┌─────────────────────────────────────┐  │
                              │  │ Sync to GitHub                       │  │
                              │  └─────────────────────────────────────┘  │
                              └──────────────────────────────────────────┘
```

### 4.2 Use Case Summary

| Use Case ID | Use Case Name | Actor | Description |
|-------------|---------------|-------|--------------|
| UC-01 | Analyze Requirements | Developer | Submit NL text, receive structured modules/entities/APIs |
| UC-02 | Generate Code | Developer | Stream code generation from requirements |
| UC-03 | Write Project | Developer | Persist generated files to disk |
| UC-04 | Auto-Pilot Scan | Developer | Full project analysis for bugs/security |
| UC-05 | Self-Correct Tests | Developer | Auto-fix failing tests (max 3 attempts) |
| UC-06 | Chat with Agent | Developer | Context-aware AI conversation |
| UC-07 | Refine File | Developer | Modify a file via NL instructions |
| UC-08 | Use Terminal | Developer | Interactive shell via WebSocket |
| UC-09 | Manage Files | Developer | Create, rename, delete files |
| UC-10 | Sync to GitHub | Developer | Push project to remote repository |

---

## 5. Class Diagrams

### 5.1 Backend Schemas (Pydantic)

```
┌─────────────────────────────────┐
│ RequirementAnalysisRequest      │
├─────────────────────────────────┤
│ + requirements_text: str        │
└─────────────────────────────────┘

┌─────────────────────────────────┐     ┌─────────────────────────────────┐
│ RequirementAnalysisResponse     │     │ ModuleItem                       │
├─────────────────────────────────┤     ├─────────────────────────────────┤
│ + modules: List[ModuleItem]      │────►│ + name: str                      │
│ + entities: List[EntityItem]     │     │ + description: Optional[str]     │
│ + apis: List[APIItem]            │     └─────────────────────────────────┘
│ + non_functional_requirements   │
│ + tech_stack_suggestions         │     ┌─────────────────────────────────┐
│ + missing_information           │     │ EntityItem                       │
└─────────────────────────────────┘     ├─────────────────────────────────┤
                                         │ + name: str                      │
         │                               │ + attributes: List[str]          │
         │                               └─────────────────────────────────┘
         │                               ┌─────────────────────────────────┐
         │                               │ APIItem                           │
         │                               ├─────────────────────────────────┤
         │                               │ + name: str                       │
         │                               │ + method: str                     │
         │                               │ + path: str                       │
         │                               │ + description: Optional[str]     │
         │                               └─────────────────────────────────┘

┌─────────────────────────────────┐     ┌─────────────────────────────────┐
│ CodeGenerationRequest           │     │ GeneratedFile                    │
├─────────────────────────────────┤     ├─────────────────────────────────┤
│ + requirements_text: str        │     │ + path: str                      │
│ + analysis: Optional[Analysis] │     │ + description: Optional[str]     │
└─────────────────────────────────┘     │ + content: str                    │
         │                               └─────────────────────────────────┘
         │
         ▼
┌─────────────────────────────────┐     ┌─────────────────────────────────┐
│ CodeGenerationResponse          │     │ RefinementRequest                │
├─────────────────────────────────┤     ├─────────────────────────────────┤
│ + files: List[GeneratedFile]    │     │ + path: str                      │
└─────────────────────────────────┘     │ + content: str                    │
                                         │ + instructions: str              │
                                         └─────────────────────────────────┘
```

### 5.2 Database Model

```
┌─────────────────────────────────┐
│ RunLog (SQLAlchemy)             │
├─────────────────────────────────┤
│ + id: Integer (PK)              │
│ + created_at: DateTime          │
│ + run_id: String                │
│ + kind: String                  │  # analysis|codegen|tests|review|write
│ + payload: Text (JSON)          │
│ + note: String                  │
└─────────────────────────────────┘
```

---

## 6. Algorithms

### 6.1 Requirements Analysis Pipeline

```
Algorithm: analyze_requirements
Input: requirements_text (string)
Output: RequirementAnalysisResponse (structured JSON)

1. Build prompt with system instructions and user text
2. Call Gemini API with response_mime_type='application/json'
3. Parse response.text as JSON
4. Validate against RequirementAnalysisResponse schema
5. Return validated object
6. On error: raise HTTPException(500)
```

### 6.2 Streaming Code Generation Protocol

```
Algorithm: stream_code_generation
Input: requirements_text, optional analysis
Output: AsyncGenerator[str] (text chunks)

1. Build prompt with requirements and analysis
2. Configure Gemini with streaming
3. Define delimiter format: ### FILE: path\ncontent\n### END FILE ###
4. For each chunk from model.generate_content_stream():
   a. Append chunk to buffer
   b. Yield chunk to client
5. Client (frontend) parses buffer with regex:
   - /### FILE: \s*(.+?)\s*[\r\n]+([\s\S]*?)### END FILE ###/g
   - Extract path, content, isComplete
```

### 6.3 Self-Correction Algorithm

```
Algorithm: run_self_correction(project_path, max_attempts=3)
Input: project_path (str), max_attempts (int)
Output: { success, attempts, message, logs }

1. FOR attempt = 1 TO max_attempts:
   a. (success, output) = run_pytest(project_path)
   b. IF success: RETURN { success: true, attempts: attempt, logs: output }
   c. failing_file = _detect_failing_file(output, project_path)
   d. IF NOT failing_file: RETURN { success: false, message: "Could not detect failing file" }
   e. original_content = read_file(project_path / failing_file)
   f. fixed_content = generate_fix(failing_file, original_content, output)
   g. write_file(project_path / failing_file, fixed_content)
2. RETURN { success: false, attempts: max_attempts, message: "Max attempts reached" }

Algorithm: _detect_failing_file(output, project_path)
1. FOR each line IN output.splitlines():
   a. match = regex ([^\s:]+\.py)(?::\d+)?
   b. IF match: candidate = match.group(1)
   c. candidate_path = normpath(join(project_path, candidate))
   d. IF exists(candidate_path): RETURN relpath(candidate_path, project_path)
2. RETURN null
```

---

## 7. Implementation Steps

### 7.1 Backend Setup

| Step | Action | Notes |
|------|--------|-------|
| 1 | Create virtual environment | `python -m venv venv` |
| 2 | Activate venv | `source venv/bin/activate` (Unix) / `venv\Scripts\activate` (Win) |
| 3 | Install dependencies | `pip install -r requirements.txt` |
| 4 | Create `.env` | `GEMINI_API_KEY=your_key`, optional `DB_URL`, `GITHUB_*` |
| 5 | Run migrations | DB auto-created if SQLite |
| 6 | Start server | `uvicorn app.main:app --reload --port 8000` |

### 7.2 Frontend Setup

| Step | Action | Notes |
|------|--------|-------|
| 1 | Install Node dependencies | `npm install` |
| 2 | Configure API URL | Optional `VITE_API_BASE_URL` in `.env` |
| 3 | Start dev server | `npm run dev` (Vite on 5173) |

### 7.3 End-to-End Pipeline Flow

| Step | Component | Implementation |
|------|-----------|----------------|
| 1 | User enters requirements | `requirementsText` state in `App.tsx` |
| 2 | Analyze | `analyzeRequirements()` → `POST /requirements/analyze` |
| 3 | Generate (stream) | `generateCodeStream()` → `POST /code/generate/stream` |
| 4 | Parse stream | `parseStreamBuffer()` with `### FILE:` / `### END FILE ###` |
| 5 | Update UI | `setCodeResult()`, `buildFileTree()`, `setSelectedFile()` |
| 6 | Write to disk | `writeCodeToDisk()` → `POST /code/write` |
| 7 | Optional Auto-Pilot | `runAutoPilot()` → `POST /autopilot/analyze` |
| 8 | Optional Chat | `sendChatMessage()` → `POST /chat/send` |

---

## 8. Test Cases Table

| ID | Test Case | Input | Expected Output | Type |
|----|-----------|-------|-----------------|------|
| TC-01 | Health check | `GET /ping` | `{"message": "Backend is running successfully!"}` | API |
| TC-02 | Analyze empty requirements | `POST /requirements/analyze` `{requirements_text: ""}` | 400 Bad Request | API |
| TC-03 | Analyze valid requirements | `POST /requirements/analyze` with NL text | 200, structured JSON (modules, entities, apis) | API |
| TC-04 | Generate code (batch) | `POST /code/generate` with requirements | 200, `CodeGenerationResponse` with files | API |
| TC-05 | Generate code (stream) | `POST /code/generate/stream` | 200, text/plain stream with `### FILE:` format | API |
| TC-06 | Write files to disk | `POST /code/write` with project_id, files | 200, files written under `generated_projects/` | API |
| TC-07 | Self-fix (tests pass) | `POST /self/fix` with project_path (all pass) | `success: true`, attempts: 1 | API |
| TC-08 | Self-fix (detect failing file) | `POST /self/fix` with failing tests | Fix applied, retry until pass or max_attempts | API |
| TC-09 | Auto-Pilot analyze | `POST /autopilot/analyze` with project_id | 200, summary, issues[], improvements[] | API |
| TC-10 | Chat send | `POST /chat/send` with message, history, context | 200, `{role, content}` | API |
| TC-11 | File create | `POST /files/create` path, content | 200, file created | API |
| TC-12 | File delete | `DELETE /files/delete` path | 200, file deleted | API |
| TC-13 | File rename | `PUT /files/rename` old_path, new_path | 200, renamed | API |
| TC-14 | Path traversal blocked | `POST /files/create` path with `../` | 403 Forbidden | API |
| TC-15 | List projects | `GET /projects/` | 200, list of project_ids | API |
| TC-16 | Download project | `GET /projects/{id}/download` | Binary ZIP | API |
| TC-17 | Refine file | `POST /refine/` path, content, instructions | 200, new_content, explanation | API |
| TC-18 | UI loads | Visit `/` | Page contains "SASDS" | E2E |
| TC-19 | Stream parsing | Buffer with `### FILE: x\ncontent\n### END FILE ###` | Parsed files with path, content, isComplete | Unit |

---

## 9. Major Source Code

### 9.1 Main Application Entry (`backend/app/main.py`)

```python
# Core setup
app = FastAPI(title="SASDS Backend", version="0.1.0")
app.add_middleware(CORSMiddleware, allow_origins=["*"], ...)
app.include_router(base_router)
app.include_router(requirements_router)
app.include_router(codegen_router)
app.include_router(code_writer_router)
app.include_router(tests_router)
app.include_router(self_fix_router)
app.include_router(review_router)
app.include_router(github_router)
app.include_router(projects_router)
app.include_router(runs_router)
app.include_router(refine_router)
app.include_router(terminal_router)
app.include_router(files_router)
app.include_router(autopilot_router)
app.include_router(chat_router)
```

### 9.2 Pydantic Schemas (`backend/app/schemas/requirements.py`)

```python
class RequirementAnalysisRequest(BaseModel):
    requirements_text: str

class ModuleItem(BaseModel):
    name: str
    description: Optional[str] = None

class EntityItem(BaseModel):
    name: str
    attributes: List[str] = Field(default_factory=list)

class APIItem(BaseModel):
    name: str
    method: str
    path: str
    description: Optional[str] = None

class RequirementAnalysisResponse(BaseModel):
    modules: List[ModuleItem]
    entities: List[EntityItem]
    apis: List[APIItem]
    non_functional_requirements: List[str]
    tech_stack_suggestions: List[str]
    missing_information: List[str]
```

### 9.3 File Writer (`backend/app/utils/file_writer.py`)

```python
def write_generated_files(project_id: str, files: list) -> str:
    base_dir = os.path.abspath("generated_projects")
    project_dir = os.path.join(base_dir, project_id)
    os.makedirs(project_dir, exist_ok=True)
    for file in files:
        rel_path = file["path"]
        content = file["content"]
        full_path = os.path.join(project_dir, rel_path)
        os.makedirs(os.path.dirname(full_path), exist_ok=True)
        with open(full_path, "w", encoding="utf-8") as f:
            f.write(content)
    return project_dir
```

### 9.4 Stream Parser (`frontend/src/lib/stream-parser.ts`)

```typescript
const fileRegex = /### FILE: \s*(.+?)\s*[\r\n]+([\s\S]*?)### END FILE ###/g;
function parseStreamBuffer(buffer: string): ParsedFile[] {
  const files: ParsedFile[] = [];
  let match;
  while ((match = fileRegex.exec(buffer)) !== null) {
    files.push({ path: match[1].trim(), content: match[2], isComplete: true });
  }
  const remaining = buffer.slice(lastIndex);
  const startMatch = /### FILE: \s*(.+?)\s*[\r\n]+([\s\S]*)$/.exec(remaining);
  if (startMatch) {
    files.push({ path: startMatch[1].trim(), content: startMatch[2], isComplete: false });
  }
  return files;
}
```

### 9.5 Self-Correction Core (`backend/app/services/self_corrector.py`)

```python
def run_self_correction(project_path: str, max_attempts: int = 3):
    for attempt in range(1, max_attempts + 1):
        success, output = run_tests_in_project(project_path)
        if success:
            return {"success": True, "attempts": attempt, "message": "All tests passed.", "logs": output}
        failing_file = _detect_failing_file(output, project_path)
        if not failing_file:
            return {"success": False, "message": "Could not detect failing file.", "logs": output}
        with open(os.path.join(project_path, failing_file), "r") as f:
            original_content = f.read()
        fixed_content = generate_fix(failing_file, original_content, output)
        with open(os.path.join(project_path, failing_file), "w") as f:
            f.write(fixed_content)
    return {"success": False, "attempts": max_attempts, "message": "Max attempts reached.", "logs": output}
```

---

## Appendix: Key API Endpoints

| Method | Path | Purpose |
|--------|------|---------|
| GET | `/ping` | Liveness |
| POST | `/requirements/analyze` | NL → structured analysis |
| POST | `/code/generate` | Batch code gen |
| POST | `/code/generate/stream` | Streaming code gen |
| POST | `/code/write` | Persist to disk |
| POST | `/tests/generate` | Generate tests |
| POST | `/self/fix` | Self-correction loop |
| POST | `/review/` | Code review |
| POST | `/refine/` | Refine file |
| POST | `/autopilot/analyze` | Project analysis |
| POST | `/chat/send` | Agent chat |
| POST | `/github/sync` | GitHub sync |
| GET | `/projects/` | List projects |
| GET | `/projects/{id}/download` | Download ZIP |
| WS | `/terminal/ws` | PTY terminal |
| POST/DELETE/PUT | `/files/*` | File CRUD |

---

*Document generated for SASDS-AI-Automation project.*
