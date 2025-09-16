import os
import secrets
from dotenv import load_dotenv

load_dotenv()

def get_env_str(key: str) -> str:
    value = os.getenv(key)
    if value is None:
        raise ValueError(f"Missing required environment variable: {key}")
    return value

def get_env_int(key: str) -> int:
    value = os.getenv(key)
    if value is None:
        raise ValueError(f"Missing required environment variable: {key}")
    return int(value)

class Config:
    SQLALCHEMY_DATABASE_URI = "sqlite:///app.db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    SECRET_KEY = secrets.token_hex(16)
    # Keep users logged in for 7 days
    from datetime import timedelta
    PERMANENT_SESSION_LIFETIME = timedelta(days=7)