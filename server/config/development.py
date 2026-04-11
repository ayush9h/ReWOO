from pydantic import Field, SecretStr
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    GROQ_API_KEY: SecretStr = Field(validation_alias="groq_api_key")

    class Config:
        env_file = "./.env"


settings = Settings()  # type: ignore
