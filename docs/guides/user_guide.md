# 📖 User Guide

> SASDS — Getting Started & Using the AI-Powered IDE

---

## Welcome to SASDS

SASDS (Single Agent Software Development System) is your AI-powered development partner. This guide walks you through every feature of the IDE.

---

## Getting Started

### 1. Access the IDE

Open your browser and navigate to:
```
http://localhost:5173
```

### 2. First Launch

You'll see a clean workspace with:
- **Left sidebar**: Requirements input / File Explorer / Agent Chat
- **Center**: Code editor (Monaco Editor)
- **Bottom**: Collapsible terminal panel
- **Top**: Action buttons (Auto-Pilot, Settings)

---

## Feature Guide

### 🏗️ Step 1: Generating a Project

1. Navigate to the **Requirements** tab in the left sidebar
2. Enter a description of your project in plain English:
   ```
   Build a REST API for managing a book library with
   title, author, ISBN. Include CRUD operations and
   search by author.
   ```
3. Click **🔍 Analyze** to get a structured breakdown:
   - Modules identified
   - Data entities and attributes
   - API endpoints suggested
   - Tech stack recommendations
   - Missing information flags
4. Review the analysis and click **⚡ Generate Code**
5. Watch as files appear in the File Explorer in real-time!

> **💡 Tip:** The more detailed your requirements, the better the generated code. Include specifics like authentication needs, database preferences, and edge cases.

---

### 📝 Step 2: Viewing and Editing Code

1. Click any file in the **File Explorer** to open it in the editor
2. The editor provides:
   - **Syntax highlighting** for Python, JavaScript, TypeScript, HTML, CSS, JSON, and more
   - **Line numbers** and **minimap** for navigation
   - **Auto-completion** and **bracket matching**
3. Edit code directly — changes update in memory immediately

---

### ✨ Step 3: Refining Code with AI

1. Open a file in the editor
2. Click the **✨ Wand Icon** (Refine) in the editor toolbar
3. Enter natural language instructions:
   - `"Add input validation to all endpoints"`
   - `"Add docstrings to every function"`
   - `"Fix the bug on line 15"`
   - `"Convert this to use async/await"`
4. Click **Apply Changes**
5. The AI modifies the code and shows an explanation of the changes

---

### 💬 Step 4: Using Agent Chat

1. Switch to the **💬 Agent Chat** tab in the left sidebar
2. Ask questions about your code:
   - `"What does the main.py file do?"`
   - `"How do I add authentication?"`
   - `"Explain the database schema"`
   - `"Write a test for the create_user endpoint"`
3. The agent knows:
   - Which file you currently have open
   - The full project structure
   - Your conversation history

> **💡 Tip:** The agent provides the best answers when you have a file open — it uses the file content as context.

---

### 🤖 Step 5: Running Auto-Pilot

1. Click the **🤖 Bot Icon** in the top header bar
2. The system scans your **entire project** and identifies:
   - 🔴 **High severity**: Critical bugs and security vulnerabilities
   - 🟡 **Medium severity**: Code quality issues and potential bugs
   - 🟢 **Low severity**: Style improvements and best practices
3. Each finding includes:
   - The affected file and line number
   - A description of the issue
   - A specific suggestion for how to fix it
4. Additionally, you'll see **improvement recommendations**:
   - Refactoring opportunities
   - Missing features
   - Security enhancements

---

### 💻 Step 6: Using the Terminal

1. Click the **Terminal** toggle at the bottom of the IDE
2. You get a full shell session:
   ```bash
   $ ls                    # View files
   $ python main.py        # Run scripts
   $ pip install requests  # Install packages
   $ pytest                # Run tests
   ```
3. The terminal supports:
   - Tab completion
   - Command history (arrow keys)
   - Colored output (ANSI codes)
   - Window resizing

---

### 📁 Step 7: Managing Files

**File Explorer Context Menu** (right-click):

| Action | Description |
|---|---|
| **📄 New File** | Create a new file in the selected directory |
| **📁 New Folder** | Create a new directory |
| **✏️ Rename** | Rename a file or folder |
| **🗑️ Delete** | Delete a file or folder |

---

## Keyboard Shortcuts

| Shortcut | Action |
|---|---|
| `Ctrl/Cmd + S` | Save current file |
| `Ctrl/Cmd + F` | Find in file |
| `Ctrl/Cmd + H` | Find and replace |
| `Ctrl/Cmd + /` | Toggle line comment |
| `Alt + Up/Down` | Move line up/down |

---

## Troubleshooting

| Problem | Solution |
|---|---|
| **"Backend Offline"** | Ensure the backend is running: `docker compose ps` |
| **Code not generating** | Check your `GEMINI_API_KEY` in `backend/.env` |
| **Auto-Pilot failed** | Verify API key and check backend logs |
| **Terminal disconnected** | Refresh the page to reconnect WebSocket |
| **Editor blank** | Try closing and reopening the file tab |
| **Files not appearing** | Wait for streaming to complete, then refresh File Explorer |

---

## Best Practices

1. **Be specific** in requirements — include data models, endpoints, and edge cases
2. **Use Auto-Pilot regularly** — catch issues early
3. **Leverage Chat** for understanding — ask the agent to explain complex code
4. **Iterate with Refine** — use targeted instructions rather than regenerating everything
5. **Test in Terminal** — run the generated code to verify it works
