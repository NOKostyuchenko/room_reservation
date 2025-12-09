from core.configs import MainSettings


class AppSettings(MainSettings):
    port: int = 8080
    host: str = "localhost"
    app_title: str = 'Бронирование переговорок'
    database_url: str


app_settings = AppSettings()
