# Basic Calculator Backend

This project provides a clean and modular Python backend for a basic calculator application using Flask and Pydantic.

## Features

*   **Basic Arithmetic**: Addition, Subtraction, Multiplication, Division.
*   **RESTful API**: A single `/calculate` endpoint for performing operations.
*   **Input Validation**: Uses Pydantic for robust request body validation.
*   **Error Handling**: Specific error types for common issues like division by zero or invalid operations.
*   **Modular Design**: Clear separation of concerns for calculator logic, API endpoints, and configuration.

## Project Structure

```
calculator_app/
├── src/
│   ├── api/
│   │   ├── __init__.py
│   │   ├── routes.py       # Defines Flask API endpoints
│   │   └── schemas.py      # Pydantic models for request/response validation
│   ├── calculator/
│   │   ├── __init__.py
│   │   ├── core.py         # Core calculator logic (add, subtract, etc.)
│   │   └── errors.py       # Custom exceptions for calculator operations
│   ├── app.py              # Flask application factory
│   └── config.py           # Application configuration
├── .env.example            # Example environment variables
├── requirements.txt        # Project dependencies
└── run.py                  # Entry point to run the Flask application
```

## Setup and Running

1.  **Clone the repository:**
    ```bash
    git clone <repository-url>
    cd calculator_app
    ```

2.  **Create a virtual environment and install dependencies:**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    pip install -r requirements.txt
    ```

3.  **Configure environment variables:**
    Create a `.env` file in the project root (`calculator_app/`) based on `.env.example`:
    ```bash
    cp .env.example .env
    ```
    You can modify `SECRET_KEY` and `FLASK_ENV` in `.env` if needed.

4.  **Run the application:**
    ```bash
    python run.py
    ```
    The server will typically run on `http://127.0.0.1:5000`.

## API Endpoint

### `POST /calculate`

Performs a basic arithmetic operation between two numbers.

**Request Body Example:**

```json
{
    "operation": "add",
    "num1": 10.5,
    "num2": 5.2
}
```

**Fields:**
*   `operation` (string, required): The arithmetic operation to perform.
    *   Allowed values: `"add"`, `"subtract"`, `"multiply"`, `"divide"`
*   `num1` (float, required): The first number.
*   `num2` (float, required): The second number.

**Successful Response (200 OK):**

```json
{
    "result": 15.7
}
```

**Error Responses:**

*   **400 Bad Request - Validation Error:**
    ```json
    {
        "message": "Invalid request payload.",
        "error_type": "Validation Error"
    }
    ```
    (e.g., missing fields, incorrect data types)

*   **400 Bad Request - Division By Zero Error:**
    ```json
    {
        "message": "Cannot divide by zero.",
        "error_type": "Division By Zero Error"
    }
    ```

*   **400 Bad Request - Invalid Operation Error:**
    ```json
    {
        "message": "Invalid operation: 'power'. Supported operations are: add, subtract, multiply, divide.",
        "error_type": "Invalid Operation Error"
    }
    ```

*   **500 Internal Server Error:**
    ```json
    {
        "message": "An unexpected error occurred.",
        "error_type": "Internal Server Error"
    }
    ```

## Example Usage with `curl`

**Addition:**
```bash
curl -X POST -H "Content-Type: application/json" -d '{"operation": "add", "num1": 10, "num2": 5}' http://127.0.0.1:5000/calculate
```

**Division:**
```bash
curl -X POST -H "Content-Type: application/json" -d '{"operation": "divide", "num1": 100, "num2": 25}' http://127.0.0.1:5000/calculate
```

**Division by Zero (Error):**
```bash
curl -X POST -H "Content-Type: application/json" -d '{"operation": "divide", "num1": 10, "num2": 0}' http://127.0.0.1:5000/calculate
```

**Invalid Operation (Error):**
```bash
curl -X POST -H "Content-Type: application/json" -d '{"operation": "power", "num1": 2, "num2": 3}' http://127.0.0.1:5000/calculate
```
