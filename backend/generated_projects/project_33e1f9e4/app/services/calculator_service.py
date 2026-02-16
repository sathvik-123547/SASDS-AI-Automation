class DivisionByZeroError(Exception):
    """Custom exception for division by zero."""
    pass

class CalculatorService:
    """
    Service layer for performing basic calculator operations.
    Encapsulates the business logic.
    """

    def add(self, operand1: float, operand2: float) -> float:
        """Adds two numbers."""
        return operand1 + operand2

    def subtract(self, operand1: float, operand2: float) -> float:
        """Subtracts the second number from the first."""
        return operand1 - operand2

    def multiply(self, operand1: float, operand2: float) -> float:
        """Multiplies two numbers."""
        return operand1 * operand2

    def divide(self, operand1: float, operand2: float) -> float:
        """
        Divides the first number by the second.
        Raises DivisionByZeroError if the second operand is zero.
        """
        if operand2 == 0:
            raise DivisionByZeroError("Cannot divide by zero")
        return operand1 / operand2

