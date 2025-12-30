from pydantic_settings import BaseSettings


class MainSettings(BaseSettings):


    class Config:
        env_file = ".env"
        _env_file_encoding = "utf-8"
        extra = "ignore"
