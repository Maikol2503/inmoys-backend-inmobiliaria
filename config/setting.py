from pydantic import BaseSettings

class Settings(BaseSettings):
    database_url: str
    secret_key: str
    debug: bool
    correo:str
    token:str



    class Config:
        env_file = ".env"