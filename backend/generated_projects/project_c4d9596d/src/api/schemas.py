from pydantic import BaseModel, Field

class CalculationRequest(BaseModel):
    """
    Schema for the incoming calculation request.
    """
    operation: str = Field(..., description="The arithmetic operation to perform (e.g., 'add', 'subtract', 'multiply', 'divide').")
    num1: float = Field(..., description="The first number for the operation.")
    num2: float = Field(..., description="The second number for the operation.")

class CalculationResponse(BaseModel):
    """
    Schema for a successful calculation response.
    """
    result: float = Field(..., description="The result of the arithmetic operation.")

class ErrorResponse(BaseModel):
    """
    Schema for an error response.
    """
    message: str = Field(..., description="A human-readable message describing the error.")
    error_type: str = Field(..., description="A short code or name for the error type.")
