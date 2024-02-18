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


class StickerAdvert(BaseSettings):
    username: str = ' @StickMaker_robot'
    bot_postfix: str = '_by_in_progress_bot'
    channel_id: int = -1001847782569
    reports_id: int = -1001914767401


config = Settings()
sticker_global_settings = StickerAdvert()
