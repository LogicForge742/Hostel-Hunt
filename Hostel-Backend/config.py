import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'your-secret-key'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'postgresql://hostel_user:JesusLoves123@localhost:5432/hostel_db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY') or 'jwt-secret-key'
    MAIL_SERVER = os.environ.get('MAIL_SERVER') or 'smtp.gmail.com'
    MAIL_PORT = int(os.environ.get('MAIL_PORT') or 587)
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS') or True
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    JWT_ACCESS_TOKEN_EXPIRE_MINUTES = int(os.environ.get('JWT_ACCESS_TOKEN_EXPIRE_MINUTES') or 15)
    JWT_REFRESH_TOKEN_EXPIRE_DAYS = int(os.environ.get('JWT_REFRESH_TOKEN_EXPIRE_DAYS') or 30)
    # Store uploads in an absolute path so Flask can reliably serve them
    UPLOAD_FOLDER = os.environ.get('UPLOAD_FOLDER') or os.path.join(BASE_DIR, 'uploads')
    MAX_CONTENT_LENGTH = int(os.environ.get('MAX_CONTENT_LENGTH') or 16 * 1024 * 1024)  # 16MB
    DEBUG = os.environ.get('DEBUG') or True
    TESTING = os.environ.get('TESTING') or False
    CORS_ALLOW_HEADERS = ['Content-Type', 'Authorization']
    CORS_ORIGINS = os.environ.get('CORS_ORIGINS') or 'http://localhost:5174'
    CORS_METHODS = ['GET', 'POST', 'PUT', 'DELETE', 'OPTIONS']
    CORS_SUPPORTS_CREDENTIALS = True
