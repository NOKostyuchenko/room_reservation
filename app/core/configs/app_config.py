from core.configs import MainSettings


class AppSettings(MainSettings):
    app_port: int = 8080
    app_host: str = "localhost"
    app_title: str = 'Бронирование переговорок'


app_settings = AppSettings()
