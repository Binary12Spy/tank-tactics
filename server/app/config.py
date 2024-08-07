from pydantic import BaseSettings
import os

class Settings(BaseSettings):
    database_url: str = "sqlite:///./test.db"
    database_url_prod: str = os.getenv("DATABASE_URL_PROD", "postgresql://user:password@localhost/dbname")

    class Config:
        env_file = ".env"

settings = Settings()
