from src.calculator.errors import DivisionByZeroError, InvalidOperationError

def add(a: float, b: float) -> float:
    """Adds two numbers."""
    return a + b

def subtract(a: float, b: float) -> float:
    """Subtracts the second number from the first."""
    return a - b

def multiply(a: float, b: float) -> float:
    """Multiplies two numbers."""
    return a * b

def divide(a: float, b: float) -> float:
    """Divides the first number by the second. Raises DivisionByZeroError if b is zero."""
    if b == 0:
        raise DivisionByZeroError()
    return a / b

# Dictionary to map operation strings to functions
OPERATIONS = {
    "add": add,
    "subtract": subtract,
    "multiply": multiply,
    "divide": divide,
}

def calculate(operation: str, num1: float, num2: float) -> float:
    """
    Performs the specified arithmetic operation on two numbers.

    Args:
        operation (str): The name of the operation (e.g., "add", "subtract").
        num1 (float): The first number.
        num2 (float): The second number.

    Returns:
        float: The result of the operation.

    Raises:
        InvalidOperationError: If the operation is not supported.
        DivisionByZeroError: If division by zero occurs.
    """
    op_func = OPERATIONS.get(operation)
    if not op_func:
        raise InvalidOperationError(operation, list(OPERATIONS.keys()))
    return op_func(num1, num2)
