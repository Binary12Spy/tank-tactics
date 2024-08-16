from pydantic_settings import BaseSettings
import secrets
import base64
import os

class Settings(BaseSettings):
    server_host: str = "0.0.0.0"
    server_port: int = 8000
    database_url: str = os.getenv('DATABASE_URL', 'sqlite:///dev.sqlite3')
    jwt_secret_key: str = os.getenv('JWT_SECRET_KEY', base64.urlsafe_b64encode(secrets.token_bytes(32)).decode())
    jwt_lifetime_minutes: int = 120
    max_players_per_game: int = os.getenv('MAX_PLAYERS_PER_GAME', 16)

    class Config:
        env_file = ".env"

settings = Settings()