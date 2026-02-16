# Task Manager API

A simple and modular task manager API built with FastAPI, SQLAlchemy (async), and Pydantic.

## Features

*   Create, Read, Update, Delete (CRUD) tasks.
*   Uses a clean, layered architecture (Repository, Service, API).
*   Asynchronous database operations.
*   Pydantic for data validation and serialization.
*   Configured for local SQLite database.

## Project Structure

```
task_manager_api/
├── main.py                  # FastAPI application entry point
├── core/
│   ├── config.py            # Application configuration
│   └── database.py          # Database setup and session management
├── api/
│   ├── router.py            # Main API router, aggregates versioned endpoints
│   └── v1/
│       ├── endpoints/
│       │   └── tasks.py     # API endpoints for tasks (CRUD operations)
│       └── schemas/
│           └── tasks.py     # Pydantic models for request/response bodies
├── models/
│   └── tasks.py             # SQLAlchemy ORM models for database tables
├── repositories/
│   └── tasks.py             # Data access layer for tasks (CRUD with database)
├── services/
│   └── tasks.py             # Business logic layer for tasks (orchestrates repositories)
├── .env.example             # Example environment variables
├── requirements.txt         # Project dependencies
└── README.md                # This file
```

## Setup and Installation

1.  **Clone the repository:**
    ```bash
    git clone <repository-url>
    cd task_manager_api
    ```

2.  **Create and activate a virtual environment:**
    ```bash
    python -m venv venv
    # On Windows
    .\venv\Scripts\activate
    # On macOS/Linux
    source venv/bin/activate
    ```

3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Create a `.env` file:**
    Copy the `.env.example` file to `.env` in the project root and customize it if needed.
    ```bash
    cp .env.example .env
    ```
    The default `DATABASE_URL` uses a local SQLite file named `task_manager.db`.

5.  **Run the application:**
    ```bash
    uvicorn main:app --reload
    ```
    The API will be available at `http://127.0.0.1:8000`.

## API Documentation

Once the server is running, you can access the interactive API documentation (Swagger UI) at:
`http://127.0.0.1:8000/docs`

## Endpoints

### Tasks (`/api/v1/tasks`)

*   **`POST /api/v1/tasks/`**
    *   Create a new task.
    *   Request Body: `TaskCreate`
    *   Response: `TaskResponse` (201 Created)

*   **`GET /api/v1/tasks/`**
    *   Retrieve a list of all tasks.
    *   Query Parameters: `skip` (int, default 0), `limit` (int, default 100)
    *   Response: `list[TaskResponse]`

*   **`GET /api/v1/tasks/{task_id}`**
    *   Retrieve a single task by its ID.
    *   Response: `TaskResponse` or 404 Not Found

*   **`PUT /api/v1/tasks/{task_id}`**
    *   Update an existing task.
    *   Request Body: `TaskUpdate` (partial updates allowed)
    *   Response: `TaskResponse` or 404 Not Found

*   **`DELETE /api/v1/tasks/{task_id}`**
    *   Delete a task by its ID.
    *   Response: 204 No Content or 404 Not Found

## Next Steps / Enhancements

*   **Database Migrations:** Implement Alembic for managing database schema changes.
*   **Authentication/Authorization:** Add user accounts and protect endpoints.
*   **Error Handling:** More granular error responses.
*   **Testing:** Comprehensive unit and integration tests.
*   **Deployment:** Dockerize the application and set up for cloud deployment.
