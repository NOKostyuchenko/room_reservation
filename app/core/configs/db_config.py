from core.configs import MainSettings


class DBSettings(MainSettings):
    db_user: str
    db_password: str
    db_host: str
    db_port: int
    db_name: str


db_settings = DBSettings()
