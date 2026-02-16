# 📋 Changelog

> All notable changes to the SASDS project are documented in this file.
>
> This format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).

---

## [0.1.0] — 2026-02-16

### 🎉 Initial Release

#### Added — Core IDE

- **Monaco Editor** integration for VS Code-like code editing experience
- **File Explorer** with recursive tree rendering and context menus (create, rename, delete)
- **Tab System** for working with multiple files simultaneously
- **Dark Theme** with TailwindCSS and Shadcn/UI design system
- **Error Boundary** component for graceful error handling

#### Added — AI-Powered Code Generation

- **Requirements Analysis** — natural language to structured modules, entities, APIs
- **Streaming Code Generation** — real-time code output with `### FILE:` delimiter protocol
- **Batch Code Generation** — complete JSON response with all generated files
- **Code Refinement** — targeted AI modifications to individual files

#### Added — Intelligent Assistants

- **Auto-Pilot** — full project analysis for bugs, security issues, and improvements
- **Agent Chat** — context-aware conversational AI assistant
- **Code Review** — structured review with severity-rated issues and recommendations
- **Self-Correction Engine** — automatic test-fix loop (up to 3 iterations)
- **Test Generator** — automated pytest test generation

#### Added — Developer Tools

- **Interactive Terminal** — full PTY-backed xterm.js terminal via WebSocket
- **GitHub Sync** — push generated projects to GitHub repositories
- **Project Download** — export projects as ZIP archives

#### Added — Infrastructure

- **Docker Compose** setup with 4 services (backend, frontend, PostgreSQL, Redis)
- **CI/CD Pipeline** via GitHub Actions (lint, type check, test, Docker build)
- **FastAPI Backend** with CORS, request logging, and global error handling
- **Google Gemini 2.5 Flash** integration for all AI operations

#### Added — Documentation

- System Architecture with Mermaid diagrams
- Technical Design Document
- Complete API Reference
- Backend and Frontend overviews
- Deployment Guide
- User Guide
- Contributing Guide
- Security Policy
