from flask import Blueprint, request, jsonify
from pydantic import ValidationError

from src.calculator import core
from src.calculator.errors import DivisionByZeroError, InvalidOperationError
from src.api.schemas import CalculationRequest, CalculationResponse, ErrorResponse

# Create a Flask Blueprint for calculator API routes
calculator_bp = Blueprint('calculator_bp', __name__, url_prefix='/') # Root URL prefix for the blueprint

@calculator_bp.route('/calculate', methods=['POST'])
def calculate():
    """
    API endpoint to perform arithmetic calculations.
    Expects a JSON payload with 'operation', 'num1', and 'num2'.
    """
    try:
        # Validate request body using Pydantic
        # request.get_json(force=True) can be used if Content-Type is not strictly 'application/json'
        # but for clean API design, it's better to expect correct Content-Type.
        data = CalculationRequest.model_validate(request.get_json())
        
        operation = data.operation
        num1 = data.num1
        num2 = data.num2

        result = core.calculate(operation, num1, num2)
        
        # Construct and return successful response
        response_data = CalculationResponse(result=result)
        return jsonify(response_data.model_dump()), 200

    except ValidationError as e:
        # Pydantic validation error for malformed request payload
        error_response = ErrorResponse(
            message="Invalid request payload.",
            error_type="Validation Error"
        )
        # Optionally, include detailed errors for development/debugging:
        # error_response.details = e.errors()
        return jsonify(error_response.model_dump()), 400
    
    except DivisionByZeroError as e:
        # Custom error for division by zero
        error_response = ErrorResponse(
            message=str(e),
            error_type="Division By Zero Error"
        )
        return jsonify(error_response.model_dump()), 400
    
    except InvalidOperationError as e:
        # Custom error for unsupported operation
        error_response = ErrorResponse(
            message=str(e),
            error_type="Invalid Operation Error"
        )
        return jsonify(error_response.model_dump()), 400
    
    except Exception as e:
        # Catch any other unexpected errors
        # Log the error for debugging purposes in a real application
        # current_app.logger.error(f"Unhandled error in /calculate: {e}", exc_info=True)
        error_response = ErrorResponse(
            message="An unexpected error occurred. Please try again later.",
            error_type="Internal Server Error"
        )
        return jsonify(error_response.model_dump()), 500
