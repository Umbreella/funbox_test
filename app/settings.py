import os

from pydantic import BaseSettings


class Settings(BaseSettings):
    FASTAPI_APP_ALLOW_ORIGINS: str
    REDIS_HOST: str
    REDIS_PORT: int

    class Config:
        env_file = os.getenv('ENV_FILE')


settings = Settings()
