import os
from datetime import timedelta

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "supersecret123")
    
    # Database
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", "postgresql://hostel_hunt_db_user:m8hd5xOaTuBGpWiljXbtpjgE2t2cm0zt@dpg-d4ir8l63jp1c73ajnci0-a.oregon-postgres.render.com/hostel_hunt_db")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # JWT
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "jwtsecret123")
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(minutes=180)
    
    # Mail settings
    MAIL_SERVER = os.getenv('MAIL_SERVER', 'smtp.googlemail.com')
    MAIL_PORT = int(os.getenv('MAIL_PORT', 587))
    MAIL_USE_TLS = os.getenv('MAIL_USE_TLS', 'True') == 'True'
    MAIL_USERNAME = os.getenv('MAIL_USERNAME')
    MAIL_PASSWORD = os.getenv('MAIL_PASSWORD')
    # CORS Configuration
    CORS_HEADERS = 'Content-Type'
    # For now, allow all origins. Frontend uses Authorization headers (no cookies),
    # so we can safely disable credentials and use a wildcard origin to avoid CORS misconfig.
    CORS_ORIGINS = "https://hostel-hunt-4j89-git-main-milton-ngenos-projects.vercel.app/"
    CORS_METHODS = ["GET", "POST", "PUT", "DELETE", "OPTIONS"]
    CORS_ALLOW_HEADERS = ["Content-Type", "Authorization"]
    CORS_SUPPORTS_CREDENTIALS = False