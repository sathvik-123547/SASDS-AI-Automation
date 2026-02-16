import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Set default FLASK_APP if not already set (e.g., by Flask CLI)
os.environ.setdefault('FLASK_APP', 'src.app:create_app')

from src.app import create_app
from src.config import DevelopmentConfig, ProductionConfig # Import specific configs

# Determine which config to use based on FLASK_ENV
env = os.getenv('FLASK_ENV', 'development')
if env == 'production':
    config_object = ProductionConfig
else:
    config_object = DevelopmentConfig

app = create_app(config_object=config_object)

if __name__ == '__main__':
    # Flask's built-in development server (not for production)
    app.run(debug=os.getenv('FLASK_ENV') == 'development')
