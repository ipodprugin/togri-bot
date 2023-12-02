import os

from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    IMGS_PATH: str = f'{os.getcwd()}/img'

settings = Settings()
