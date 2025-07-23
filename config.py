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
    EMAIL_USERNAME = get_env_str("EMAIL_USERNAME")
    EMAIL_PASSWORD = get_env_str("EMAIL_PASSWORD")
    EMAIL_SERVER = get_env_str("EMAIL_SERVER")
    EMAIL_PORT = get_env_int("EMAIL_PORT")

    SQLALCHEMY_DATABASE_URI = "sqlite:///app.db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    SECRET_KEY = secrets.token_hex(16)