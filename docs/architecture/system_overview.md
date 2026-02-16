# System Architecture

## Overview

SASDS (Single Agent Software Development System) is an AI-powered IDE designed to democratize software creation. It leverages a modern tech stack to provide a seamless, agentic coding experience.

## High-Level Architecture

```mermaid
graph TD
    Client[Frontend (React/Vite)]
    LB[Nginx / Reverse Proxy]
    API[Backend API (FastAPI)]
    DB[(File System Storage)]
    
    subgraph "External Services"
        Gemini[Google Gemini 1.5 Pro]
    end

    Client -- HTTP/WebSocket --> LB
    LB --> API
    API -- Read/Write --> DB
    API -- Prompt/Response --> Gemini
```

## Core Components

### 1. Frontend (`/frontend`)
- **Framework**: React 18 with Vite.
- **Language**: TypeScript.
- **Styling**: TailwindCSS with Shadcn/UI.
- **State Management**: React Context / Local State.
- **Key Features**:
    - **Monaco Editor**: VS Code-like editing experience.
    - **Xterm.js**: Web-based terminal emulator.
    - **File Explorer**: Recursive file tree visualization.
    - **Split-Pane Layout**: Modern, adjustable IDE layout.

### 2. Backend (`/backend`)
- **Framework**: FastAPI (Python 3.9+).
- **Asynchronous**: Fully async architecture using `asyncio`.
- **Key Services**:
    - **Code Generator**: Streams code from Gemini using a custom delimiter protocol.
    - **File System API**: Handles CRUD operations on the local file system.
    - **Terminal Service**: Manages PTY sessions via WebSockets.
    - **Auto-Pilot**: Background analysis service.
    - **Agent Chat**: Context-aware conversational agent.

### 3. AI Engine
- **Model**: Google Gemini 1.5 Pro / Flash.
- **Integration**: `google-generativeai` SDK (migrating to `google-genai`).
- **Capabilities**:
    - Code Generation (Streaming)
    - Code Refinement
    - Project Analysis
    - Chat Assistance

## Data Flow

1. **Code Generation**:
   User Prompt -> Frontend -> Backend -> Gemini -> Streaming Response (Chunks) -> Frontend Parser -> File System.

2. **Terminal Interaction**:
   User Keypress -> xterm.js -> WebSocket -> Backend PTY -> Shell -> Output -> WebSocket -> Frontend.

3. **Auto-Pilot**:
   Trigger -> Backend reads all files -> Gemini Analysis -> structured JSON -> Frontend Modal.
