# Frontend Documentation

The SASDS frontend is a modern React application built with TypeScript, Vite, and TailwindCSS. It provides a rich, IDE-like experience within the browser.

## Tech Stack

- **React 18**: Component-based UI library.
- **Vite**: Next-generation frontend tooling.
- **TypeScript**: Strict syntactical superset of JavaScript.
- **TailwindCSS**: Utility-first CSS framework.
- **Shadcn/UI**: Reusable component primitives (Radix UI).
- **Monaco Editor**: The VS Code editor for the web.
- **xterm.js**: Full-featured terminal emulator.

## Project Structure

- `src/components/`: Reusable UI components.
    - `ui/`: Shadcn/UI primitives (Button, Card, etc.).
    - `CodeViewer.tsx`: The main editing component (monaco-editor).
    - `FileExplorer.tsx`: Recursive file tree component.
    - `Terminal.tsx`: xterm.js wrapper.
    - `ChatInterface.tsx`: The conversational agent UI.
- `src/api/`: API client functions (`client.ts`).
- `src/lib/`: Utility functions (`utils.ts`, `stream-parser.ts`).
- `src/types.ts`: TypeScript interfaces and types.

## Key Features

### 1. Code Editor (`CodeViewer.tsx`)
- Uses `@monaco-editor/react`.
- Supports multiple languages based on file extension.
- **Refinement**: Integrated "Wand" tool allows users to highlight code and ask AI to modify it.

### 2. File Explorer (`FileExplorer.tsx`)
- recursive rendering of file tree.
- context menu for file operations (create, delete, rename).
- updates in real-time as code is generated.

### 3. Agent Chat (`ChatInterface.tsx`)
- Provides a chat interface to interact with the AI agent.
- Sends current file context and project structure with each message.
- Supports markdown rendering for code blocks.

### 4. Real-time Streaming (`stream-parser.ts`)
- Custom parser to handle the delimited stream from the backend.
- Updates the file system state incrementally as chunks arrive.

## State Management

- `App.tsx` serves as the main state orchestrator.
- **Local State**: `useState` is used for UI state (tabs, modals).
- **Project State**: `codeResult` holds the current project file structure.
- **Streaming State**: A mutable `ref` buffer accumulates incoming text for parsing.

## Theming

- Dark mode by default (`index.css`).
- Custom color palette defined in `tailwind.config.js`.
- Consistent design language via Shadcn/UI components.
