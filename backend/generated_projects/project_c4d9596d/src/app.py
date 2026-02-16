from flask import Flask, jsonify
from src.config import DevelopmentConfig # Ensure Config is accessible

def create_app(config_object=DevelopmentConfig):
    """
    Application factory function for the Flask app.
    Initializes and configures the Flask application.
    """
    app = Flask(__name__)
    app.config.from_object(config_object)

    # Register blueprints
    from src.api.routes import calculator_bp
    app.register_blueprint(calculator_bp)

    # Define a simple root route for health check or info
    @app.route('/')
    def index():
        return jsonify({"message": "Calculator API is running!"})

    # Register a generic error handler for 404 (Not Found)
    @app.errorhandler(404)
    def not_found_error(error):
        return jsonify({"message": "Resource not found.", "error_type": "Not Found"}), 404

    # Register a generic error handler for 500 (Internal Server Error)
    @app.errorhandler(500)
    def internal_server_error(error):
        app.logger.error(f"Internal Server Error: {error}") # Log the error
        return jsonify({"message": "An unexpected error occurred.", "error_type": "Internal Server Error"}), 500


    return app
