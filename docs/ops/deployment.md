# 🚀 Deployment Guide

> SASDS — Docker & Production Deployment

---

## Prerequisites

| Requirement | Version |
|---|---|
| Docker Engine | 20.10+ |
| Docker Compose | v2.0+ |
| Google Gemini API Key | — |
| Git | 2.0+ |

---

## Quick Start (Docker Compose)

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/SASDS-AI-Automation.git
cd SASDS-AI-Automation
```

### 2. Configure Environment

```bash
# Set your Gemini API key
echo "GEMINI_API_KEY=your_api_key_here" > backend/.env
```

### 3. Launch the Stack

```bash
docker compose up --build -d
```

### 4. Access the Application

| Service | URL |
|---|---|
| **Frontend (IDE)** | `http://localhost:5173` |
| **Backend API** | `http://localhost:8000` |
| **API Docs (Swagger)** | `http://localhost:8000/docs` |
| **Health Check** | `http://localhost:8000/ping` |

### 5. Verify

```bash
# Check all containers are running
docker compose ps

# Check backend health
curl http://localhost:8000/ping

# View logs
docker compose logs -f backend
```

---

## Container Architecture

![Docker Compose Architecture](images/docker_architecture.png)

| Container | Image | Port | Volume | Command |
|---|---|---|---|---|
| `sasds-frontend` | Node 18-alpine | 5173 | — | `npm run dev -- --host 0.0.0.0` |
| `sasds-backend` | Python 3.9-slim | 8000 | `./backend:/app` | `uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload` |
| `sasds-db` | postgres:15-alpine | 5432 | `postgres_data` | Default PostgreSQL |
| `sasds-redis` | redis:7-alpine | 6379 | — | Default Redis |

---

## Environment Variables

| Variable | Required | Default | Service |
|---|---|---|---|
| `GEMINI_API_KEY` | ✅ | — | Backend |
| `GEMINI_MODEL_NAME` | ❌ | `models/gemini-2.5-flash` | Backend |
| `DATABASE_URL` | ❌ | (set in compose) | Backend |
| `REDIS_URL` | ❌ | (set in compose) | Backend |
| `GITHUB_TOKEN` | ❌ | — | Backend (GitHub sync) |
| `GITHUB_REPO` | ❌ | — | Backend (GitHub sync) |
| `POSTGRES_USER` | ❌ | `sasds` | Database |
| `POSTGRES_PASSWORD` | ❌ | `sasds_password` | Database |
| `POSTGRES_DB` | ❌ | `sasds_db` | Database |

---

## Local Development (Without Docker)

### Backend

```bash
cd backend
python -m venv .venv
source .venv/bin/activate          # macOS/Linux
# .venv\Scripts\activate           # Windows
pip install -r requirements.txt
echo "GEMINI_API_KEY=your_key" > .env
uvicorn app.main:app --reload --port 8000
```

### Frontend

```bash
cd frontend
npm install
npm run dev
```

---

## Production Deployment

### Recommended Configuration

| Concern | Recommendation |
|---|---|
| **Reverse Proxy** | Use Nginx to serve frontend static files and proxy `/api/*` to backend |
| **SSL/TLS** | Enable HTTPS with Let's Encrypt or a managed certificate |
| **WebSocket** | Configure Nginx to proxy WebSocket connections (`wss://`) |
| **CORS** | Restrict `allow_origins` to your production domain |
| **Persistence** | Use named Docker volumes for `generated_projects/` |
| **Secrets** | Use Docker secrets or a vault — never commit `.env` files |
| **Monitoring** | Add health check probes to your container orchestrator |
| **Scaling** | Backend is stateless (except file system) — can scale horizontally with shared storage |

### Nginx Configuration (Reference)

The project includes `frontend/nginx.conf` for production use:

```nginx
server {
    listen 80;
    server_name localhost;

    location / {
        root /usr/share/nginx/html;
        index index.html;
        try_files $uri $uri/ /index.html;
    }

    location /api/ {
        proxy_pass http://backend:8000/;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }

    location /terminal/ws {
        proxy_pass http://backend:8000/terminal/ws;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
    }
}
```

---

## Common Operations

### Stop the Stack
```bash
docker compose down
```

### Rebuild After Changes
```bash
docker compose up --build -d
```

### View Logs
```bash
docker compose logs -f backend    # Backend logs only
docker compose logs -f             # All services
```

### Reset Database
```bash
docker compose down -v            # Removes volumes
docker compose up --build -d
```

---

## Troubleshooting

| Issue | Solution |
|---|---|
| **"Backend Offline"** | Check `docker compose ps` — ensure backend container is running |
| **"GEMINI_API_KEY not set"** | Verify `backend/.env` contains your key |
| **Port 8000 in use** | Stop conflicting services: `lsof -ti:8000 \| xargs kill -9` |
| **Port 5173 in use** | Stop conflicting services: `lsof -ti:5173 \| xargs kill -9` |
| **WebSocket disconnects** | Ensure Nginx is configured for WebSocket proxy (see above) |
| **Container build fails** | Run `docker compose build --no-cache` to force clean build |
