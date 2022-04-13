from pydantic import BaseSettings

class Settings(BaseSettings):
    ST: int = 60
    DB_PATH: str = 'sqlite:///./app/src/db/thndr.db'
settings = Settings()