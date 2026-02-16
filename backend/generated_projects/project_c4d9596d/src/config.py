import os

class Config:
    """Base configuration"""
    SECRET_KEY = os.getenv('SECRET_KEY', 'default_secret_key_please_change')
    DEBUG = False
    TESTING = False

class DevelopmentConfig(Config):
    """Development configuration"""
    DEBUG = True
    FLASK_ENV = 'development'

class ProductionConfig(Config):
    """Production configuration"""
    FLASK_ENV = 'production'
    # For production, ensure SECRET_KEY is set via environment variable
    # Disable debug mode in production for security
    DEBUG = False

class TestingConfig(Config):
    """Testing configuration"""
    TESTING = True
    DEBUG = True # Often True for testing to see output/errors
    FLASK_ENV = 'testing'
