from pydantic import BaseModel, Field

class OperationRequest(BaseModel):
    """
    Schema for calculator operation requests.
    """
    operand1: float = Field(..., description="The first number for the operation")
    operand2: float = Field(..., description="The second number for the operation")

class ResultResponse(BaseModel):
    """
    Schema for calculator operation results.
    """
    result: float = Field(..., description="The result of the operation")

class ErrorResponse(BaseModel):
    """
    Schema for error responses.
    """
    detail: str = Field(..., description="A detailed error message")

