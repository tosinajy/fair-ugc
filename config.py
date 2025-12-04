import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # Generate a secure key in production: secrets.token_hex(16)
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-prod'
    
    # Database Configuration
    # Default to local postgres if not set
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'postgresql://postgres:vaug@localhost/fairugc'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Custom App Configs
    ADMIN_DEFAULT_PASS = os.environ.get('ADMIN_DEFAULT_PASS') or 'admin123'