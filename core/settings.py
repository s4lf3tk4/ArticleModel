from pydantic_settings import BaseSettings
from pydantic import Field, field_validator
from typing import Optional
from pathlib import Path

class Settings(BaseSettings):
    work_dir: str = Field(
            ".",
            alias="WORKDIR",
            description="Дирректория, куда сохраняется доклад"
    )
    max_symbols: int = Field(
        2000,
        alias="MAX_SYMBOLS",
        description="Базовый URL для ChatAnywhere"
        )
    max_iterations: int = Field(
        4,
        alias="MAX_ITERATIONS",
        description="Количсетво итераций"
        )
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        populate_by_name = True

settings = Settings()

WORKDIR = Path(settings.work_dir)
MAX_SYMBOLS = settings.max_symbols
MAX_ITERATIONS = settings.max_iterations
