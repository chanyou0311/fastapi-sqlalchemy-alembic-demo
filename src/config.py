from typing import Literal

from pydantic import BaseSettings


class Settings(BaseSettings):
    environment: Literal["dev", "qa", "prod"]
    database_url: str

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
