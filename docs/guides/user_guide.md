# User Guide

Welcome to SASDS! This guide will help you get started with the AI-powered IDE.

## Getting Started

1. **Access the IDE**: Open `http://localhost:5173` in your browser.
2. **First Launch**: You will see a clean workspace with a "Requirements" input.

## Features

### 1. Generating a Project
- Navigate to the **Requirements** tab.
- Enter a description of your project (e.g., "A todo app using React and Python").
- Click **Analyze** to get a breakdown of the requirements.
- Click **Generate** to start the coding process.
- Watch as the file explorer populates in real-time!

### 2. Viewing and Editing Code
- Click any file in the **Explorer** to open it.
- The editor supports syntax highlighting for most languages.
- Changes are saved automatically to memory (download to disk feature coming soon).

### 3. Refining Code
- Open a file in the editor.
- Click the **Wand Icon (Refine)** in the top right.
- Type instructions like "Add comments" or "Fix the bug in line 10".
- Click **Apply Changes** to let the AI update the code.

### 4. Agent Chat
- Stuck? Switch to the **Agent Chat** tab on the left.
- Ask questions like "How do I run this?" or " explain this file".
- The agent knows what file you are looking at and can provide context-aware help.

### 5. Auto-Pilot
- Click the **Bot Icon** in the header.
- The system will analyze your entire project for bugs and improvements.
- Review the suggestions and apply them manually or via Chat.

## Troubleshooting

- **"Backend Offline"**: Ensure the backend container is running (`docker compose ps`).
- **"Auto-Pilot Failed"**: Check your Gemini API key in `backend/.env`.
- **"Terminal Disconnected"**: Refresh the page to reconnect the WebSocket.
