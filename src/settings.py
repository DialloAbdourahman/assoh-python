from pydantic_settings import BaseSettings
from utils.config import base_url

class Settings(BaseSettings):
    app_name:str = "Assoh"
    base_path:str = base_url

    # model_config = SettingsConfigDict(env_file=".env")
