import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # Flask-Session Configuration
    SECRET_KEY = os.getenv('FLASK_SECRET_KEY', 'default-dev-key')
    
    # Store sessions on the filesystem (server-side), not in cookies
    SESSION_TYPE = 'filesystem'
    SESSION_PERMANENT = False
    SESSION_USE_SIGNER = True
    
    # Cookie Security
    # In production with HTTPS, set these to True
    SESSION_COOKIE_SECURE = False 
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'
