# 📡 API Reference

> SASDS Backend — Complete REST & WebSocket API

**Base URL:** `http://localhost:8000`

---

## Table of Contents

- [Health Check](#health-check)
- [Requirements Analysis](#requirements-analysis)
- [Code Generation](#code-generation)
- [Code Refinement](#code-refinement)
- [Auto-Pilot](#auto-pilot)
- [Agent Chat](#agent-chat)
- [File Operations](#file-operations)
- [Project Management](#project-management)
- [Terminal (WebSocket)](#terminal-websocket)
- [Error Handling](#error-handling)

---

## Health Check

### `GET /ping`

Verify that the backend is running.

**Response:**
```json
{
    "message": "Backend is running successfully!"
}
```

**Example:**
```bash
curl http://localhost:8000/ping
```

---

## Requirements Analysis

### `POST /requirements/analyze`

Analyze natural language requirements and return a structured breakdown of modules, entities, APIs, and tech stack suggestions.

**Request Body:**
```json
{
    "requirements_text": "Build a task management app with user authentication, CRUD operations for tasks, and a REST API"
}
```

**Response (`RequirementAnalysisResponse`):**
```json
{
    "modules": [
        { "name": "auth", "description": "User authentication and authorization" },
        { "name": "tasks", "description": "Task CRUD operations" }
    ],
    "entities": [
        { "name": "User", "attributes": ["id", "email", "password_hash", "created_at"] },
        { "name": "Task", "attributes": ["id", "title", "description", "status", "user_id"] }
    ],
    "apis": [
        { "name": "Create Task", "method": "POST", "path": "/api/tasks", "description": "Create a new task" },
        { "name": "List Tasks", "method": "GET", "path": "/api/tasks", "description": "Get all tasks for a user" }
    ],
    "non_functional_requirements": ["Authentication required", "Input validation"],
    "tech_stack_suggestions": ["FastAPI", "SQLAlchemy", "JWT"],
    "missing_information": ["Database preference?", "Role-based access control needed?"]
}
```

**Example:**
```bash
curl -X POST http://localhost:8000/requirements/analyze \
  -H "Content-Type: application/json" \
  -d '{"requirements_text": "Build a todo app with REST API"}'
```

---

## Code Generation

### `POST /code/generate`

Generate project code files based on requirements (batch mode — returns complete JSON).

**Request Body (`CodeGenerationRequest`):**
```json
{
    "requirements_text": "A REST API for managing books with title, author, and ISBN",
    "analysis": null
}
```

> **Note:** `analysis` is optional. Pass the output from `/requirements/analyze` to provide the AI with a structured breakdown.

**Response (`CodeGenerationResponse`):**
```json
{
    "files": [
        {
            "path": "backend/app/main.py",
            "description": "FastAPI application entry point",
            "content": "from fastapi import FastAPI\n\napp = FastAPI()\n..."
        },
        {
            "path": "backend/app/models/book.py",
            "description": "Book data model",
            "content": "from pydantic import BaseModel\n..."
        }
    ]
}
```

---

### `POST /code/generate/stream`

Stream generated code as text chunks in real-time. Uses the custom delimiter protocol.

**Request Body:** Same as `POST /code/generate`

**Response:** `text/plain` stream using delimiter format:

```
### FILE: backend/app/main.py
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def root():
    return {"message": "Hello World"}
### END FILE ###

### FILE: backend/app/models/book.py
from pydantic import BaseModel

class Book(BaseModel):
    title: str
    author: str
    isbn: str
### END FILE ###
```

**Example:**
```bash
curl -X POST http://localhost:8000/code/generate/stream \
  -H "Content-Type: application/json" \
  -d '{"requirements_text": "A simple hello world API"}' \
  --no-buffer
```

---

## Code Refinement

### `POST /refine/`

Refine an existing file based on natural language instructions.

**Request Body (`RefinementRequest`):**
```json
{
    "path": "backend/app/main.py",
    "content": "from fastapi import FastAPI\n\napp = FastAPI()\n",
    "instructions": "Add a /health endpoint that returns status ok"
}
```

**Response (`RefinementResponse`):**
```json
{
    "path": "backend/app/main.py",
    "new_content": "from fastapi import FastAPI\n\napp = FastAPI()\n\n@app.get(\"/health\")\ndef health():\n    return {\"status\": \"ok\"}\n",
    "explanation": "Added a GET /health endpoint that returns a JSON status object."
}
```

---

## Auto-Pilot

### `POST /autopilot/analyze`

Trigger a full project analysis. The AI scans all project files and identifies bugs, security issues, and improvements.

**Request Body:**
```json
{
    "project_id": "my-project-123"
}
```

**Response (`AutoPilotResponse`):**
```json
{
    "summary": "The project has a solid foundation but has 3 security issues and 2 potential bugs.",
    "issues": [
        {
            "severity": "high",
            "file": "app/main.py",
            "line": 15,
            "description": "SQL injection vulnerability in query builder",
            "suggestion": "Use parameterized queries instead of string concatenation"
        },
        {
            "severity": "medium",
            "file": "app/auth.py",
            "line": 8,
            "description": "Hardcoded secret key",
            "suggestion": "Move to environment variable"
        }
    ],
    "improvements": [
        {
            "type": "refactor",
            "description": "Extract database operations into a repository pattern",
            "file": "app/main.py"
        },
        {
            "type": "security",
            "description": "Add rate limiting to API endpoints"
        }
    ]
}
```

---

## Agent Chat

### `POST /chat/send`

Send a message to the context-aware AI agent. The agent knows about the currently opened file and project structure.

**Request Body (`ChatRequest`):**
```json
{
    "message": "How do I add authentication to this API?",
    "history": [
        { "role": "user", "content": "What does this file do?" },
        { "role": "model", "content": "This file defines the main FastAPI application..." }
    ],
    "context": {
        "selected_file_path": "backend/app/main.py",
        "selected_file_content": "from fastapi import FastAPI\n...",
        "project_structure": "backend/app/main.py\nbackend/app/models/user.py\n..."
    }
}
```

**Response:**
```json
{
    "role": "model",
    "content": "To add authentication, I recommend using JWT tokens with FastAPI's security utilities..."
}
```

> **Note:** `context` is optional but recommended. It allows the agent to provide file-aware and project-aware responses.

---

## File Operations

### `POST /files/create`

Create a file or directory.

**Request Body:**
```json
{
    "path": "my-project/src/utils.py",
    "content": "# Utility functions\n",
    "is_directory": false
}
```

**Response:**
```json
{
    "message": "File created: my-project/src/utils.py"
}
```

---

### `DELETE /files/delete`

Delete a file or directory.

**Request Body:**
```json
{
    "path": "my-project/src/old_file.py"
}
```

**Response:**
```json
{
    "message": "Deleted: my-project/src/old_file.py"
}
```

---

### `PUT /files/rename`

Rename or move a file or directory.

**Request Body:**
```json
{
    "old_path": "my-project/src/utils.py",
    "new_path": "my-project/src/helpers.py"
}
```

**Response:**
```json
{
    "message": "Renamed my-project/src/utils.py to my-project/src/helpers.py"
}
```

---

## Project Management

### `GET /projects/`

List all generated projects.

**Response:**
```json
{
    "projects": [
        {
            "project_id": "todo-app-2026",
            "project_path": "/app/generated_projects/todo-app-2026",
            "created_at": "2026-02-16T10:30:00"
        }
    ]
}
```

---

### `GET /projects/{project_id}/download`

Download a generated project as a ZIP archive.

**Response:** Binary ZIP file download.

**Example:**
```bash
curl -O http://localhost:8000/projects/todo-app-2026/download
```

---

## Terminal (WebSocket)

### `WS /terminal/ws`

Open an interactive terminal session via WebSocket. Provides full shell access through a pseudo-terminal (PTY).

**Connection:**
```javascript
const ws = new WebSocket("ws://localhost:8000/terminal/ws");
```

**Client → Server Messages:**

| Type | Format | Description |
|---|---|---|
| **Input** | `{"type": "input", "data": "ls -la\n"}` | Send keystrokes to the shell |
| **Resize** | `{"type": "resize", "cols": 80, "rows": 24}` | Resize the terminal window |

**Server → Client Messages:**

Raw text output from the shell (decoded from PTY stdout).

**Example (JavaScript):**
```javascript
const ws = new WebSocket("ws://localhost:8000/terminal/ws");

ws.onopen = () => {
    // Send a command
    ws.send(JSON.stringify({ type: "input", data: "echo Hello World\n" }));
};

ws.onmessage = (event) => {
    console.log("Terminal output:", event.data);
};
```

---

## Error Handling

All errors return a consistent JSON format:

```json
{
    "detail": "Human-readable error description"
}
```

### HTTP Status Codes

| Code | Meaning | When |
|---|---|---|
| `200` | Success | Request completed successfully |
| `400` | Bad Request | Invalid input (empty requirements, missing fields) |
| `403` | Forbidden | Path traversal attempt in file operations |
| `404` | Not Found | File or project does not exist |
| `409` | Conflict | Rename destination already exists |
| `500` | Internal Server Error | Gemini API failure, JSON parse error, or unhandled exception |
