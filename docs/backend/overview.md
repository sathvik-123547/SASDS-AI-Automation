# Backend Documentation

The SASDS backend is a high-performance, asynchronous API built with **FastAPI**. It orchestrates all AI operations, file system management, and terminal sessions.

## Directory Structure

- `app/main.py`: Application entry point and configuration.
- `app/routers/`: API route handlers (Controllers).
- `app/services/`: Business logic and AI integration.
- `app/models/`: Pydantic data models.
- `app/utils/`: Helper functions.

## Key Services

### 1. Code Generation (`services/code_generator.py`)
- **Function**: `generate_code_with_gemini_stream`
- **Description**: Streams generated code chunks. Uses a specialized system prompt to enforce a specific output format (`### FILE: path ... ### END FILE ###`) for easy parsing.

### 2. Auto-Pilot (`services/auto_pilot.py`)
- **Function**: `analyze_project_structure`
- **Description**: Reads the entire project context and prompts Gemini to identify bugs, security issues, and improvements. Returns structured JSON.

### 3. Chat Agent (`services/chat_agent.py`)
- **Function**: `chat_with_agent`
- **Description**: Maintains a conversation history and injects current file context and project structure into the prompt for context-aware responses.

### 4. Terminal (`routers/terminal.py`)
- **Protocol**: WebSocket
- **Description**: Uses Python's `pty` module to spawn a pseudo-terminal. Connects stdin/stdout to a WebSocket for real-time shell interaction.

## API Endpoints

### Code Generation
- `POST /code/generate/stream`: Stream generated code based on requirements.
- `POST /refine/`: Refine existing code based on instructions.

### File System
- `POST /files/create`: Create a file or directory.
- `DELETE /files/delete`: Delete a file or directory.
- `PUT /files/rename`: Rename a file or directory.

### Analysis & Chat
- `POST /requirements/analyze`: Analyze requirements before generation.
- `POST /autopilot/analyze`: Run full project analysis.
- `POST /chat/send`: Send a message to the AI agent.

### System
- `GET /ping`: Health check.
