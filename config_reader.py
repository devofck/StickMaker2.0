from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import SecretStr


class Settings(BaseSettings):
    bot_token: SecretStr
    model_config = SettingsConfigDict(
        env_file='.env',
        env_file_encoding='utf-8',
    )
    # PG DATA
    PG_USER: str
    password: str
    ip: str
    port: int
    base: str


config = Settings()
