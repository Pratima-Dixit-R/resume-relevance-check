import os

class Config:
    DEBUG = os.getenv('DEBUG', 'False') == 'True'
    DATABASE_URI = os.getenv('DATABASE_URI', 'sqlite:///resume_relevance_check.db')
    SECRET_KEY = os.getenv('SECRET_KEY', 'your_secret_key')
    ALLOWED_EXTENSIONS = {'pdf', 'docx'}
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16 MB limit for uploads
    EMBEDDING_MODEL = os.getenv('EMBEDDING_MODEL', 'default_model')
    API_KEY = os.getenv('API_KEY', 'your_api_key')