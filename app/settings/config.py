import os
import re

from typing import Pattern
from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict

BASEPATH = os.getcwd()


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file='./.env', env_file_encoding='utf-8')
    DEBUG: bool = False
    CHUNK_SIZE: int

    PORT: int
    HOST: str
    DOMAIN: str
    TGTOKEN: SecretStr

    WEBHOOK_ENDPOINT: str
    WEBHOOK_URL: str

    GSHEETS_CREDS_PATH: str
    GSHEETURL: str
    WORKSHEET_TITLE: str
    PARSER_API_URL: str

    YADISK_OAUTH_TOKEN: str
    IMGS_PATH: str = '%s/img' % BASEPATH
    
    PPTX_TEMPLATE_PATH: str = '%s/templates/template3.pptx' % BASEPATH
    PPTX_OUTPUT_DIRPATH: str = '%s/generated' % BASEPATH
    PICTURES_PLACEHOLDERS: dict = {
        'map': None, # Добавление фасада отменено в template3 шаблоне
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
        'Img11': None,
        'Img11': None,
        'Img12': None,
    }
    PROCEDURE_FORMS: dict = {
        'Открытый аукцион в электронной форме': 1,
        'Открытый аукцион в электронной форме «преимущественное право»': 1,
        'Открытый конкурс в электронной форме': 1,
        'Публичное предложение': 2,
        'Без объявления цены': 3,
    }
    TENDER_ID_REGEX: Pattern = re.compile(r'^\d{8,}$')


settings = Settings()
