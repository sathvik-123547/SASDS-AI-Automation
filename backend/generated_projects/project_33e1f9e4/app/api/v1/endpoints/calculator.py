from fastapi import APIRouter, HTTPException, status
from app.schemas.calculator import OperationRequest, ResultResponse, ErrorResponse
from app.services.calculator_service import CalculatorService, DivisionByZeroError

router = APIRouter()
calculator_service = CalculatorService()

@router.post("/add", response_model=ResultResponse, summary="Add two numbers")
async def add_numbers(request: OperationRequest):
    """
    Performs addition of two numbers.
    """
    result = calculator_service.add(request.operand1, request.operand2)
    return ResultResponse(result=result)

@router.post("/subtract", response_model=ResultResponse, summary="Subtract two numbers")
async def subtract_numbers(request: OperationRequest):
    """
    Performs subtraction of two numbers.
    """
    result = calculator_service.subtract(request.operand1, request.operand2)
    return ResultResponse(result=result)

@router.post("/multiply", response_model=ResultResponse, summary="Multiply two numbers")
async def multiply_numbers(request: OperationRequest):
    """
    Performs multiplication of two numbers.
    """
    result = calculator_service.multiply(request.operand1, request.operand2)
    return ResultResponse(result=result)

@router.post("/divide", response_model=ResultResponse, responses={
    status.HTTP_400_BAD_REQUEST: {"model": ErrorResponse, "description": "Division by zero error"}
}, summary="Divide two numbers")
async def divide_numbers(request: OperationRequest):
    """
    Performs division of two numbers.
    Raises an error if division by zero is attempted.
    """
    try:
        result = calculator_service.divide(request.operand1, request.operand2)
        return ResultResponse(result=result)
    except DivisionByZeroError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

