from typing import List

from pydantic import SecretStr, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    BOT_TOKEN: SecretStr

    POSTGRES_USER: str
    POSTGRES_PASSWORD: SecretStr
    POSTGRES_DB: str
    POSTGRES_HOST: str
    POSTGRES_PORT: int

    MONGO_USER: str
    MONGO_PASSWORD: SecretStr
    MONGO_DB: str
    MONGO_HOST: str
    MONGO_PORT: int

    PGADMIN_EMAIL: str = ""   
    PGADMIN_PASSWORD: str = "" 
    
    model_config = SettingsConfigDict(
        env_file=".env", 
        extra="ignore",
        env_prefix=""  
    )
    
    @property
    def postgres_url(self):
        return (
            f"postgresql+asyncpg://{self.POSTGRES_USER}:"
            f"{self.POSTGRES_PASSWORD.get_secret_value()}@"
            f"{self.POSTGRES_HOST}:"
            f"{self.POSTGRES_PORT}/"
            f"{self.POSTGRES_DB}"
        )
        
    @property
    def mongo_url(self):
        return (
            f"mongodb://{self.MONGO_USER}:{self.MONGO_PASSWORD.get_secret_value()}"
            f"@{self.MONGO_HOST}:{self.MONGO_PORT}/"
            f"{self.MONGO_DB}?authSource=admin"
        )

config = Settings()