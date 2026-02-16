class CalculatorError(Exception):
    """Base exception for calculator-related errors."""
    pass

class DivisionByZeroError(CalculatorError):
    """Raised when an attempt is made to divide by zero."""
    def __init__(self, message="Cannot divide by zero."):
        self.message = message
        super().__init__(self.message)

class InvalidOperationError(CalculatorError):
    """Raised when an unsupported or invalid operation is requested."""
    def __init__(self, operation, supported_operations):
        self.message = (
            f"Invalid operation: '{operation}'. "
            f"Supported operations are: {', '.join(supported_operations)}."
        )
        super().__init__(self.message)
