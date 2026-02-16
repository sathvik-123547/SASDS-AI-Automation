# Todo Application Backend

This is a clean and modular Python backend for a simple Todo application, built with FastAPI and SQLModel.

## Features

- Create, Read, Update, Delete (CRUD) todo items.
- RESTful API endpoints.
- Data validation and serialization using Pydantic/SQLModel.
- Database integration with SQLite (easy to switch to PostgreSQL/MySQL).
- Modular project structure for easy maintenance and scalability.

## Project Structure

```
.
├── .env                  # Environment variables for configuration
├── .gitignore            # Files to ignore in Git
├── README.md             # This file
├── requirements.txt      # Project dependencies
├── main.py               # Main FastAPI application entry point
├── core/
│   ├── __init__.py
│   ├── config.py         # Application settings
│   └── database.py       # Database engine and session setup
├── models/
│   ├── __init__.py
│   └── todo.py           # SQLModel definition for Todo items
├── schemas/
│   ├── __init__.py
│   └── todo.py           # Pydantic schemas for Todo requests/responses
├── crud/
│   ├── __init__.py
│   └── todo.py           # CRUD operations (database interactions) for Todo items
└── api/
    └── v1/
        ├── __init__.py
        └── endpoints/
            ├── __init__.py
            └── todo.py   # API endpoints for Todo resources
```

## Setup and Installation

1.  **Clone the repository (if applicable):**
    ```bash
    # git clone <your-repo-url>
    # cd <your-project-directory>
    ```

2.  **Create a virtual environment (recommended):**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```

3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Configure Environment Variables:**
    Create a `.env` file in the project root with the following content:
    ```
    DATABASE_URL=sqlite:///./sql_app.db
    ```
    This configures a SQLite database named `sql_app.db` in the project root.

5.  **Run the application:**
    ```bash
    uvicorn main:app --reload
    ```
    The `--reload` flag enables auto-reloading on code changes during development.

## API Documentation

Once the server is running, you can access the interactive API documentation (Swagger UI) at:
[http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

Or the ReDoc documentation at:
[http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)

## API Endpoints

### Todos

*   **`POST /api/v1/todos/`**
    *   Create a new todo item.
    *   Request Body (JSON):
        ```json
        {
          "title": "Buy groceries",
          "description": "Milk, eggs, bread",
          "completed": false
        }
        ```
    *   Response (JSON): Created todo item.

*   **`GET /api/v1/todos/`**
    *   Retrieve a list of all todo items.
    *   Query Parameters: `skip` (int, default 0), `limit` (int, default 100)
    *   Response (JSON): Array of todo items.

*   **`GET /api/v1/todos/{todo_id}`**
    *   Retrieve a specific todo item by ID.
    *   Response (JSON): The requested todo item.
    *   Returns `404 Not Found` if the todo does not exist.

*   **`PUT /api/v1/todos/{todo_id}`**
    *   Update an existing todo item by ID.
    *   Request Body (JSON):
        ```json
        {
          "title": "Buy organic groceries",
          "description": "Organic milk, eggs, bread",
          "completed": true
        }
        ```
    *   Response (JSON): The updated todo item.
    *   Returns `404 Not Found` if the todo does not exist.

*   **`DELETE /api/v1/todos/{todo_id}`**
    *   Delete a specific todo item by ID.
    *   Response (JSON): Message indicating successful deletion.
    *   Returns `404 Not Found` if the todo does not exist.

---
