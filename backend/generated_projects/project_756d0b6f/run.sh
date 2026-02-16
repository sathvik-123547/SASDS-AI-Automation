#!/bin/bash
# Check if .env file exists, if not, create a default one
if [ ! -f .env ]; then
  echo "DATABASE_URL=sqlite:///./sql_app.db" > .env
  echo ".env file created with default SQLite database URL."
fi

# Run database initialization
python -c "from app.db.init_db import init_db; init_db()"

# Start Uvicorn server
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
