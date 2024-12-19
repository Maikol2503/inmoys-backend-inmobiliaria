# from pydantic import BaseSettings
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    database_url: str
    secret_key: str
    debug: bool
    correo:str
    token:str



    # class Config:
    #     env_file = ".env"
