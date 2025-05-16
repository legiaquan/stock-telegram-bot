from pydantic_settings import BaseSettings
from typing import Literal

class Settings(BaseSettings):
    API_V1_STR: str = "/api/v1"
    ENVIRONMENT: Literal["local", "staging", "production"] = "local"
    PROJECT_NAME: str = "Stock Bot"

settings = Settings()  # type: ignore