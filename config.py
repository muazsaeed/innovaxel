import os
from dotenv import load_dotenv

# Load environment variables from .env file if present
load_dotenv()

class Config:
    """Base configuration class."""
    DEBUG = False
    TESTING = False
    MONGO_URI = os.getenv('MONGO_URI', 'mongodb://localhost:27017/')
    MONGO_DB = os.getenv('MONGO_DB', 'url_shortener')
    BASE_URL = os.getenv('BASE_URL', 'http://localhost:5000/')
    # The length of the generated shortcode
    SHORTCODE_LENGTH = int(os.getenv('SHORTCODE_LENGTH', 6))

class DevelopmentConfig(Config):
    """Development configuration."""
    DEBUG = True

class TestingConfig(Config):
    """Testing configuration."""
    TESTING = True
    DEBUG = True
    MONGO_DB = os.getenv('MONGO_DB_TEST', 'url_shortener_test')

class ProductionConfig(Config):
    """Production configuration."""
    DEBUG = False

# Configuration dictionary
config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}

# Get configuration based on environment
env = os.getenv('FLASK_ENV', 'default')
current_config = config[env] 