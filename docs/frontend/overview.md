# 🎨 Frontend Documentation

> SASDS Frontend — Modern React IDE Experience

---

## Overview

The SASDS frontend is a feature-rich, browser-based IDE built with **React 18**, **TypeScript**, and **Vite**. It provides a professional coding experience with a Monaco Editor, interactive terminal, file explorer, and AI chat — all within a dark-themed, VS Code-inspired interface.

---

## Tech Stack

| Technology | Version | Purpose |
|---|---|---|
| **React** | 18.3+ | Component-based UI library |
| **TypeScript** | 5.6+ | Type-safe JavaScript superset |
| **Vite** | 6.0+ | Build tool & dev server |
| **TailwindCSS** | 3.4+ | Utility-first styling |
| **Shadcn/UI** | Latest | Radix-based component primitives |
| **Monaco Editor** | 4.7+ | VS Code editor for the web |
| **xterm.js** | 5.3+ | Terminal emulator |
| **Lucide React** | 0.330+ | Icon library |

---

## Project Structure

```
frontend/src/
├── App.tsx                   # Main app + state orchestrator (576 lines)
├── main.tsx                  # React entry point
├── types.ts                  # TypeScript interfaces & types
├── vite-env.d.ts             # Vite type declarations
├── index.css                 # Global styles + TailwindCSS
│
├── components/
│   ├── CodeViewer.tsx        # Monaco Editor wrapper with refinement
│   ├── FileExplorer.tsx      # Recursive file tree with context menu
│   ├── Terminal.tsx           # xterm.js WebSocket terminal
│   ├── ChatInterface.tsx     # AI agent chat panel
│   ├── ErrorBoundary.tsx     # React error boundary
│   └── ui/
│       ├── button.tsx        # Shadcn button component
│       └── card.tsx          # Shadcn card component
│
├── api/
│   └── client.ts             # HTTP & streaming API client
│
└── lib/
    ├── utils.ts              # Utility functions (cn, class merging)
    ├── stream-parser.ts      # Streaming delimiter parser
    └── file-utils.ts         # File tree builder utility
```

---

## Component Architecture

![Component Architecture](../images/component_hierarchy.png)

---

## Key Components

### 1. CodeViewer (`CodeViewer.tsx`)

The primary code editing component powered by Monaco Editor.

| Feature | Description |
|---|---|
| **Multi-language** | Auto-detects language from file extension |
| **Dark Theme** | `vs-dark` theme matching IDE aesthetic |
| **Refinement Tool** | Integrated "Wand" button for AI-powered code modifications |
| **Auto-save** | Changes propagated to parent state on edit |
| **Read-only Mode** | Supports view-only mode for generated code |

### 2. FileExplorer (`FileExplorer.tsx`)

A recursive file tree component with project management capabilities.

| Feature | Description |
|---|---|
| **Tree Rendering** | Recursive rendering of nested directories and files |
| **Context Menu** | Right-click for Create File, Create Folder, Rename, Delete |
| **Real-time Updates** | Tree updates live as streaming code arrives |
| **Icon Mapping** | File-type icons for visual clarity |
| **Click-to-Open** | Single click opens file in CodeViewer |

### 3. Terminal (`Terminal.tsx`)

Full-featured terminal emulator connected to the backend via WebSocket.

| Feature | Description |
|---|---|
| **xterm.js** | Complete terminal emulation with ANSI escape code support |
| **Fit Addon** | Auto-resizes terminal to container dimensions |
| **WebSocket** | Real-time bidirectional communication with backend PTY |
| **Input/Output** | Full shell access (cd, ls, python, npm, etc.) |
| **Resize Events** | Sends terminal dimensions to backend for proper rendering |

### 4. ChatInterface (`ChatInterface.tsx`)

Conversational AI assistant panel.

| Feature | Description |
|---|---|
| **Message History** | Scrollable chat history with user/AI messages |
| **Context Injection** | Sends current file path, content, and project structure |
| **Markdown Support** | AI responses rendered with code block formatting |
| **Auto-scroll** | Automatically scrolls to latest message |

### 5. ErrorBoundary (`ErrorBoundary.tsx`)

React error boundary that catches rendering errors and displays a fallback UI instead of a white screen.

---

## State Management

All application state lives in `App.tsx` using React's `useState` and `useRef` hooks:

| State | Type | Purpose |
|---|---|---|
| `requirementsText` | `string` | User's natural language input |
| `analysis` | `RequirementAnalysisResponse` | Structured requirements breakdown |
| `codeResult` | `CodeGenerationResponse` | Generated project files |
| `selectedFile` | `GeneratedFile` | Currently open file in editor |
| `openTabs` | `GeneratedFile[]` | Open editor tabs |
| `chatHistory` | `ChatMessage[]` | Agent conversation history |
| `autoPilotResult` | `AutoPilotResponse` | Project analysis results |
| `streamBuffer` | `useRef<string>` | Mutable buffer for stream parsing |

### State Flow
```
User Input → API Call → State Update → Component Re-render → UI Update
```

---

## Styling & Theming

- **Dark Mode** by default via `index.css` and TailwindCSS
- **Custom Color Palette** defined in `tailwind.config.cjs`
- **Shadcn/UI** primitives for consistent design language
- **CSS Variables** for theme customization

### Key Theme Colors
| Purpose | Class |
|---|---|
| Background | `bg-zinc-950` |
| Surface | `bg-zinc-900` |
| Border | `border-zinc-800` |
| Primary | `bg-indigo-600` |
| Text | `text-zinc-100` |
| Muted | `text-zinc-400` |

---

## API Client (`api/client.ts`)

Centralized API client for all backend communication:

| Method | Endpoint | Returns |
|---|---|---|
| `analyzeRequirements()` | `POST /requirements/analyze` | `RequirementAnalysisResponse` |
| `generateCode()` | `POST /code/generate` | `CodeGenerationResponse` |
| `generateCodeStream()` | `POST /code/generate/stream` | `ReadableStream` |
| `refineCode()` | `POST /refine/` | `RefinementResponse` |
| `analyzeProject()` | `POST /autopilot/analyze` | `AutoPilotResponse` |
| `sendChatMessage()` | `POST /chat/send` | `ChatMessage` |

---

## Stream Parser (`lib/stream-parser.ts`)

Custom parser for the streaming code generation protocol:

```
Input:  "### FILE: path\ncontent\n### END FILE ###"
Output: { path: "path", content: "content" }
```

The parser incrementally processes text chunks, detecting file boundaries and updating state as new files are discovered.

---

## Build & Development

### Development Server
```bash
cd frontend
npm install
npm run dev
```
Access at: `http://localhost:5173`

### Production Build
```bash
npm run build
```
Output in `frontend/dist/` — served via Nginx in Docker.

### Type Checking
```bash
npx tsc --noEmit
```
