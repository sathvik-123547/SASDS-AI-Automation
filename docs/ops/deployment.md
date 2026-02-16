# Deployment Guide

This guide describes how to deploy SASDS using Docker and Docker Compose.

## Prerequisites

- Docker Engine 20.10+
- Docker Compose v2.0+
- A Google Gemini API Key

## Configuration

1. Set your `GEMINI_API_KEY` in `backend/.env` or as an environment variable.

```bash
export GEMINI_API_KEY="your_api_key_here"
```

## Running with Docker Compose

To start the entire stack (Frontend + Backend + Nginx):

```bash
docker compose up --build -d
```

- **Frontend**: Accessible at `http://localhost:5173`
- **Backend**: API accessible at `http://localhost:8000`

## Container Architecture

- **Backend Container**:
    - Image: Python 3.9-slim
    - Exposed Port: 8000
    - Volume: `backend/generated_projects` mapped to host for persistence.
    - Command: `uvicorn app.main:app --host 0.0.0.0 --port 8000`

- **Frontend Container**:
    - Image: Node 18-alpine
    - Exposed Port: 5173
    - Command: `npm run dev -- --host 0.0.0.0`

## Production Considerations

For a production environment, you should:

1. **Use Nginx as a Reverse Proxy**: Serve the frontend static files and proxy `/api/*` requests to the backend container.
2. **Secure WebSocket Connections**: Ensure `wss://` is used for terminal connections.
3. **Persist Data**: Use named Docker volumes for `generated_projects`.
4. **Environment Variables**: Use Docker secrets or a `.env` file not committed to git.
