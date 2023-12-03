import os

from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict

BASEPATH = os.getcwd()


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file='./.env', env_file_encoding='utf-8')
    PORT: int
    HOST: str
    DOMAIN: str
    TGTOKEN: SecretStr

    WEBHOOK_ENDPOINT: str
    WEBHOOK_URL: str

    GSHEETS_CREDS_PATH: str
    GSHEETURL: str

    YADISK_OAUTH_TOKEN: str
    IMGS_PATH: str = '%s/img' % BASEPATH
    
    PPTX_TEMPLATE_PATH: str = '%s/templates/template2.pptx' % BASEPATH
    PPTX_OUTPUT_DIRPATH: str = '%s/generated' % BASEPATH
    PICTURES_PLACEHOLDERS: dict = {
        'map': None,
        'plan': None,
        'Img1': None,
        'Img2': None,
        'Img3': None,
        'Img4': None,
        'Img5': None,
        'Img6': None,
        'Img7': None,
        'Img8': None,
        'Img9': None,
    }

settings = Settings()