import os

from pydantic import BaseSettings


class Settings(BaseSettings):
    REDIS_HOST: str
    REDIS_PORT: int

    class Config:
        env_file = os.getenv('ENV_FILE')


settings = Settings()
