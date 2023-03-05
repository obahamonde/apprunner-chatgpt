from pydantic import BaseSettings, BaseConfig, Field

class Settings(BaseSettings):
    """Settings for the application
    """
    API_KEY: str = Field(..., env="API_KEY")
    FAUNA_SECRET: str = Field(..., env="FAUNA_SECRET")
    AUTH0_DOMAIN: str = Field(..., env="AUTH0_DOMAIN")
    
    class Config(BaseConfig):
        env_file = ".env"
        file_encoding = "utf-8"
        
env = Settings()