from typing import Literal, Type

from pydantic import BaseSettings
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker


class Settings(BaseSettings):
    environment: Literal["dev", "qa", "prod"]
    database_url: str

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()

engine = create_engine(settings.database_url)
SessionLocal: Type[Session] = sessionmaker(engine)
