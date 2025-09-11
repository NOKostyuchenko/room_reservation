from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_title: str = 'Бронирование переговорок'
    app_author: str
    

    class Config:
        env_file = ".env"
        _env_file_encoding = "utf-8"


settings = Settings()