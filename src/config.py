from dotenv import load_dotenv
from pydantic import BaseSettings, BaseConfig, Field
import os

load_dotenv()


class Settings(BaseSettings):
    """Settings for the application
    """
    API_KEY: str = Field(default = os.environ.get("API_KEY"))   
    FAUNA_SECRET: str = Field(default=os.environ.get("FAUNA_SECRET"))
    AUTH0_DOMAIN: str = Field(default=os.environ.get("AUTH0_DOMAIN"))
    
    class Config(BaseConfig):
        env_file = ".env"
        file_encoding = "utf-8"
        
env = Settings()